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
                         --frame 5              \
                         --no-timestamp         \
                         --no-banner            \
                         --no-info              \
                         --greyscale            \
                         --save                 \
                         image_cam1_5frames.jpg "
    else: 
        cmd = " fswebcam --device /dev/video2  \
	               --quiet               \
	               --resolution 640x480  \
	               -s sharpness=15       \
	               --frame 10            \
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
    return pd.read_excel(filename, sheet_name = sheet, index_col = 0).dropna(how="all")
    #ENDOF: read_excel_file()

'''
Need to rework write and append
    the append mode does not seem to be working...I think it really just 
    allows us to write to a new sheet on an existing file, rather than
    appending rows to a file

insert_rows() is a function that should allow for actually appending to
    the end of a sheet. Will just need a <relatively> painless way
    of keeping track of the row index to write to....able to do
    so without converting whole .xlsx to a dataframe?
'''
def write_excel_file(filename: str, data: pd.core.frame.DataFrame, sheet="untitled"):
    data.to_excel(filename, index=True, header=True, sheet_name=sheet)
    #ENDOF: write_excel_file()


def append_excel_file(filename: str, data: pd.core.frame.DataFrame, sheet=0):
    with pd.ExcelWriter(filename, mode='a') as writer: data.to_excel(writer, sheet_name = sheet)
    #ENDOF: append_excel_file()

def read_csv(filename: str):
    with open(filename, "r") as f: return list(map(lambda l: l.split(','), f.readlines()))
    #ENDOF: read_csv()


def write_csv(filename: str, data):
    with open(filename, "w") as f:
        for line in data: f.writelines( line )
    #ENDOF: write_csv()


if __name__=="__main__":
    mount_drive()
    unmount_drive()
    take_pic(1)
    take_pic(2)

    frame = read_excel_file("SPR Gravity 2022.xlsx", "22SPR")
    print(frame)
    write_excel_file("gravity_copy.xlsx", frame)
    append_excel_file("gravity_copy.xlsx", frame, "22SPR")

