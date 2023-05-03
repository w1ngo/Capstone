import peripheral_functions as funcs
import os

# the usb drive is located in /media/ag
# want to output all files located at the location
# of files in the directory present, representing
    # the external drive
folder = [ item for item in os.listdir("/media/ag") if os.path.isdir(f"/media/ag/{item}") ][0]
files = [ filename for filename in os.listdir(f"/media/ag/{folder}") if ".csv" in filename or ".xlsx" in filename ]
print(files)

with open("test_data.csv", "a") as f:
    f.write("test, info, new, line, appended")

