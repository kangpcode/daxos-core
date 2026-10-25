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
	{ 0x95ac83d3, "kernel_kobj" },
	{ 0x11f4259a, "_raw_spin_lock_irqsave" },
	{ 0xd272d446, "__fentry__" },
	{ 0xe8213e80, "_printk" },
	{ 0xbd03ed67, "__ref_stack_chk_guard" },
	{ 0xd272d446, "__stack_chk_fail" },
	{ 0x9e3ce042, "sysfs_remove_file_ns" },
	{ 0x2ed01892, "compat_ptr_ioctl" },
	{ 0xc8167060, "noop_llseek" },
	{ 0x402db74e, "memcmp" },
	{ 0x444885a7, "_raw_spin_unlock_irqrestore" },
	{ 0xe98a2697, "misc_register" },
	{ 0xd272d446, "__x86_return_thunk" },
	{ 0x092a35a2, "_copy_to_user" },
	{ 0x7bc2c7ea, "kobject_create_and_add" },
	{ 0x7a6661ca, "ktime_get_real_seconds" },
	{ 0x955c7048, "kobject_put" },
	{ 0x155e60e3, "misc_deregister" },
	{ 0x092a35a2, "_copy_from_user" },
	{ 0xd08a1472, "sysfs_create_file_ns" },
	{ 0x40a621c5, "scnprintf" },
	{ 0xe9196a28, "module_layout" },
};

static const u32 ____version_ext_crcs[]
__used __section("__version_ext_crcs") = {
	0x95ac83d3,
	0x11f4259a,
	0xd272d446,
	0xe8213e80,
	0xbd03ed67,
	0xd272d446,
	0x9e3ce042,
	0x2ed01892,
	0xc8167060,
	0x402db74e,
	0x444885a7,
	0xe98a2697,
	0xd272d446,
	0x092a35a2,
	0x7bc2c7ea,
	0x7a6661ca,
	0x955c7048,
	0x155e60e3,
	0x092a35a2,
	0xd08a1472,
	0x40a621c5,
	0xe9196a28,
};
static const char ____version_ext_names[]
__used __section("__version_ext_names") =
	"kernel_kobj\0"
	"_raw_spin_lock_irqsave\0"
	"__fentry__\0"
	"_printk\0"
	"__ref_stack_chk_guard\0"
	"__stack_chk_fail\0"
	"sysfs_remove_file_ns\0"
	"compat_ptr_ioctl\0"
	"noop_llseek\0"
	"memcmp\0"
	"_raw_spin_unlock_irqrestore\0"
	"misc_register\0"
	"__x86_return_thunk\0"
	"_copy_to_user\0"
	"kobject_create_and_add\0"
	"ktime_get_real_seconds\0"
	"kobject_put\0"
	"misc_deregister\0"
	"_copy_from_user\0"
	"sysfs_create_file_ns\0"
	"scnprintf\0"
	"module_layout\0"
;

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "CB06A13212215A0402CF2E9");
