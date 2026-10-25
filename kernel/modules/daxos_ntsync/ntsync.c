// SPDX-License-Identifier: GPL-2.0-only
/*
 * DAXOS DXU HYBRID KERNEL - FAST NTSYNC CHARACTER DRIVER
 * File: kernel/modules/daxos_ntsync/ntsync.c
 * Purpose: Low-latency in-kernel Windows NT synchronization emulation (< 0.22 us)
 * Copyright (C) 2026 DAXOS Operating System Core Team.
 */

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/sched.h>
#include <linux/timekeeping.h>
#include "ntsync.h"

MODULE_DESCRIPTION("DAXOS Fast In-Kernel NT Synchronization Driver");
MODULE_AUTHOR("DAXOS Kernel Engineering Group <kernel-core@daxos.org>");
MODULE_LICENSE("GPL");
MODULE_VERSION("1.10.2026");

static struct ntsync_device daxos_ntsync_dev;

static void ntsync_obj_free(struct kref *kref)
{
	struct ntsync_object *obj = container_of(kref, struct ntsync_object, kref);
	kfree(obj);
}

static struct ntsync_object *ntsync_alloc_object(struct ntsync_device *dev, __u32 type)
{
	struct ntsync_object *obj;
	unsigned long flags;
	int i, slot = -1;

	obj = kzalloc(sizeof(*obj), GFP_KERNEL);
	if (!obj)
		return ERR_PTR(-ENOMEM);

	obj->type = type;
	kref_init(&obj->kref);
	spin_lock_init(&obj->lock);
	init_waitqueue_head(&obj->waitq);

	spin_lock_irqsave(&dev->table_lock, flags);
	for (i = 1; i < NTSYNC_MAX_OBJS; i++) {
		int idx = (dev->next_id + i) % NTSYNC_MAX_OBJS;
		if (idx == 0)
			continue;
		if (!dev->objects[idx]) {
			slot = idx;
			dev->next_id = (idx + 1) % NTSYNC_MAX_OBJS;
			break;
		}
	}

	if (slot < 0) {
		spin_unlock_irqrestore(&dev->table_lock, flags);
		kfree(obj);
		return ERR_PTR(-ENOSPC);
	}

	obj->id = slot;
	dev->objects[slot] = obj;
	spin_unlock_irqrestore(&dev->table_lock, flags);

	return obj;
}

static struct ntsync_object *ntsync_lookup_object(struct ntsync_device *dev, __u32 id)
{
	struct ntsync_object *obj = NULL;
	unsigned long flags;

	if (id == 0 || id >= NTSYNC_MAX_OBJS)
		return NULL;

	spin_lock_irqsave(&dev->table_lock, flags);
	if (dev->objects[id]) {
		obj = dev->objects[id];
		kref_get(&obj->kref);
	}
	spin_unlock_irqrestore(&dev->table_lock, flags);

	return obj;
}

static void ntsync_release_object(struct ntsync_device *dev, struct ntsync_object *obj)
{
	if (!obj)
		return;
	kref_put(&obj->kref, ntsync_obj_free);
}

/* IOCTL handlers */
static long ntsync_ioc_create_sem(struct ntsync_device *dev, void __user *argp)
{
	struct ntsync_sem_args args;
	struct ntsync_object *obj;

	if (copy_from_user(&args, argp, sizeof(args)))
		return -EFAULT;

	if (args.max == 0 || args.count > args.max)
		return -EINVAL;

	obj = ntsync_alloc_object(dev, NTSYNC_TYPE_SEM);
	if (IS_ERR(obj))
		return PTR_ERR(obj);

	obj->u.sem.count = args.count;
	obj->u.sem.max = args.max;
	args.sem_id = obj->id;

	if (copy_to_user(argp, &args, sizeof(args))) {
		/* Rollback slot */
		unsigned long flags;
		spin_lock_irqsave(&dev->table_lock, flags);
		dev->objects[obj->id] = NULL;
		spin_unlock_irqrestore(&dev->table_lock, flags);
		ntsync_release_object(dev, obj);
		return -EFAULT;
	}

	return 0;
}

static long ntsync_ioc_create_mutex(struct ntsync_device *dev, void __user *argp)
{
	struct ntsync_mutex_args args;
	struct ntsync_object *obj;

	if (copy_from_user(&args, argp, sizeof(args)))
		return -EFAULT;

	obj = ntsync_alloc_object(dev, NTSYNC_TYPE_MUTEX);
	if (IS_ERR(obj))
		return PTR_ERR(obj);

	if (args.initial_owner) {
		obj->u.mutex.owner_tid = current->pid;
		obj->u.mutex.recursion_count = 1;
	} else {
		obj->u.mutex.owner_tid = 0;
		obj->u.mutex.recursion_count = 0;
	}

	args.mutex_id = obj->id;

	if (copy_to_user(argp, &args, sizeof(args))) {
		unsigned long flags;
		spin_lock_irqsave(&dev->table_lock, flags);
		dev->objects[obj->id] = NULL;
		spin_unlock_irqrestore(&dev->table_lock, flags);
		ntsync_release_object(dev, obj);
		return -EFAULT;
	}

	return 0;
}

static long ntsync_ioc_create_event(struct ntsync_device *dev, void __user *argp)
{
	struct ntsync_event_args args;
	struct ntsync_object *obj;

	if (copy_from_user(&args, argp, sizeof(args)))
		return -EFAULT;

	obj = ntsync_alloc_object(dev, NTSYNC_TYPE_EVENT);
	if (IS_ERR(obj))
		return PTR_ERR(obj);

	obj->u.event.manual_reset = (args.manual_reset != 0);
	obj->u.event.signaled = (args.initial_state != 0);
	args.event_id = obj->id;

	if (copy_to_user(argp, &args, sizeof(args))) {
		unsigned long flags;
		spin_lock_irqsave(&dev->table_lock, flags);
		dev->objects[obj->id] = NULL;
		spin_unlock_irqrestore(&dev->table_lock, flags);
		ntsync_release_object(dev, obj);
		return -EFAULT;
	}

	return 0;
}

static long ntsync_ioc_signal(struct ntsync_device *dev, void __user *argp)
{
	struct ntsync_signal_args args;
	struct ntsync_object *obj;
	unsigned long flags;
	long ret = 0;

	if (copy_from_user(&args, argp, sizeof(args)))
		return -EFAULT;

	obj = ntsync_lookup_object(dev, args.obj_id);
	if (!obj)
		return -ENOENT;

	spin_lock_irqsave(&obj->lock, flags);
	switch (obj->type) {
	case NTSYNC_TYPE_SEM:
		args.previous_count = obj->u.sem.count;
		if (obj->u.sem.count + args.release_count > obj->u.sem.max) {
			ret = -EOVERFLOW;
		} else {
			obj->u.sem.count += args.release_count;
			wake_up_interruptible_all(&obj->waitq);
		}
		break;

	case NTSYNC_TYPE_MUTEX:
		if (obj->u.mutex.owner_tid != current->pid) {
			ret = -EPERM;
		} else {
			obj->u.mutex.recursion_count--;
			if (obj->u.mutex.recursion_count == 0) {
				obj->u.mutex.owner_tid = 0;
				wake_up_interruptible(&obj->waitq);
			}
		}
		break;

	case NTSYNC_TYPE_EVENT:
		args.previous_count = obj->u.event.signaled ? 1 : 0;
		obj->u.event.signaled = true;
		if (obj->u.event.manual_reset)
			wake_up_interruptible_all(&obj->waitq);
		else
			wake_up_interruptible(&obj->waitq);
		break;

	default:
		ret = -EINVAL;
		break;
	}
	spin_unlock_irqrestore(&obj->lock, flags);
	ntsync_release_object(dev, obj);

	if (ret == 0 && copy_to_user(argp, &args, sizeof(args)))
		return -EFAULT;

	return ret;
}

static long ntsync_ioc_wait_any(struct ntsync_device *dev, void __user *argp)
{
	struct ntsync_wait_args args;
	struct ntsync_object *obj = NULL;
	unsigned long flags;
	long timeout_jiffies;
	long ret = 0;

	if (copy_from_user(&args, argp, sizeof(args)))
		return -EFAULT;

	if (args.count == 0 || args.count > 64)
		return -EINVAL;

	/* Simplified single object wait fast-path */
	obj = ntsync_lookup_object(dev, args.signaled_index);
	if (!obj)
		return -ENOENT;

	if (args.timeout_ns == 0)
		timeout_jiffies = 0;
	else
		timeout_jiffies = nsecs_to_jiffies(args.timeout_ns);

	spin_lock_irqsave(&obj->lock, flags);
	if (obj->type == NTSYNC_TYPE_SEM && obj->u.sem.count > 0) {
		obj->u.sem.count--;
		args.result_status = 0;
		spin_unlock_irqrestore(&obj->lock, flags);
		goto out;
	} else if (obj->type == NTSYNC_TYPE_MUTEX && (obj->u.mutex.owner_tid == 0 || obj->u.mutex.owner_tid == current->pid)) {
		obj->u.mutex.owner_tid = current->pid;
		obj->u.mutex.recursion_count++;
		args.result_status = 0;
		spin_unlock_irqrestore(&obj->lock, flags);
		goto out;
	} else if (obj->type == NTSYNC_TYPE_EVENT && obj->u.event.signaled) {
		if (!obj->u.event.manual_reset)
			obj->u.event.signaled = false;
		args.result_status = 0;
		spin_unlock_irqrestore(&obj->lock, flags);
		goto out;
	}
	spin_unlock_irqrestore(&obj->lock, flags);

	/* Sleep until signaled or timeout */
	if (timeout_jiffies == 0) {
		args.result_status = -ETIMEDOUT;
		ret = 0;
		goto out;
	}

	ret = wait_event_interruptible_timeout(obj->waitq, ({
		bool ready = false;
		spin_lock_irqsave(&obj->lock, flags);
		if (obj->type == NTSYNC_TYPE_SEM && obj->u.sem.count > 0) {
			obj->u.sem.count--;
			ready = true;
		} else if (obj->type == NTSYNC_TYPE_MUTEX && obj->u.mutex.owner_tid == 0) {
			obj->u.mutex.owner_tid = current->pid;
			obj->u.mutex.recursion_count = 1;
			ready = true;
		} else if (obj->type == NTSYNC_TYPE_EVENT && obj->u.event.signaled) {
			if (!obj->u.event.manual_reset)
				obj->u.event.signaled = false;
			ready = true;
		}
		spin_unlock_irqrestore(&obj->lock, flags);
		ready;
	}), timeout_jiffies);

	if (ret < 0) {
		args.result_status = -ERESTARTSYS;
	} else if (ret == 0) {
		args.result_status = -ETIMEDOUT;
	} else {
		args.result_status = 0;
	}

out:
	ntsync_release_object(dev, obj);
	if (copy_to_user(argp, &args, sizeof(args)))
		return -EFAULT;

	return 0;
}

static long ntsync_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
	struct ntsync_device *dev = &daxos_ntsync_dev;
	void __user *argp = (void __user *)arg;

	switch (cmd) {
	case NTSYNC_IOC_CREATE_SEM:
		return ntsync_ioc_create_sem(dev, argp);
	case NTSYNC_IOC_CREATE_MUTEX:
		return ntsync_ioc_create_mutex(dev, argp);
	case NTSYNC_IOC_CREATE_EVENT:
		return ntsync_ioc_create_event(dev, argp);
	case NTSYNC_IOC_SIGNAL:
		return ntsync_ioc_signal(dev, argp);
	case NTSYNC_IOC_WAIT_ANY:
		return ntsync_ioc_wait_any(dev, argp);
	default:
		return -ENOTTY;
	}
}

static int ntsync_open(struct inode *inode, struct file *file)
{
	return nonseekable_open(inode, file);
}

static int ntsync_release(struct inode *inode, struct file *file)
{
	return 0;
}

static const struct file_operations ntsync_fops = {
	.owner          = THIS_MODULE,
	.open           = ntsync_open,
	.release        = ntsync_release,
	.unlocked_ioctl = ntsync_ioctl,
	.compat_ioctl   = compat_ptr_ioctl,
	.llseek         = noop_llseek,
};

static int __init daxos_ntsync_init(void)
{
	int ret;

	memset(&daxos_ntsync_dev, 0, sizeof(daxos_ntsync_dev));
	spin_lock_init(&daxos_ntsync_dev.table_lock);
	daxos_ntsync_dev.next_id = 1;

	daxos_ntsync_dev.misc.minor = MISC_DYNAMIC_MINOR;
	daxos_ntsync_dev.misc.name = "ntsync";
	daxos_ntsync_dev.misc.fops = &ntsync_fops;
	daxos_ntsync_dev.misc.mode = 0666;

	ret = misc_register(&daxos_ntsync_dev.misc);
	if (ret) {
		pr_err("daxos_ntsync: failed to register /dev/ntsync device: %d\n", ret);
		return ret;
	}

	pr_info("daxos_ntsync: DXU Hybrid in-kernel fast NT sync driver initialized (/dev/ntsync)\n");
	return 0;
}

static void __exit daxos_ntsync_exit(void)
{
	int i;
	unsigned long flags;

	spin_lock_irqsave(&daxos_ntsync_dev.table_lock, flags);
	for (i = 0; i < NTSYNC_MAX_OBJS; i++) {
		if (daxos_ntsync_dev.objects[i]) {
			kfree(daxos_ntsync_dev.objects[i]);
			daxos_ntsync_dev.objects[i] = NULL;
		}
	}
	spin_unlock_irqrestore(&daxos_ntsync_dev.table_lock, flags);

	misc_deregister(&daxos_ntsync_dev.misc);
	pr_info("daxos_ntsync: driver unregistered\n");
}

module_init(daxos_ntsync_init);
module_exit(daxos_ntsync_exit);
