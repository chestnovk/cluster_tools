#!/usr/bin/python3
import subprocess


# Need to make it works
class Vm:

    def __init__(self, options, cmdline):
        self.options = options
        self.cmdline = cmdline

    def create_vm(self):
        name = self.options['name']
        # Need to find a way how to define description
        description = ""
        iso = self.options['iso_name']

        subprocess.call(["prlctl", "create", name,
                          "--vmtype", "vm",
                          "--distribution", "vzlinux7"]
                         , stdout=False)

        subprocess.call(["prlctl", "set", name,
                          "--description", description]
                         , stdout=False)

        subprocess.call(["prlctl", "set", name,
                          "--device-set", "net0",
                          "--ipfilter", "no",
                          "--macfilter", "no",
                          "--preventpromisc", "no"]
                         , stdout=False)

        subprocess.call(["prlctl", "set", name,
                          "--vnc-mode", "auto"]
                         , stdout=False)

        subprocess.call(["prlctl", "set", name,
                          "--device-set", "cdrom0",
                          "--connect", "--image", iso]
                         , stdout=False)

        # Enable support of  nested virt
        subprocess.call(["prlctl", "set", name,
                          "--nested-virt", "on"]
                         , stdout=False)
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



def generate_dumpxml(workdir, vm_name, vmlinuz, initrd, commandline):

    domainxml = os.path.join(workdir, "configs", vm_name)
    domainxml_tmp = domainxml + "_tmp"

    with open(domainxml, 'w') as file:
        subprocess.call(["virsh", "dumpxml", vm_name], stdout=file)

    with open(domainxml) as file:
        tmp = file.readlines()

        for index, line in enumerate(tmp):
            if "<qemu:commandline>" in line:
                # Need to rewrite for XML
                # This is not cool at all
                tmp.insert(index + 1,"    <qemu:arg value='{}'/>\n".format(vmlinuz))
                tmp.insert(index + 1,"    <qemu:arg value='-kernel'/>\n")
                tmp.insert(index + 1,"    <qemu:arg value='{}'/>\n".format(initrd))
                tmp.insert(index + 1,"    <qemu:arg value='-initrd'/>\n")
                tmp.insert(index + 1,"    <qemu:arg value='{}'/>\n".format(commandline))
                tmp.insert(index + 1,"    <qemu:arg value='-append'/>\n")

        with open(domainxml_tmp, 'w') as file:
            for line in tmp:
                file.write(line)

        return domainxml_tmp


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

