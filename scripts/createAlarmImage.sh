#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo 'This script must be run as root'
    exit 1
fi

if [ $# -lt 2 ]; then
    echo $'usage: alarm.sh \'<SSID>\' \'<Passphrase>\''
    exit 1
fi

BOOT_PARTITION_SIZE_MB=100
SECTOR_SIZE=512
START_SECTOR=2048
FIRST_OFFSET=$(expr $SECTOR_SIZE \* $START_SECTOR)
SECOND_OFFSET=$(expr $BOOT_PARTITION_SIZE_MB \* 1024 \* 1024 + $FIRST_OFFSET)

apt update
apt install -y libarchive-tools wpasupplicant dosfstools wget

fallocate -l 2G sdcard.img

fdisk sdcard.img <<EOF
o
n
p
1

+100M
t
c
n
p
2


w
EOF

losetup -o $FIRST_OFFSET --sizelimit ${BOOT_PARTITION_SIZE_MB}M loop0 sdcard.img
losetup -o $SECOND_OFFSET loop1 sdcard.img

mkfs.vfat /dev/loop0
mkfs.ext4 /dev/loop1

cd /mnt
mkdir boot root
mount /dev/loop0 boot
mount /dev/loop1 root

wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-latest.tar.gz
bsdtar -xpf ArchLinuxARM-rpi-latest.tar.gz -C root
sync
mv root/boot/* boot

# Download setup script
curl -o root/home/alarm/setup.sh https://raw.githubusercontent.com/mlowijs/teslacam_py/master/scripts/setup.sh

rm ArchLinuxARM-rpi-latest.tar.gz

cat << EOF >> root/etc/systemd/network/wlan0.network
[Match]
Name=wlan0

[Network]
DHCP=yes
EOF

wpa_passphrase $1 $2 > root/etc/wpa_supplicant/wpa_supplicant-wlan0.conf
ln -sr root/usr/lib/systemd/system/wpa_supplicant\@.service root/etc/systemd/system/multi-user.target.wants/wpa_supplicant\@wlan0.service

umount boot root
rm -rf root boot
losetup -d /dev/loop0
losetup -d /dev/loop1

cp sdcard.img /tmp
