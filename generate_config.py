#!/usr/bin/python3
import json
import os
from generators import generate_timestamp, generate_private_ip, generate_cmdline
from os_tools import mount, umount
from vm_tools import Vm


# Temp name
def generate_config(json_config):

    # Create an array to store VMs:
    vms = []

    with open(json_config) as f:
        config = json.load(f)
        i = 1
        for vm_public_ip in config['cluster']['public_net']['ips']:
            # the name_generator should be better.
            options = {}
            options['iso_name'] = config['general']['iso']
            options['hostname'] = generate_timestamp(config['cluster']['name']) + "-" + str(i)
            options['public_ip'] = vm_public_ip
            options['public_mask'] = config['cluster']['public_net']['mask']
            options['public_gw'] = config['cluster']['public_net']['gw']
            options['public_dns'] = config['cluster']['public_net']['dns']
            options['ks_device'] = config['general']['ks_device']
            options['ks'] = config['general']['ks']

            if config['cluster']['private_net']['create'] == "True":
                options['private_ip'] = generate_private_ip(vm_public_ip)
                options['private_mask'] = config['cluster']['private_net']['mask']

            # Try to create management containers
            # Final decision is made by a kickstart file
            # Depends on given cmdline options
            # In case of troubles check cat /proc/cmdline
            # From anaconda and compare with kickstart
            if i == 1:
                options['includes_va'] = True
                options['va_ip'] = config['va']['ip']
                options['includes_storage_ui'] = True
                options['storage_ui_ip'] = config['storage_ui']['ip']
            # In case there is no such values left blank
            else:
                options['va_ip'] = config['va']['ip']
                options['storage_ui_ip'] = config['storage_ui']['ip']
                options['storage_ui_token'] = config['storage_ui']['token']
            vm = Vm(options)
            vms.append(vm)
            i += 1

    return vms


def main():

    mount(config['general']['iso'],
          os.path.join(config['general']['workdir'],"mounts",)

    vms = generate_config("/home/kchestnov/PycharmProjects/clusterTools/cluster_config.json")
    for vm in vms:
        print(vm.options)
        print(vm.cmdline)




if __name__ == "__main__":
    main()
