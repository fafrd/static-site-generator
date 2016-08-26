title: Setting up Xen in Ubuntu 16.04

# Setting up Xen in Ubuntu 16.04

Xen is the future, you guys. Death to KVM.

## Install the Xen hypervisor
	[code:bash]sudo apt-get install xen-hypervisor-amd64[/code]
Change Ubuntu's grub bootloader to customize how Xen boots. The following gives Xen dom0 1 cpu, "pins" it (cpu assigned to dom0 won't change), and gives 4gb memory.
	[code:bash]sudo vim /etc/default/grub[/code]
add the following line:
	[code:python]GRUB_CMDLINE_XEN_DEFAULT="dom0_max_vcpus=1 dom0_cpus_pin dom0_mem=4G,max:4G"[/code]
update grub:
	[code:bash]sudo update-grub[/code]

## Create a disk for use with Xen
This can be done in several different ways. Here I use LVM to create a new logical volume.

Basically, you'll figure out what the name of your existing *volume group* is, then add another *logical volume* into that.
List volume groups with
	[code:bash]sudo vgs[/code]
Mine is called *pcp-d-15-vg*. I create a 16gb logical volume with the name *xen_1*:
	[code:bash]lvcreate -L 16G pcp-d-15-vg -n xen_1[/code]

More information on using LVM: [tldp.org/HOWTO/LVM-HOWTO](http://tldp.org/HOWTO/LVM-HOWTO/)
