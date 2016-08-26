title: Setting up NAT networking in Xen using virsh

# Setting up NAT networking in Xen using virsh

There are two main ways to set up networking in Xen. You can use a bridged network, or you can set up NAT. A bridged network means that the guest domains will talk to the router directly to get an IP address. NAT networking creates a subnet local to your machine, and the guest domains will talk to dom0 to get an IP address.

Neither one is better than the other, really. Bridged networking is slightly simpler if you want something that just works. NAT-ing will create an internal network that allows for simpler local (domain-to-domain) communication and greater control over external communication. The downside is that you'll need to set up a static IP per guest and set iptables rules to allow for external communication.

## Installing virsh
Install libvirt:
	[code:bash]sudo apt-get install libvirt-bin libvirt0[/code]
Check that it's been installed, and that the default network is in place:
	virsh net-list --all

## Set static IP, associate each IP with a mac address
Edit the default virsh config:
	[code:bash]sudo virsh net-edit default[/code]
Under the <dhcp> tag, add a listing for each guest. The name can be whatever you want it to be.
For the MAC address, the first 3 bytes should not be changed, this is the [OUI](https://en.wikipedia.org/wiki/Organizationally_unique_identifier) assigned to the Xen project. The last 3 can be whatever you like.
This is my DHCP configuration, with three guest domains configured:
[code:xml]
<dhcp>
	<range start='192.168.122.128' end='192.168.122.254'/>
	<host mac='00:16:3e:00:00:02' name='osv' ip='192.168.122.2'/>
	<host mac='00:16:3e:00:00:03' name='ubuntu' ip='192.168.122.3'/>
	<host mac='00:16:3e:00:00:04' name='rumprun' ip='192.168.122.4'/>
</dhcp>
[/code]

## Setting up a guest domain with NAT
### standard xen cfg
In your Xen guest configuration file, add the following virtual interface, where mac corrosponds with the virsh configuration:
	[code:python]vif = ['mac=00:16:3e:00:00:03,bridge=virbr0'][/code]
### rumprun unikernel
The rumprun unikernel is launched with the rumprun script. Here "newnet" is used internally by the script and can be set to whatever you like. rumprun_image.bin represents the baked rumprun binary you are running:
	[code:bash]rumprun -S xen -id -I newnet,xenif,'bridge=virbr0,mac=00:16:3e:00:00:04' -W newnet,inet,dhcp rumprun_image.bin0[/code]
