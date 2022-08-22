#!/bin/bash

echo 298 > /sys/class/gpio/export #298
echo 388 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio298/direction #298
echo out > /sys/class/gpio/gpio388/direction
echo 1 > /sys/class/gpio/gpio388/active_low
/usr/bin/rs_save &>> /var/log/rs_log.txt
