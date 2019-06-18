#!/usr/bin/python3
import sys
import subprocess
import os

# Probably I can do it in a less number of rows


class IsoTools:

    def __init__(self, iso_path, workdir):

        if not os.path.isfile(iso_path) and not os.path.isdir(workdir):
            sys.exit("Please specify correct ISO or workdir")

        self.name = os.path.splitext(os.path.basename(iso_path))[0]
        self.iso_path = iso_path
        self.mount_dir = os.path.join(workdir, os.path.splitext(os.path.basename(iso_path))[0])
        if not os.path.isdir(self.mount_dir):
            try:
                os.mkdir(self.mount_dir)
            except OSError as err:
                sys.exit("Cannot create \"{}\". Error: {}".format (self.mount_dir, err.strerror))
        self.vmlinuz = os.path.join(self.mount_dir, "images/pxeboot/vmlinuz")
        self.initrd = os.path.join(self.mount_dir, "images/pxeboot/initrd.img")

    def mount(self):
        try:
            subprocess.run(["sudo", "mount", "-o", "ro", self.iso_path, self.mount_dir], check=True, stderr=True)
            return self.mount_dir
        except subprocess.CalledProcessError as err:
            sys.exit("Cannot mount the {} to the {}. Error: {}".format (self.iso_path, self.mount_dir, err.returncode))

    def umount(self):
        try:
            subprocess.run(["sudo", "umount", self.mount_dir], check=True)
        except subprocess.CalledProcessError as err:
            sys.exit("Cannot umount the {}".format(self.mount_dir, err.returncode))

    def get_vmlinuz(self):
        if not os.path.isfile(self.vmlinuz):
            sys.exit("Cannot find {} in a {}".format(self.vmlinuz, self.mount_dir))
        else:
            return self.vmlinuz

    def get_initrd(self):
        if not os.path.isfile(self.initrd):
            sys.exit("Cannot find {} in a {}".format(self.initrd, self.mount_dir))
        else:
            return self.initrd


def main():
    IsoTools_v = IsoTools("/home/kchestnov/Downloads/vz-platform-2.5.0-1642-1642.iso", "")
    IsoTools_v.mount()
    IsoTools_v.get_initrd()
    IsoTools_v.get_vmlinuz()
    IsoTools_v.umount()


if __name__ == "__main__":
    main()