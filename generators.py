#!/usr/bin/python3
import datetime
import json
from vm_tools import Vm


def generate_cmdline(**kwargs):

    cmdline = ""

    def append(key, value):
        nonlocal cmdline
        cmdline += (" " + key + "=" + value)

    for k, v in kwargs.items():
        if k == "iso_name":
            append("inst.stage2=hd:LABEL", v)
        elif k == "public_ip":
            append("ip", v)
            append(k, v)
        else:
            append(k, str(v))

    return cmdline


def generate_private_ip(ip):
    # I will extend it for any subnet
    return "192.168.100." + ip[-3:]


def generate_timestamp(base):
    now = datetime.datetime.now()
    name = base + "-" + now.strftime("%Y%m%d")
    return name


def generate_config(json_config):

    # Create an array to store VMs:
    vms = []

    with open(json_config) as f:
        config = json.load(f)
        i = 1
        general_options = {}
        general_options['workdir'] = config['general']['workdir']
        general_options['iso'] = config['general']['iso']
        general_options['ks'] = config['general']['ks']
        general_options['ks_device'] = config['general']['ks_device']
        general_options['name'] = config['cluster']['name']
        general_options['va'] = config['va']
        general_options['storage_ui'] = config['storage_ui']

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
            # For example if you not specify IP address
            # The kickstart will not create VA
            # Same for UI
            # Token should be obtain somehow later.
            # Actually this decision affects future cluster updates.
            # Probably I could write a value "general" "is_created"
            # So it will not be added later if additional VM should be added to
            # an existed cluster with ui

            if i == 1 and not config['general']['is_created']:
                options['includes_va'] = True
                options['va_ip'] = config['va']['ip']
                options['includes_storage_ui'] = True
                options['storage_ui_ip'] = config['storage_ui']['ip']
            # In case there is no such values left blank
            else:
                options['va_ip'] = config['va']['ip']
                options['storage_ui_ip'] = config['storage_ui']['ip']
                options['storage_ui_token'] = config['storage_ui']['token']
            vm = Vm(options, generate_cmdline(**options))
            # I probably need to check VM names and try to create a VM.
            # If it was successfully created I need to create an dumpxml right here.
            # If something goes wrong the script must be stopped.
            vms.append(vm)
            i += 1

    return vms, general_options


def main():
    pass


if __name__ == "__main__":
    main()
