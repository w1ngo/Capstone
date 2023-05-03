import peripheral_functions as funcs
from subprocess import Popen

funcs.mount_drive()

Popen("ls /dev/sda1".split)

