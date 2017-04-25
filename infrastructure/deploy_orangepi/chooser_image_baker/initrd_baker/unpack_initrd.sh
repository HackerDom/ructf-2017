#!/bin/sh

MY_NAME="`readlink -f "$0"`"
MY_DIR="`dirname "$MY_NAME"`"
cd "${MY_DIR}"

dd if=uInitrd of=initrd.gz bs=64 skip=1
gunzip initrd.gz
mkdir -p initrd_root
cd initrd_root
cpio -i < ../initrd
