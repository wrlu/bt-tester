#! /bin/bash
adb push android_6_0_1_nexus5/bluetooth.default.so /sdcard/bluetooth.default.so
adb shell 'su -c "mount -o remount,rw /system"'
adb shell 'su -c "cp /sdcard/bluetooth.default.so /system/lib/hw/bluetooth.default.so"'
adb shell 'su -c "chmod 644 /system/lib/hw/bluetooth.default.so"'
adb shell 'su -c "chown root:root /system/lib/hw/bluetooth.default.so"'