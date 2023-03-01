
import subprocess

'''
lsusb - shell command to list all usb devices connected
  may be useful for finding USB & identifying webcams
'''

def mount_drive(): subprocess.Popen('sudo mount /dev/sda1 /mnt/usb -o uid=pi,gid=pi')
def unmount_drive(): subprocess.Popen('sudo unmount /mnt/usb')


