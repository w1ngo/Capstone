import pandas as pd
import subprocess

'''
lsusb -> shell command to list all usb devices connected
  may be useful for finding USB & identifying webcams

usb-devices -> Another shell command. Seems to be a more
  verbose version than lsusb. May have more connections
  displayed as well.
'''

def read_barcode() -> str:
    for i in range(5):
        inp = input("Scan batch ID: ")
        if input(f"Is {inp} the correct batch ID [Y/n]?") in ["Y", "y", "YES", "Yes", "yes"]: return inp
    return input("10 incorrect attempts to read the barcode...please type in the desired Batch ID: ")

def take_pic(camera: int):
    if camera == 1:
        cmd = " fswebcam --device /dev/video0   \
                         --quiet                \
                         --resolution 640x480   \
                         -s sharpness=15       \
                         --frame 8              \
                         --no-timestamp         \
                         --no-banner            \
                         --no-info              \
                         --greyscale            \
                         --save                 \
                         image_cam1.jpg "
    else: 
        cmd = " fswebcam --device /dev/video2  \
	               --quiet               \
	               --resolution 640x480  \
	               -s sharpness=15       \
	               --frame 8             \
	               --no-timestamp        \
	               --no-banner           \
	               --no-info             \
	               --greyscale           \
	               --save                \
                       image_cam2.jpg        "
    subprocess.Popen( cmd.split(), stdout = subprocess.PIPE )


def mount_drive():
    subprocess.Popen('sudo mount /dev/sda1 /mnt/usb -o uid=pi,gid=pi'.split(), stdout=subprocess.PIPE)
    #DNDOF: mount_drive()


def unmount_drive():
    subprocess.Popen('sudo unmount /mnt/usb'.split(), stdout=subprocess.PIPE)
    #ENDOF: unmount_drive()


def read_excel_file(filename: str, sheet=0) -> pd.core.frame.DataFrame:
    return pd.read_excel(filename, sheet_name = sheet, index_col = None).dropna(how="all")
    #ENDOF: read_excel_file()


def write_excel_file(filename: str, data: pd.core.frame.DataFrame, sheet="untitled"):
    data.to_excel(filename, index=True, header=True, sheet_name=sheet)
    #ENDOF: write_excel_file()


def read_csv(filename: str):
    with open(filename, "r") as f: return list(map(lambda l: l.split(','), f.readlines()))
    #ENDOF: read_csv()


def write_csv(filename: str, data):
    with open(filename, "w") as f:
        for line in data: f.writelines( line )
    #ENDOF: write_csv()

