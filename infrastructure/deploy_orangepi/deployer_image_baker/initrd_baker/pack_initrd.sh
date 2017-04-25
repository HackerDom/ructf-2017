#!/bin/sh

MY_NAME="`readlink -f "$0"`"
MY_DIR="`dirname "$MY_NAME"`"
cd "${MY_DIR}"

cd initrd_root
find | cpio -H newc -o > ../initrd.new
cd ..
gzip initrd.new
mkimage -A arm -T ramdisk -C none -n uInitrd -d initrd.new.gz uInitrd.new
