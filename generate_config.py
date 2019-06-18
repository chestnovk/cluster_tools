#!/usr/bin/python3
import os
import generators
from os_tools_class import IsoTools
from vm_tools import Vm



def main():

    # Obtain all the parameters from json. It will generate a list of Vm objects + array of general options
    # general option are to be used for mount iso, for example.
    vms, general_options = generators.generate_config("/home/kchestnov/Python/cluster_tools/cluster_tools/cluster_config.json")

    # I should mount iso only after I know that vms were created.
    iso = IsoTools(general_options['iso'], os.path.join(general_options['workdir'], "mounts"))
    iso.mount()

    for vm in vms:
        print(vm.options)
        print(vm.cmdline)

        # The VM must be created as well as dumpxml.
        # vm.define
        # vm.start
        # vm.wait
        # vm.define
        # vm.start


    # After all of the VM have been created, umount ISO
    iso.umount()


if __name__ == "__main__":
    main()
