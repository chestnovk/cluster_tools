#!/usr/bin/python3
import subprocess
from generators import generate_cmdline

# Need to make it works
class Vm:


    def __init__(self, options):
        self.options = options
        self.cmdline = generate_cmdline(**self.options)
    # define
    # create
    # configure
    # start
    # remove


# Rewrite call to run and handle exceptions
# The best choise is to use Dispatcher and Libvirtd
def define_vm(domainxml):
    # This executes virsh define <domainxml>
    subprocess.call(["virsh", "define", domainxml], stdout=False)


# Rewrite to subprocess.run()
def create_vm(vm_name, description):
    # Create the VM
    subprocess.call([
        "prlctl", "create", vm_name,
        "--vmtype", "vm",
        "--distribution", "vzlinux7"
        ], stdout=False)
    # Add some description
    subprocess.call([
        "prlctl", "set", vm_name,
        "--description", description
        ], stdout=False)
    # Disable filtering
    subprocess.call([
        "prlctl", "set", vm_name,
        "--device-set", "net0",
        "--ipfilter", "no",
        "--macfilter", "no",
        "--preventpromisc", "no"
        ], stdout=False)

    # Add VNC config
    subprocess.call([
        "prlctl", "set", vm_name,
        "--vnc-mode", "auto"
        ], stdout=False)

    # Attach cdrom
    subprocess.call([
        "prlctl", "set", vm_name,
        "--device-set", "cdrom0",
        "--connect",
        "--image", iso
        ], stdout=False)

    # Enable support of  nested virt
    subprocess.call([
        "prlctl", "set", vm_name,
        "--nested-virt", "on"
        ], stdout=False)


def start(vm_name):
    # It starts the VM
        subprocess.call(["prlctl", "start", vm_name], stdout=False)


def remove(vm_name):
        subprocess.call(["prlctl", "stop", vm_name, "--force"], stdout=False)
        subprocess.call(["prlctl", "delete", vm_name, "--force"], stdout=False)


def main():
    # Simple main
    pass


if __name__ == "__main__":
    main()

