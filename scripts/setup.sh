#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo 'This script must be run as root'
    exit 1
fi

if [ $# -lt 1 ]; then
    echo $'usage: setup.sh <Partition_size_GB>'
    exit 1
fi

# Fix root mount pount
echo "/dev/mmcblk0p2 / ext4 defaults,rw,noatime 0 1" >> /etc/fstab

# Update and install some packages
pacman-key --init
pacman-key --populate archlinuxarm
pacman -Syu --noconfirm
pacman -S --noconfirm dosfstools sudo python python-pip base-devel

# Setup time zone and hostname
ln -sf /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime

hostnamectl set-hostname teslacam
echo "127.0.0.1 localhost teslacam" > /etc/hosts
echo "::1 localhost teslacam" >> /etc/hosts

# Setup sudo
echo "%wheel ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers

# Resize root partition
fdisk /dev/mmcblk0 <<EOF
d
2
n
p
2


n
w
EOF

resize2fs /dev/mmcblk0p2

# Setup USB filesystem
fallocate -l $1G /usbfs

fdisk /usbfs <<EOF
o
n
p
1
2048

t
c
w
q
EOF

losetup -o 1048576 loop0 /usbfs
mkdosfs /dev/loop0 -F 32 -n TESLACAM
losetup -d /dev/loop0

# Create mountpoint and TeslaCam folder
mkdir -p /mnt/usbfs
echo "/usbfs /mnt/usbfs vfat loop,offset=1048576,rw,user,errors=continue 0 0" >> /etc/fstab

mount /mnt/usbfs
mkdir -p /mnt/usbfs/TeslaCam
umount /mnt/usbfs

# Setup USB driver
echo "dtoverlay=dwc2" >> /boot/config.txt
echo "dwc2" >> /etc/modules-load.d/raspberrypi.conf

# Set module options
echo "options g_mass_storage file=/usbfs removable=1 stall=0 iSerialNumber=123456" > /etc/modprobe.d/g_mass_storage.conf
echo "g_mass_storage" >> /etc/modules-load.d/raspberrypi.conf

# Install TeslaCam software
pip install teslacam-py

# Install systemd service
cat << EOF >> /etc/systemd/system/teslacam.service
[Unit]
Description=TeslaCam
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/teslacam

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable teslacam

reboot
