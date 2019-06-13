#!/usr/bin/python3
import datetime

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

def test_1():

    options = {'hostname': "kchestnov",
            'iso_name': "cloud_linux.iso",
            'public_ip': "172.16.56.80",
            'public_mask': "255.255.252.0",
            'public_gw': "172.16.56.1",
            'public_dns': "10.30.0.27",
            'ks_device': "eth0",
            'ks': "http://172.16.56.80/ks/cluster_config.cfg",
            'private_ip': "",
            'private_mask': "255.255.255.0",
            'includes_va': False,
            'va_register': False,
            'va_ip': "",
            'includes_storage_ui': False,
            'storage_ui_register': False,
            'storage_ui_ip': "",
            'storage_ui_token': ""}

    print(generate_cmdline(**options))


def main():
    test_1()


if __name__ == "__main__":
    main()
