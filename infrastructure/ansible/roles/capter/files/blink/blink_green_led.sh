#!/bin/bash

echo default-on > /sys/class/leds/green_led/trigger

blinks="$1"

while true; do
 for i in `seq "$blinks"`; do
  echo 1 > /sys/class/leds/green_led/brightness
  sleep 0.3
  echo 0 > /sys/class/leds/green_led/brightness
  sleep 0.2
 done
 sleep 1.2
done
