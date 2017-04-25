#!/bin/bash

set -e
cd "$( dirname "${BASH_SOURCE[0]}" )"

./create_firstrun_in_root.sh

echo Generating empty file
dd if=/dev/zero of=ructf2017.img bs=1M count=1500

echo Partitioning

deviceSize=$(stat -c%s ructf2017.img)
echo Device Size is ${deviceSize}
deviceCylinders=$(echo "${deviceSize} / 255 / 63 / 512" | bc)
echo Deivce Cylinders is ${deviceCylinders}

fdisk ructf2017.img << EOF
d
n
p
1


w
EOF

echo Writing loader
dd if=u-boot-sunxi-with-spl.bin of=ructf2017.img bs=1024 seek=8 conv=notrunc,nocreat

echo "Unmounting old partitions if any"
(umount root_mounted || exit 0)
sleep 1

(kpartx -d ructf2017.img || exit 0)
sleep 2

echo Mounting partitions
mappedCard=`kpartx -av ructf2017.img | grep "add map" | head -n 1 | cut -d' ' -f3`

cardp="/dev/mapper/${mappedCard:0:5}p"
cardroot=${cardp}1

echo "Cardroot is ${cardroot}, sleeping 5 secounds(some utils hold them)"
sleep 5

#mkfs.btrfs -L RUCTF2017 -O ^skinny-metadata -O ^extref ${cardroot}
mkfs.ext4 -L RUCTF2017 ${cardroot}
sleep 1

echo "Mounting root"
mount ${cardroot} root_mounted

echo "Copying root contents to partition on image"
rsync -a root/ root_mounted/

echo "All done, sleeping 2 secounds"
sleep 2
umount root_mounted

echo "Sleeping 5 secounds for unmounting"
sleep 5
kpartx -d ructf2017.img

echo "All done, the image is ructf2017.img"
