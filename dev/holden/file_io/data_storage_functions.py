import pandas as pd
import subprocess

'''
lsusb -> shell command to list all usb devices connected
  may be useful for finding USB & identifying webcams

usb-devices -> Another shell command. Seems to be a more
  verbose version than lsusb. May have more connections
  displayed as well.
'''
def mount_drive():
    subprocess.Popen('sudo mount /dev/sda1 /mnt/usb -o uid=pi,gid=pi')
    #DNDOF: mount_drive()


def unmount_drive():
    subprocess.Popen('sudo unmount /mnt/usb')
    #ENDOF: unmount_drive()

def read_excel_file(filename: str, sheet: int=0) -> pd.core.frame.DataFrame:
    return pd.read_excel(filename, sheet, index_col = sheet)
    #ENDOF: read_excel_file()


def write_excel_file(filename: str, data: pd.core.frame.DataFrame):
    data.to_excel(filename, index=False, header=True)
    #ENDOF: write_excel_file()


def append_excel_file(filename: str, data: pd.core.frame.DataFrame):
    return
    #ENDOF: append_excel_file()


def read_csv(filename: str):
    return
    #ENDOF: read_csv()


def write_csv(filename: str):
    return
    #ENDOF: write_csv()


def append_csv(filename: str):
    return
    #ENDOF: append_csv()


if __name__=="__main__":
    frame = read_excel_file("SPR Gravity 2022.xlsx", 1)
    print(frame)

    write_excel_file("gravity_copy.xlsx", frame)
