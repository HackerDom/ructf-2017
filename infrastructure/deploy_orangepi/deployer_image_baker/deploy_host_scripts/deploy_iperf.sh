#!/bin/sh

blink_success() {
    times=$1

    for i in `seq $times`; do
        echo 0 > /sys/class/leds/green_led/brightness
        echo 0 > /sys/class/leds/red_led/brightness
        sleep 0.3
        echo 1 > /sys/class/leds/green_led/brightness
        echo 1 > /sys/class/leds/red_led/brightness
        sleep 0.3
    done
    sleep 1
}


blink_success 2

# net testing
umount -lf /deploy
ip address add 10.60.50.1/24 dev eth0
iperf -s &
