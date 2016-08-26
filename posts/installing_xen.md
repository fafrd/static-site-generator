title: Setting up Xen in Ubuntu 16.04

# Setting up Xen in Ubuntu 16.04

Xen is the future, you guys. While KVM has very good support and widespread use, the fact that it exists as a Linux kernel module means it runs as basically another process under linux, with all of the scheduling issues and limitations that come along with being a process. Xen works by "pinning" the host and guest operating systems to specific cores, allowing for much greater separation of guests. In Xen, the guest is running alongside the host, instead of under it. The host, aka "dom0", sits meekly alongside with the permissions to administer guests.

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

*More information on using LVM: [tldp.org/HOWTO/LVM-HOWTO](http://tldp.org/HOWTO/LVM-HOWTO/)*

## Making a config file
There are a lot of options that go into making a xen cfg file. Below is provided a basic config with some explanations, but google around as needed to get a better understanding.

### PV or HVM?
There are two ways to run Xen: HVM or PV mode. HVM stands for Hardware Virtualization Mode, and PV stands for Paravirtualized. Traditionally, HVM provided more efficient emulation, as it gave the guest more direct access to hardware; paravirtualization provides a "paravirtualized" interface for the guest to run on, and requires the guest have paravirtualized driver support. Recently, better paravirtualized driver support in Linux and better interaction between Xen and hardware virtualization has led to paravirtualized mode actually being the better option over HVM. (Interestingly, one of the biggest places PV shines over HVM is in page table and TLB virtualization; see [wiki.xen.org/wiki/X86_Paravirtualised_Memory_Management](https://wiki.xen.org/wiki/X86_Paravirtualised_Memory_Management)).

### sample xen.cfg
*I recommend you follow [this guide](https://help.ubuntu.com/community/Xen) on how to set up a new Ubuntu guest using their bootloader code. If you already have a prepared disk image, skip the kernel and ramdisk images and go ahead and uncomment bootloader.*

*tsc_mode is something complicated to do with the emulation of x86 timer instructions. read more here: [xenbits.xen.org/docs/4.3-testing/misc/tscmode.txt](https://xenbits.xen.org/docs/4.3-testing/misc/tscmode.txt)*

[code:python]
name = "example ubuntu guest"
# memory in megabytes
memory = 2048
# number of cpus, which cpus this guest is pinned to
vcpus = 4
cpus = "5-8"

tsc_mode = "native"

kernel = "/var/lib/xen/images/ubuntu-netboot/trusty14LTS/vmlinuz"
ramdisk = "/var/lib/xen/images/ubuntu-netboot/trusty14LTS/initrd.gz"
#bootloader = "/usr/lib/xen-4.4/bin/pygrub"

disk = ['/dev/pcp-d-15-vg/xen_1,raw,xvda,rw']

# see my xen networking article for info on how to set up networking: [/setting-up-nat-networking-in-xen-using-virsh.html](setting-up-nat-networking-in-xen-using-virsh.html)
[/code]

## Starting up Xen
The Xen control program is called xl. Given config file "xen.cfg", start up a guest domain like
	[code:bash]sudo xl create xen.cfg[/code]

If it works, it will have started in the background and you will need to attach to the guest's console in order to control it. 
First you'll need the guest domains' id (domid). List domain IDs by typing
	[code:bash]sudo xl list[/code]
Attach to the console by typing
	[code:bash]sudo xl console DOMID[/code]
You can then detach from this console with the hotkey ctrl-] (control and left bracket).

A domain can then be shut down by issuing a instructing the guest operating system to shutdown (e.g. the Linux shutdown command), or using xl.
Gracefully request an OS shutdown with the command
	[code:bash]sudo xl shutdown DOMID[/code]
Force an immediate shutdown with
	[code:bash]sudo xl destroy DOMID[/code]
