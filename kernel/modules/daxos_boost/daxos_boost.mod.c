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
	{ 0x2352b148, "timer_delete_sync" },
	{ 0x11f4259a, "_raw_spin_lock_irqsave" },
	{ 0xd272d446, "__fentry__" },
	{ 0xe8213e80, "_printk" },
	{ 0xbd03ed67, "__ref_stack_chk_guard" },
	{ 0xd272d446, "__stack_chk_fail" },
	{ 0x90a48d82, "__ubsan_handle_out_of_bounds" },
	{ 0x2ed01892, "compat_ptr_ioctl" },
	{ 0x32feeafc, "mod_timer" },
	{ 0xc8167060, "noop_llseek" },
	{ 0xc5c2a6a3, "const_current_task" },
	{ 0x444885a7, "_raw_spin_unlock_irqrestore" },
	{ 0x165c9585, "proc_mkdir" },
	{ 0xe98a2697, "misc_register" },
	{ 0xd272d446, "__x86_return_thunk" },
	{ 0x092a35a2, "_copy_to_user" },
	{ 0x058c185a, "jiffies" },
	{ 0xe290afe8, "seq_read" },
	{ 0x26772f20, "remove_proc_entry" },
	{ 0x5fe49b2b, "seq_printf" },
	{ 0x6f7437b5, "single_release" },
	{ 0x02f9bbf0, "timer_init_key" },
	{ 0xc714db12, "single_open" },
	{ 0x155e60e3, "misc_deregister" },
	{ 0x092a35a2, "_copy_from_user" },
	{ 0xdef8136e, "proc_create" },
	{ 0xce9b2870, "seq_lseek" },
	{ 0xe9196a28, "module_layout" },
};

static const u32 ____version_ext_crcs[]
__used __section("__version_ext_crcs") = {
	0x2352b148,
	0x11f4259a,
	0xd272d446,
	0xe8213e80,
	0xbd03ed67,
	0xd272d446,
	0x90a48d82,
	0x2ed01892,
	0x32feeafc,
	0xc8167060,
	0xc5c2a6a3,
	0x444885a7,
	0x165c9585,
	0xe98a2697,
	0xd272d446,
	0x092a35a2,
	0x058c185a,
	0xe290afe8,
	0x26772f20,
	0x5fe49b2b,
	0x6f7437b5,
	0x02f9bbf0,
	0xc714db12,
	0x155e60e3,
	0x092a35a2,
	0xdef8136e,
	0xce9b2870,
	0xe9196a28,
};
static const char ____version_ext_names[]
__used __section("__version_ext_names") =
	"timer_delete_sync\0"
	"_raw_spin_lock_irqsave\0"
	"__fentry__\0"
	"_printk\0"
	"__ref_stack_chk_guard\0"
	"__stack_chk_fail\0"
	"__ubsan_handle_out_of_bounds\0"
	"compat_ptr_ioctl\0"
	"mod_timer\0"
	"noop_llseek\0"
	"const_current_task\0"
	"_raw_spin_unlock_irqrestore\0"
	"proc_mkdir\0"
	"misc_register\0"
	"__x86_return_thunk\0"
	"_copy_to_user\0"
	"jiffies\0"
	"seq_read\0"
	"remove_proc_entry\0"
	"seq_printf\0"
	"single_release\0"
	"timer_init_key\0"
	"single_open\0"
	"misc_deregister\0"
	"_copy_from_user\0"
	"proc_create\0"
	"seq_lseek\0"
	"module_layout\0"
;

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "3882DB4F53CD29B40EE7572");
