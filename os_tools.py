#!/usr/bin/python3
import sys
import subprocess
import os

# Mount tool assumes that you make precheck if ISO exists and mount dir is created before calling.
# Otherwise it exits.
# Probably I can do it in a less number of rows

def get_mount_dir_name(iso_path, workdir):
    mount_dir_name = os.path.join(workdir, os.path.splitext(os.path.basename(iso_path))[0])
    return mount_dir_name


def create_mount_dir(iso_path, workdir):
    mount_dir = get_mount_dir_name(iso_path, workdir)
    if not os.path.isdir(mount_dir):
        os.mkdir(mount_dir)
    return mount_dir


def mount(iso_path, workdir):
    mount_dir = create_mount_dir(iso_path, workdir)
    try:
        subprocess.run(["sudo", "mount", "-o", "loop", iso_path, mount_dir],
                       check=True, stderr=True)
        return mount_dir
    except subprocess.CalledProcessError as err:
        sys.exit("Cannot mount the {} to the {}. Error: {}".format(iso_path, mount_dir, err.returncode))


def umount(mount_dir):

    try:
        subprocess.run(["sudo", "umount", mount_dir],
                       check=True)
    except subprocess.CalledProcessError as err:
        sys.exit("Cannot umount the {}".format(mount_dir, err.returncode))


def get_vmlinuz(mount_dir):
    vmlinuz = os.path.join(mount_dir, "images/pxeboot/vmlinuz")
    if not os.path.isfile(vmlinuz):
        sys.exit("Cannot find {} in a {}".format(vmlinuz, mount_dir))
    else:
        return vmlinuz


def get_initrd(mount_dir):
    initrd = os.path.join(mount_dir, "images/pxeboot/initrd.img")
    if not os.path.isfile(initrd):
        sys.exit("Cannot find {} in a {}".format(initrd, mount_dir))
    else:
        return initrd


# Check if mount success if there is no ISO
def test1():
    iso_path = ""
    workdir = "/tmp/mount"
    mount(iso_path, workdir)
    umount(iso_path, workdir)
    return "Passed"


# Check if mount success if there is no mount_dir
def test2():
    iso_path = "/home/kchestnov/ISO/CentOS-7-x86_64-Minimal-1810.iso"
    workdir = "/temp/nosuchdir"
    mount(iso_path, workdir)
    umount(iso_path, workdir)
    return "Passed"


# Check if mount success if there is already mounted ISO
def test3():
    iso_path = "/home/kchestnov/ISO/CentOS-7-x86_64-Minimal-1810.iso"
    workdir = "/tmp/mount"
    mountdir = mount(iso_path, workdir)
    mountdir = mount(iso_path, workdir)
    umount(mountdir)
    return "Passed"

def test4():
    iso_path = "/home/kchestnov/ISO/CentOS-7-x86_64-Minimal-1810.iso"
    workdir = "/tmp/mount"
    mount_dir = mount(iso_path, workdir)
    print(get_initrd(mount_dir))
    print(get_vmlinuz(mount_dir))
    umount(mount_dir)
    return "Passed"


def main():
    #print(test1())
    #print(test2())
    print(test4())


if __name__ == "__main__":
    main()
