#include <linux/module.h>
#include <linux/export-internal.h>
#include <linux/compiler.h>

MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x11f4259a, "_raw_spin_lock_irqsave" },
	{ 0xd272d446, "__fentry__" },
	{ 0xe8213e80, "_printk" },
	{ 0xbd03ed67, "__ref_stack_chk_guard" },
	{ 0x6ac784f4, "schedule_timeout" },
	{ 0xd272d446, "__stack_chk_fail" },
	{ 0xff0106da, "refcount_warn_saturate" },
	{ 0x90a48d82, "__ubsan_handle_out_of_bounds" },
	{ 0x2ed01892, "compat_ptr_ioctl" },
	{ 0x7a5ffe84, "init_wait_entry" },
	{ 0xc8167060, "noop_llseek" },
	{ 0xbd03ed67, "random_kmalloc_seed" },
	{ 0xc5c2a6a3, "const_current_task" },
	{ 0x444885a7, "_raw_spin_unlock_irqrestore" },
	{ 0xe98a2697, "misc_register" },
	{ 0xd272d446, "__x86_return_thunk" },
	{ 0x092a35a2, "_copy_to_user" },
	{ 0xe804603d, "__init_waitqueue_head" },
	{ 0x59cf8621, "nonseekable_open" },
	{ 0xce56ea17, "__kmalloc_cache_noprof" },
	{ 0x58914088, "nsecs_to_jiffies" },
	{ 0xe4de56b4, "__ubsan_handle_load_invalid_value" },
	{ 0x7851be11, "__SCT__might_resched" },
	{ 0xa65b83f9, "kmalloc_caches" },
	{ 0x155e60e3, "misc_deregister" },
	{ 0x092a35a2, "_copy_from_user" },
	{ 0xb730487b, "finish_wait" },
	{ 0xcb8b6ec6, "kfree" },
	{ 0xc281f1fb, "prepare_to_wait_event" },
	{ 0x68a1b6c6, "__wake_up" },
	{ 0xe9196a28, "module_layout" },
};

static const u32 ____version_ext_crcs[]
__used __section("__version_ext_crcs") = {
	0x11f4259a,
	0xd272d446,
	0xe8213e80,
	0xbd03ed67,
	0x6ac784f4,
	0xd272d446,
	0xff0106da,
	0x90a48d82,
	0x2ed01892,
	0x7a5ffe84,
	0xc8167060,
	0xbd03ed67,
	0xc5c2a6a3,
	0x444885a7,
	0xe98a2697,
	0xd272d446,
	0x092a35a2,
	0xe804603d,
	0x59cf8621,
	0xce56ea17,
	0x58914088,
	0xe4de56b4,
	0x7851be11,
	0xa65b83f9,
	0x155e60e3,
	0x092a35a2,
	0xb730487b,
	0xcb8b6ec6,
	0xc281f1fb,
	0x68a1b6c6,
	0xe9196a28,
};
static const char ____version_ext_names[]
__used __section("__version_ext_names") =
	"_raw_spin_lock_irqsave\0"
	"__fentry__\0"
	"_printk\0"
	"__ref_stack_chk_guard\0"
	"schedule_timeout\0"
	"__stack_chk_fail\0"
	"refcount_warn_saturate\0"
	"__ubsan_handle_out_of_bounds\0"
	"compat_ptr_ioctl\0"
	"init_wait_entry\0"
	"noop_llseek\0"
	"random_kmalloc_seed\0"
	"const_current_task\0"
	"_raw_spin_unlock_irqrestore\0"
	"misc_register\0"
	"__x86_return_thunk\0"
	"_copy_to_user\0"
	"__init_waitqueue_head\0"
	"nonseekable_open\0"
	"__kmalloc_cache_noprof\0"
	"nsecs_to_jiffies\0"
	"__ubsan_handle_load_invalid_value\0"
	"__SCT__might_resched\0"
	"kmalloc_caches\0"
	"misc_deregister\0"
	"_copy_from_user\0"
	"finish_wait\0"
	"kfree\0"
	"prepare_to_wait_event\0"
	"__wake_up\0"
	"module_layout\0"
;

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "D6AF4D1A3D067F8BC2FC7B3");
