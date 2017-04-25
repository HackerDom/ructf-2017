#!/bin/sh
# This program flashes /ructf2017.img on microsd card
# It uses orangepi leds to indicate flashing status
# Alexander Bersenev, bay@hackerdom.ru

# trigger values: none default-on mmc0 timer heartbeat
# leds order: blue orange white green

set_red_led() {
	echo default-on > '/sys/class/leds/red_led/trigger'
	echo $1 > '/sys/class/leds/red_led/trigger'
}

set_green_led() {
	echo default-on > '/sys/class/leds/green_led/trigger'
	echo $1 > '/sys/class/leds/green_led/trigger'
}

wait_ejection() {
	while [ -b /dev/mmcblk0 ]; do sleep 0.1; done
}

wait_insertion() {
	while [ ! -b /dev/mmcblk0 ]; do sleep 0.1; done
}

flash_work() {
	set_red_led default-on
	set_green_led default-on

	wait_insertion

	set_red_led none
	set_green_led none

	sleep 1
	set_red_led default-on
	sleep 1
	set_green_led default-on
	sleep 1
	set_red_led heartbeat
	set_green_led heartbeat

	# write an image
	dd if=/deploy/ructf2017.img of=/dev/mmcblk0 bs=65536
	sync

	set_red_led default-on
	set_green_led heartbeat


	last_part_num=$(/bin/parted /dev/mmcblk0 -ms unit s p | tail -n 1 | cut -f 1 -d:)
	if [ "$last_part_num" != "1" ];then
		set_green_led none
		set_red_led default-on
		wait_ejection
		return
	fi

	part_start=$(parted /dev/mmcblk0 -ms unit s p | grep "^1" | cut -f 2 -d: | tr -d 's')
	[ "${part_start}" ] || ( set_green_led none; set_red_led default-on; wait_ejection; return )

	fdisk /dev/mmcblk0 << EOF
d
1
n
p
1
${part_start}

w
EOF
	sync

        mkdir /mnt
	mount /dev/mmcblk0p1 /mnt/
	if [ "$?" != "0" ]; then
		set_green_led none
		set_red_led default-on

		wait_ejection

		return
	fi

	umount /mnt
	umount -l /mnt

	resize2fs /dev/mmcblk0p1
	#btrfs filesystem resize max /mnt
	if [ "$?" != "0" ]; then
		set_green_led none
		set_red_led default-on

		wait_ejection

		return
	fi
	sync	
	
	set_red_led none
	set_green_led default-on

	wait_ejection
}


set_red_led timer
set_green_led timer
wait_ejection

#modprobe btrfs

while true; do
	flash_work
done
