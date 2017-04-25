#!/bin/sh

cid="$(cat /sys/class/mmc_host/mmc0/mmc0\:0001/cid)"

echo default-on > '/sys/class/leds/green_led/trigger'
echo default-on > '/sys/class/leds/red_led/trigger'

wait_ejection() {
    while [ -b /dev/mmcblk0 ]; do sleep 0.01; done
}

wait_insertion() {
    while [ ! -b /dev/mmcblk0 ]; do sleep 0.01; done
}

set_red_led() {
    echo $1 > '/sys/class/leds/red_led/brightness'
}

set_green_led() {
    echo $1 > '/sys/class/leds/green_led/brightness'
}

blink_green_led() {
    set_green_led 0
    sleep 0.2
    for i in `seq $1`; do
      set_green_led 1
      sleep 0.2
      set_green_led 0
      sleep 0.2
    done
}

smart_wait_insertion() {
    local cnt=0
    while true; do
     if [ $cnt -eq 0 ]; then
      blink_green_led $1
      cnt=0
     fi
     if [ ! -b /dev/mmcblk0 ]; then
      sleep 0.01;
     else
      break
     fi
     cnt=$(((cnt+1)%100))
    done
}

indicate_failure() {
 set_green_led 0
 set_red_led 1
 sleep 2
}

indicate_success() {
 set_green_led 1
 set_red_led 0
 sleep 2
}

cid="$(cat /sys/class/mmc_host/mmc0/mmc0\:0001/cid)"

cnt=1
while true; do
 set_red_led 1
 set_green_led 1
 wait_ejection
 set_green_led 0
 set_red_led 0
 smart_wait_insertion $cnt
 new_cid="$(cat /sys/class/mmc_host/mmc0/mmc0\:0001/cid)"
 if [ x$cid == x$new_cid ]; then
  cnt=$((cnt%6+1))
  echo equal $cnt
 else
  echo not equal $cid $new_cid $cnt
  set_red_led 0
  set_green_led 0

  mkdir /mnt
  mount /dev/mmcblk0p1 /mnt/
  if [ "$?" != "0" ]; then
   indicate_failure
   continue
  fi

  name=""
  case $cnt in
    1) name="capter" ;;
    2) name="fooddispenser" ;;
    3) name="redbutton" ;;
    4) name="settings" ;;
    5) name="stargate" ;;
    6) name="xxx" ;;
  esac
  echo $name
  sed -e "s/emptyservice/$name/" /dhclient.conf > /mnt/etc/dhcp/dhclient.conf
  if [ "$?" != "0" ]; then
   umount -lf /mnt
   indicate_failure
   continue
  fi
  umount -lf /mnt
  if [ "$?" != "0" ]; then
   indicate_failure
   continue
  fi
  sync
  indicate_success
 fi
done
