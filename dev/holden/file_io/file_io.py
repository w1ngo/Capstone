
import subprocess

def mount_drive(): subprocess.Popen('sudo mount /dev/sda1 /mnt/usb -o uid=pi,gid=pi')
def unmount_drive(): subprocess.Popen('sudo unmount /mnt/usb')


