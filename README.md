# raspberrypi-python-still-camera
Simple server to host still from a Raspberry Pi

Current resolution only works with camera module v2.

Also make sure you have enough GPU-memory allocated.
For RPi 3 the default value should be fine, but for RPi Zero (and Zero W) you probably have to increase the memory allocated for GPU to 192MB.
Edit /boot/config.txt and make sure gpu_mem have the correct value.
