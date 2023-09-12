# Raspberry Pi *personal* notes

Bookmark: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#frequency-management-and-thermal-control

<img src=images/rpi-gpio.svg width="500">

&nbsp;

<img src=images/Shrouded_Box_Headers.png width="600">

&nbsp;

# Hardware
- R-Pi **1**, **Zero**, ZeroW, CM1
  - SoC: Broadcom BCM2835
    - CPU: ARM11 ARM1176JZF-S 32bits
      - Zero: 1GHz
    - GPU: VideoCore IV, OpenGL ES 2.0, OpenVG 1080p30 H.264 @250MHz
    - RAM
      - B+, Zero: 512 MiB
- R-Pi 2B (early models)
  - SoC: Broadcom BCM2836
    - CPU: ARM Cortex-A7 Quad-Core ARMv7 32bits
    - GPU: VideoCore IV, OpenGL ES 2.0, OpenVG 1080p30 H.264
    - RAM
- R-Pi **2**B (later models), CM3, **3**B
  - SoC: Broadcom BCM2837
    - CPU: ARM Cortex-A53 Quad-Core ARMv8 64bits
    - GPU: VideoCore IV, @400MHz
- R-Pi **3**A+, **3**B+, CM3+
  - SoC: Broadcom BCM2837B0
    - CPU: quad-core 64bit ARMv8 Cortex-A53 64bits @1.4GHz
    - GPU VideoCore IV, OpenGL ES 2.0, OpenVG 1080p60 H.264 @400MHz
    - RAM
      - 3B+: 1GiB
- R-Pi **4**B, 400, CM4
  - SoC: Broadcom BCM2711
    - CPU: ARM Cortex-A72 Quad-Core ARMv8 64bit
- R-Pi **Zero2** W
  - SiP: RP3A0 BCM2710A1 silicon die (the same inside BCM2837) 

<img src=images/bcm2835.png width="1000">

# Boot sequence
- 1st stage bootloader: GPU
  - The GPU (VideoCore IV), contains a VPU (Vector processing unit) and two Scalar Units (RISC)   
  - The VPU runs code from ROM (and check the OTP-block)
    - boot mode register @OTP-block:
      - SD card boot (default): the FAT32 boot partition of the SDCard is mounted if present.
      - [USB Device Boot Mode](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-device-boot-mode) (default?): Available on Raspberry Pi CM, CM3, Zero, Zero W, A, A+, and 3A+ only. 
      - [GPIO Boot Mode](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-boot-mode): Available on the Raspberry Pi CM3, CM3+, 3A+, 3B, 3B+ 
      - [USB Host Boot Mode](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-host-boot-mode), Ethernet and Mass Storage: Available on Raspberry Pi 3B, 3B+, 3A+, and 2B v1.2 only. Raspberry Pi 3A+ only supports mass storage boot, not network boot.
- 2nd stage bootloader: GPU
  - `bootcode.bin` -> 128K 4 way set associative L2 cache of the GPU
  - R-Pi4,400 and CM4, instead of `bootcode.bin`, use an EEPROM, with some binaries created with `rpi-eeprom`
  - RAM enabled, `start.elf` loaded
- 3rd stage bootloader: `start.elf` @GPU (called VideoCore OS or VCOS ??)
  - `start.elf` contains a multitasking kernel (ThreadX \[OS\]) and implementations of OpenGL-ES/OpenVG \[...\] [forum](https://forums.raspberrypi.com/viewtopic.php?t=24204)
  - (The physical memory address perceived by the ARM core is mapped to >=0xC0000000@VideoCore by the MMU)
  - sets up system using `config.txt` &nbsp; ([RPi_config](https://elinux.org/RPiconfig))
    - selects the .dtb file appropriate for the platform by name (e.g. `bcm2711-rpi-400.dtb`), and reads it into memory
  - Determines memory split between CPU/GPU (Default 50/50)
  - resets the ARM core
  - loads kernel.img into SDRAM at `0x8000`
- the ARM core executes `kernel.img` with arguments from `cmdline.txt`
  - `cmdline.txt` can be found in `/boot/` &nbsp; ([RPi_cmdline](https://elinux.org/RPi_cmdline.txt))
  - kernel executes `/sbin/init`
    - `init` looks at `/etc/inittab`

## OTP registers and bits
```bash
# Register 17: (boot mode) Bits 0 to 31. Only the "public" information is shown
#   Bit  1: sets the oscillator frequency to 19.2MHz
#   Bit  3: enables pull ups on the SDIO pins
#   Bit 19: enables GPIO bootmode
#   Bit 20: sets the bank to check for GPIO bootmode
#   Bit 21: enables booting from SD card
#   Bit 22: sets the bank to boot from
#   Bit 28: enables USB device booting
#   Bit 29: enables USB host booting (ethernet and mass storage)

vcgencmd otp_dump | grep 17:  # R-Pi B+ v1.2 -> 17:1020000a (default)
                              # R-Pi Zero W  -> 
```

&nbsp;

# Imager
## Debian:
```bash
sudo apt update
sudo apt install snapd
sudo snap install core
sudo snap install rpi-imager
snap list
/snap/bin/rpi-imager ↵
```
- `C-X` Advanced options, to set hostname, ssh, etc.

&nbsp;

# Raspbian
- Debian arm with raspberry pi support for hard-float. Debian arm was initially ARMv4 soft-float or ARMv7 with hard-float (Not compatible with the first Pi)
- Raspberry Pi Os: Debian ARM64

```bash
wget https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-11-08/2021-10-30-raspios-bullseye-armhf-lite.zip
sha256sum 2021-10-30-raspios-bullseye-armhf-lite.zip
unzip !$
sudo dd if=2021-10-30-raspios-bullseye-armhf.img of=/dev/mmcblk0 bs=4M conv=fsync status=progress
sync
```
**Verification**:
```bash
# from previous dd: xxx+0 records in
sudo  dd if=/dev/mmcblk0 of=from-sd-card.img bs=4M count=xxx
truncate --reference 2021-10-30-raspios-bullseye-armhf.img from-sd-card.img
diff -s from-sd-card.img 2021-10-30-raspios-bullseye-armhf.img
```

&nbsp;

# UART
**Host**
```bash
# stty -F /dev/ttyUSB0 115200 cs8 -cstopb -parenb  
#   cs8: 8bits
#   -cstopb: one stop bit
#   -parenb: no parity bit 
minicom
```
**R-Pi**
- `enable_uart=1` (console): Check if this setting has impact in `vcgencmd measure_clock core` (core frequency)
- To enable early stage UART: (R-Pi) `strings bootcode.bin | grep BOOT_UART && sed -i -e "s/BOOT_UART=0/BOOT_UART=1/" bootcode.bin` (_For boards pre-Raspberry Pi 4, Model B_)

&nbsp;

# mDNS
> Verify: If you change the system hostname of the Raspberry Pi (e.g., by editing `/etc/hostname`), Avahi will also change the `.local` mDNS address.
```conf
# /etc/avahi/avahi-daemon.conf:
[server]
host-name=rpizw
domain-name=local
```
- `systemctl restart avahi-daemon`

&nbsp;

# Throttling
`journalctl -b | grep -i voltage | wc -l`: warnings count

```bash
#!/usr/bin/bash

THR=$(/usr/bin/vcgencmd get_throttled | cut -d'=' -f2)
(( $THR & 0x1 << 0)) && echo "Under-voltage detected"
(( $THR & 0x1 << 1)) && echo "Arm frequency capped"
(( $THR & 0x1 << 2)) && echo "Currently throttled"
(( $THR & 0x1 << 3)) && echo "Soft temperature limit active"
(( $THR & 0x1 << 16)) && echo "Under-voltage has occurred"
(( $THR & 0x1 << 17)) && echo "Arm frequency capping has occurred"
(( $THR & 0x1 << 18)) && echo "Throttling has occurred"
(( $THR & 0x1 << 19)) && echo "Soft temperature limit has occurred"
```

&nbsp;

# Python
- `apt list --installed | grep python` &nbsp; highlights:
  ```
  python3-rpi.gpio/stable,now 0.7.0-0.2+b1 armhf [installed]
  python3-smbus/stable,now 4.2-1+b1 armhf [installed]
  python3-sn3218/stable,now 1.2.7 all [installed]
  python3-spidev/stable,now 20200602~200721-1 armhf [installed]
  python3-automationhat/stable,now 0.2.0 all [installed]
  python3-explorerhat/stable,now 0.4.2 all [installed]
  ```

&nbsp;

# GPIO

&nbsp;

# I2C
- `raspi-config` → "Interface Options" → enable I2C
- `i2cdetect` from `i2c-tools`

&nbsp;

# SPI

&nbsp;

# Serial
- `serial0 -> ttyS0`: is the UART on pins 8,10
- `serial1 -> ttyAMA0`: is used for Bluetooth ()
```python
import serial
S = serial.Serial('/dev/serial0',baudrate=9600)
```

&nbsp;

# DT
- c.f. `/boot/overlays/README`
```bash
# c.f. adafruit's tftbonnet13-overlay.dts
dtc -I dts -O dtb -o overlay.dtbo overlay.dts
```

&nbsp;

# MIDI
```bash
sudo apt install fluidsynth
fluidsynth -a alsa -n -i /usr/share/sounds/sf2/FluidR3_GM.sf2 72257.mid
fluidsynth -T wav -F test.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 72257.mid 
```
```bash
fluidsynth -a alsa -m alsa_seq -i -1 -s -p FluidSynth /usr/share/sounds/sf2/FluidR3_GM.sf2 &  # check this
dosbox ↵  # dosbox-staging
```
- c.f. `sudo renice -n -15 -p <pid>`

&nbsp;

# Kernel Modules
- [This](https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/blob/main/adafruit-pitft.py) script: installs a systemd daemon, compile a kernel module, writes udev rules, etc. Neat.
  - `sudo apt update && sudo apt upgrade` (This will also upgrade the Kernel -> Reboot)
  - `sudo apt install raspberrypi-kernel-headers`
  - Proceed as in LDD3, then `mv <mod>.ko /lib/modules/$(uname -r)/kernel/drivers/staging/`

&nbsp;

# Notes
- `/etc/inputrc: set bell-style none` to avoid intense rage/berserk

```bash
raspi-config  # TUX configuration tool
DISPLAY=:0 zenity --warning --text="Warning!"
DISPLAY=:0 yad --timeout 3 --image alert.gif 
DISPLAY=:0 xdg-screensaver reset
```

- [luks-dropbear](https://www.cyberciti.biz/security/how-to-unlock-luks-using-dropbear-ssh-keys-remotely-in-linux/)
- `libsensors`

```bash
lscpu  # display information about the CPU architecture
vcgencmd commands ↵
iotop  # simple top-like I/O monitor
cat /proc/device-tree/model  # → "Raspberry Pi 400 Rev 1.0"
cat /etc/os-release
```

- [benchmarking-the-raspberry-pi-4](https://medium.com/@ghalfacree/benchmarking-the-raspberry-pi-4-73e5afbcd54b)
- `raspi-config` → `sudo find / -type d -mmin -5 -ls | grep -v "proc"`: list modified directories within last 5 mins
- c.f. `/etc/asound.conf`
- Hardware Watchdog, `/boot/config.txt: dtparam=watchdog=on`, `/dev/watchdog`
- HD63P01M1 - CMOS MCU
  - Package on Package concept
- c.f. `motion` https://motion-project.github.io/motion_config.html
- R-Pi both access point (AP) and station (STA)
- [This](https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/blob/main/adafruit-pitft.py) script: installs a systemd daemon, compile a kernel module, writes udev rules, etc. Neat.
- **f2fs** (**Flash-Friendly File System**) is a flash file system initially developed by Samsung Electronics for the Linux kernel (wikipedia)
  - `f2fs` may be time consuming to set up. Make sure to test `ext4` with `noatime@/etc/fstab`, and use `ramfs`as possible
- Raspberry Pi 3 quick look at native USB boot with Tony D https://www.youtube.com/watch?v=hxV3yrn8FK8&list=PL1A011279DBD4EB7E&index=50&ab_channel=AdafruitIndustries
- https://raspberrypi.stackexchange.com/questions/104722/kernel-types-in-raspbian-10-buster@fg%E2%82%AC@
- Password recovery:
  ```bash
  /boot/cmdline.txt: '[...] init=/bin/sh'
  mount -o remount,rw /dev/mmcblk0p2 /
  mount -o rw /dev/mmcblk0p1 /boot/  # optional
  ```
- **tmpfs**
  ```bash
  sudo mkdir /tmp/stream
  sudo mount -t tmpfs -o defaults,noatime,mode=1777 tmpfs /tmp/stream
  time dd if=/dev/zero of=~/100M.bin  bs=100M  count=1  # → 5.030s @rpi400
  time dd if=/dev/zero of=/tmp/stream/100M.bin bs=100M count=1  # → 0.549s @rpi4000
  ```
- `/etc/sudoers.d/010_at-export`
  - `Defaults env_keep += "NO_AT_BRIDGE"`
- [userland](https://github.com/raspberrypi/userland): This repository contains the source code for the ARM side libraries used on Raspberry Pi. These typically are installed in /opt/vc/lib and includes source for the ARM side code to interface to: EGL, mmal, GLESv2, vcos, openmaxil, vchiq_arm, bcm_host, WFC, OpenVG.
- When e.g. Linux requires an element not directly accessible to it (e.g. ), it communicates with VCOS using mailboxes

## Interesting
```
v4l2-ctl --list-devices
bcm2835-codec-decode (platform:bcm2835-codec):
        /dev/video10
        /dev/video11
        /dev/video12
        /dev/video18
        /dev/video31
        /dev/media2

bcm2835-isp (platform:bcm2835-isp):
        /dev/video13
        /dev/video14
        /dev/video15
        /dev/video16
        /dev/video20
        /dev/video21
        /dev/video22
        /dev/video23
        /dev/media0
        /dev/media1

Webcam C170: Webcam C170 (usb-3f980000.usb-1.1.2):
        /dev/video0
        /dev/video1
        /dev/media3
```

## Mem
```c
uint32_t pagesize = getpagesize();  // 4096
uint32_t pagemask = ~0UL ^ (getpagesize() - 1);  // 0xfffff000
uint32_t offsetmask = getpagesize() - 1;  // 0xfff
int mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
// mmap: a new `struct vm_area_struct` is created:
// (Entry added in /proc/PID/maps ??)
void *mem = mmap(0, size, PROT_READ|PROT_WRITE, MAP_SHARED, mem_fd, DMA_ADDR & pagemask);
close(mem_fd);
return (char *)mem + (DMA_ADDR & offsetmask);
// cat /proc/PID/maps
// [...]
// b6faa000-b6fab000 rw-s fe200000 00:05 4    /dev/mem
// b6fab000-b6fac000 rw-s fe20c000 00:05 4    /dev/mem
// b6fac000-b6fad000 rw-s fe007000 00:05 4    /dev/mem
// b6fad000-b6fae000 rw-s 3ebf9000 00:05 4    /dev/mem
// b6fae000-b6faf000 rw-s 00000000 00:05 92   /dev/gpiomem
// DMA Channel 0 is located at the address of 0x7e007000, Channel 1 at 0x7e007100, ...
```