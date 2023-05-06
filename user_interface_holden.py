import gravitometer_functions as grav
import peripheral_functions as func
import test_functions as test
import json
import os
import RPi.GPIO as GPIO
from time import sleep
from subprocess import Popen

def greeting():
    reset_position()
    
    # Option to zero scale (basket tare) on startup
    if input("Would you like to zero the scale? [Y/n] ") in ("Y", "y", "yes", "Yes"):
        tare_scale()

    # Startup menu
    print( "\n\nWelcome to the Agrilife Tuber Analysis System!" )
    print( "______________________________________________" )
    print( "What procedures will be performed during this trial?\n"
           "1) specific gravity only (Gravitometer)\n"
           "2) specific gravity and dimension measurement (Dimentiometer)\n" )  # Dimentiometer module not curretnly supported
    
    while True:
        option = input( "Select an option: ")
        if option == "1": return 1  # gravitometer only
        if option == "2": return 2  # gravitometer & dimentiometer (not supported)
        print( "Please enter the digit 1 or the digit 2 to indicate the desired procedures\n" )
    #ENDOF: greeting()


def tare_scale():
    _ = input("Press enter when the basket is empty, still, and ready to be calibrated")
    air_tare1, air_tare2, water_tare1, water_tare2 = grav.measure_tare()
    tare_dict = {"Air1": air_tare1, "Air2": air_tare2, "Water1": water_tare1, "Water2": water_tare2}

    # Save data to file
    with open('tare.json', 'w') as file: json.dump(tare_dict, file, indent=4)
    #ENDOF: tare_scale()


def calibrate_scale():
    known_weigtht = input("Enter known weight of object in basket (grams): ").strip()
    with open('tare.json', 'r') as file: tare_dict = json.load(file)
    ratio1, ratio2 = grav.measure_ratio(float(known_weigtht), tare_dict['Air1'], tare_dict['Air2'])

    # Save data to file
    ratio_dict = {"Ratio1": ratio1, "Ratio2": ratio2}
    with open('ratio.json', 'w') as file: json.dump(ratio_dict, file, indent=4)
    #ENDOF: calibrate_scale()


def gravitometer(id):
    # Load tare and ratio data from files
    if os.path.isfile('tare.json') and os.path.getsize('tare.json') > 0 \
       and os.path.isfile('ratio.json') and os.path.getsize('ratio.json') > 0:
        with open('tare.json', 'r') as file: tare_dict   = json.load(file)
        with open('ratio.json', 'r') as file: ratio_dict = json.load(file)

        # measure air-weight
        air_w1, air_w2 = grav.read_load_cell(tare_dict['Air1'], tare_dict['Air2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])
        grav.motor_control("Vertical Down")

        # Measure weight in water
        wet_w1, wet_w2 = grav.read_load_cell(tare_dict['Water1'], tare_dict['Water2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])

        # Calculate specific gravity
        specific_gravity = air_w2 / (air_w2 - wet_w2)

        # Raise and turn basket to remove potatoes
        grav.motor_control("Vertical Up")
        print("If stuck, slowly rotate the arm counter-clockwise until you hear a click")
        grav.motor_control("Rotational Out")
        _ = input("Press enter when the potatoes are dumped...")
        grav.motor_control("Rotational In")

        return air_w2, wet_w2, specific_gravity

    # if one of the if conditions failed:
    print("Necessary scale calibration data not present, running calibration") 

    calibrate_scale()
    gravitometer(id)
    #ENDOF: gravitometer()


def reset_position():
    grav.motor_control("Vertical Up")
    grav.motor_control("Rotational In")
    #ENDOF: reset_position()


def run():
    GPIO.setwarnings(False)
    option = greeting()

    # gravitometer only
    if option == 1:
        data = []

        print("Gravitometer selected")
        while True:

            # if "yes", start a measurement trial
            if input("Ready for a trial? [Y/n] ") in ("Y", "y", "yes", "Yes"):
                print("Starting trial. If you have not already, load tubers in the basket")
                code = func.read_barcode()
                length = "NA"
                width  = "NA"
                thick  = "NA"
                
                # Input potato dimensions manually, left blank if "no"
                if input("Input length, width, and thickness data? [Y/n] ") in ("Y", "y", "Yes", "yes"):
                    length = input("Length (cm): ")
                    width  = input("Width (cm): ")
                    thick  = input("Thickness (cm): ")
                
                # Run gravitometer
                reset_position()
                sleep(1)
                print("Starting weight measurements")
                air, wet, sg = gravitometer(code)

                # Determine if specific gravity is within the desired range
                condition = "OK"
                if sg < 1.055: condition = "LOW"
                if sg > 1.07 : condition = "HIGH"

                # Add data to a list
                data.append(f"{code},{air},{wet},{length},{width},{thick},{sg},{condition}\n")
                print(f"Calculated specific gravity: {sg}" )

                continue
            
            # if the user did not indicate "yes", then record data and exit
            while True:
                op = input("Enter 1 to recalibrate, or 2 to store data and exit: ")

                # Recalibrate and zero the scale
                if op == "1":
                    tare_scale()
                    print("Scale has been rezeroed.")
                    if input("Would you like to recalibrate with a known weight? [Y/n] ") in ("Y", "y", "Yes", "yes"):
                        calibrate_scale()
                        print("Scale has been recalibrated")
                    break

                # Store data and exit the program
                if op == "2":
                    folder = [item for item in os.listdir("/media/ag") if os.path.isdir(f"/media/ag/{item}")][0]
                    fileType = input("Enter 1 to write to a new csv, or 2 to add onto an exiting file: ")
                    
                    # Store data to new csv file
                    if fileType == "1":
                        filename = input("Enter your desired filename, excluding the file extension: ")
                        with open(f"/media/ag/{folder}/{filename}.csv", "w") as f:
                            f.write("Plot, Weight out(g), Weight in(g), Length(cm), Width(cm), Thickness(cm), Specific Gravity, Check\n")
                            for line in data:
                                f.write(line)
                        print("File write complete. Raw output shown below. Exiting program now...")
                        Popen(f"cat /media/ag/{folder}/{filename}.csv".split())
                        return

                    # Store data to existing csv file
                    if fileType == "2":
                        print("The files available on the detected drive are listed here: ")
                        print( [ filename for filename in os.listdir(f"/media/ag/{folder}") if ".csv" in filename or ".xlsx" in filename or ".xls" in filename ] )

                        f = input( "Enter the filename, along with the extension, that you would like to append to: " )

                        # Append to .csv file
                        if ".csv" in f:
                            print( "CSV-type detected, based on the file extension.")
                            with open(f"/media/ag/{folder}/{f}", "a") as fil:
                                for line in data:
                                    fil.write(line)
                            print("File write complete. Raw output shown below. Exiting program now...")
                            Popen(f"cat /media/ag/{folder}/{f}".split())
                            return

                        # Append to excel file
                        else:
                            print( "Excel spreadsheet detected, based on the file extension. Depending on the size of the file, the write process may be slow." )
                            sheet_name = input( "Input the sheet name you would like to append to, or just press enter to write to the first sheet: " )
                            if sheet_name == "": sheet_name = 0
                            frame = func.read_excel_file(f,sheet_name)
                            print(frame)
                            #return
                            # Does this need a return statement?

                print("Input not recognized. Please enter the digit 1 or the digit 2.")
            
    # gravitometer & dimentiometer
    if option == 2: print( "This option is not currently supported. Aborting..." )
    #ENDOF: run()


if __name__ == '__main__':
    run()
