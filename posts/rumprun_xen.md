title: Running rumprun for Xen in Ubuntu 16.04

# Running rumprun for Xen in Ubuntu 16.04

Running rumprun under Xen isn't hard, but it's less documented than running it under KVM. This page is similar to [Rumprun's guide to building rumprun unikernels](https://github.com/rumpkernel/wiki/wiki/Tutorial:-Building-Rumprun-Unikernels) with a few Xen-specific changes.

## Build the rumprun platform
Install prerequisite xen headers and build tools:
	[code:bash]sudo apt-get install build-essential libxen-dev[/code]
Clone their repo, cd, build:
	[code:bash]
	git clone http://repo.rumpkernel.org/rumprun
	cd rumprun
	git submodule update --init
	CC=cc ./build-rr.sh xen
	[/code]

## Add binaries to PATH
You've now build rumprun and the binaries necessary for building, baking, running are located in rumprun/bin. You'll want to these to your [PATH variable](https://en.wikipedia.org/wiki/PATH_(variable)) for convenient access:
	[code:bash]export PATH="${PATH}:$(pwd)/rumprun/bin"[/code]
You can also add this to your ~/.bashrc to make these changes permanent.
	[code:bash]vim ~/.bashrc[/code]
Append the following, where [location of rumprun] represents the directory containing rumprun:
	[code:bash]export PATH="$PATH:[location of rumprun]/rumprun/bin"[/code]

## Building applications
Get some source code and use rumprun's version of gcc to compile it. (Follow the [rumprun tutorial](https://github.com/rumpkernel/wiki/wiki/Tutorial:-Building-Rumprun-Unikernels) for a more thorough explanation...)
Here, helloer.c is our source code and helloer-rumprun is the output binary.
	[code:bash]x86_64-rumprun-netbsd-gcc -o helloer-rumprun helloer.c[/code]

## Baking applications
I was going to make a joke here but I can't think of anything clever right now. You need to bake it. That means running a command to add in all the kernel-y bits that makes rumprun ready for it.
Here, helloer-rumprun is the binary we just built and helloer-rumprun.bin is the the binary with the necessary rumprun pieces.
	[code:bash]rumprun-bake xen_pv helloer-rumprun.bin helloer-rumprun[/code]

## Running applications
Here's the hard part. The rumprun command is a script that will create a Xen configuration file in /tmp and start up a Xen PV guest. For xen, it will look like this:
	[code:bash]rumprun -S xen -id -g [Xen config options] -I [network interface] -W [more network options][/code]
The -I and -W commands can be omitted if there is no need for networking. I have networking set up using a NAT, in which there exists a subnet local to the machine. Look at my [article on Xen networking](/setting-up-nat-networking-in-xen-using-virsh.html) to see how I set up networking within rumprun.
