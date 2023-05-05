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
    
    if input("Would you like to zero the scale? [Y/n] ") in ("Y", "y", "yes", "Yes"):
        tare_scale()

    print( "\n\nWelcome to the Agrilife Tuber Analysis System!" )
    print( "______________________________________________" )
    print( "What procedures will be performed during this trial?\n"
           "1) specific gravity only (Gravitometer)\n"
           "2) specific gravity and dimension measurement (Dimentiometer)\n" )
    
    while True:
        option = input( "Select an option: ")
        if option == "1": return 1
        if option == "2": return 2
        print( "Please enter the digit 1 or the digit 2 to indicate the desired procedures\n" )
    #ENDOF: greeting()


def tare_scale():
    _ = input("Press enter when the basket is empty, still, and ready to be calibrated")
    air_tare1, air_tare2, water_tare1, water_tare2 = grav.measure_tare()
    tare_dict = {"Air1": air_tare1, "Air2": air_tare2, "Water1": water_tare1, "Water2": water_tare2}
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
    if os.path.isfile('tare.json') and os.path.getsize('tare.json') > 0 \
       and os.path.isfile('ratio.json') and os.path.getsize('ratio.json') > 0:
        with open('tare.json', 'r') as file: tare_dict   = json.load(file)
        with open('ratio.json', 'r') as file: ratio_dict = json.load(file)

        # measure air-weight
        air_w1, air_w2 = grav.read_load_cell(tare_dict['Air1'], tare_dict['Air2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])

        # Measure weight in water
        
        grav.motor_control("Vertical Down")
        wet_w1, wet_w2 = grav.read_load_cell(tare_dict['Water1'], tare_dict['Water2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])

        # Calculate specific gravity
        specific_gravity = air_w2 / (air_w2 - wet_w2)

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
    if option == 1:
        data = []

        print("Gravitometer selected")
        while True:
            if input("Ready for a trial? [Y/n] ") in ("Y", "y", "yes", "Yes"):
                print("Starting trial. If you have not already, load tubers in the basket")
                code = func.read_barcode()
                length = "NA"
                width  = "NA"
                thick  = "NA"
                
                if input("Input length, width, and thickness data? [Y/n] ") in ("Y", "y", "Yes", "yes"):
                    length = input("Length (cm): ")
                    width  = input("Width (cm): ")
                    thick  = input("Thickness (cm): ")

                reset_position()
                sleep(1)
                print("Starting weight measurements")
                air, wet, sg = gravitometer(code)
                
                condition = "OK"
                if sg < 1.055: condition = "LOW"
                if sg > 1.07 : condition = "HIGH"

                data.append(f"{code},{air},{wet},{length},{width},{thick},{sg},{condition}\n")
                print(f"Calculated specific gravity: {sg}" )

                continue
            
            # if the user did not indicate "yes", then record data and exit
            while True:
                op = input("Enter 1 to recalibrate, or 2 to store data and exit: ")

                if op == "1":
                    tare_scale()
                    print("Scale has been rezeroed.")
                    if input("Would you like to recalibrate with a known weight? [Y/n] ") in ("Y", "y", "Yes", "yes"):
                        calibrate_scale()
                        print("Scale has been recalibrated")
                    break

                if op == "2":
                    folder = [item for item in os.listdir("/media/ag") if os.path.isdir(f"/media/ag/{item}")][0]
                    fileType = input("Enter 1 to write to a new csv, or 2 to add onto an exiting file: ")
                    if fileType == "1":
                        filename = input("Enter your desired filename, excluding the file extension: ")
                        with open(f"/media/ag/{folder}/{filename}.csv", "w") as f:
                            f.write("Plot, Weight out(g), Weight in(g), Length(cm), Width(cm), Thickness(cm), Specific Gravity, Check\n")
                            for line in data:
                                f.write(line)
                        print("File write complete. Raw output shown below. Exiting program now...")
                        Popen(f"cat /media/ag/{folder}/{filename}.csv".split())
                        return

                    
                    if fileType == "2":
                        print("The files available on the detected drive are listed here: ")
                        print( [ filename for filename in os.listdir(f"/media/ag/{folder}") if ".csv" in filename or ".xlsx" in filename or ".xls" in filename ] )

                        f = input( "Enter the filename, along with the extension, that you would like to append to: " )

                        if ".csv" in f:
                            print( "CSV-type detected, based on the file extension.")
                            with open(f"/media/ag/{folder}/{f}", "a") as fil:
                                for line in data:
                                    fil.write(line)
                            print("File write complete. Raw output shown below. Exiting program now...")
                            Popen(f"cat /media/ag/{folder}/{f}".split())
                            return


                        else:
                            print( "Excel spreadsheet detected, based on the file extension. Depending on the size of the file, the write process may be slow." )
                            sheet_name = input( "Input the sheet name you would like to append to, or just press enter to write to the first sheet: " )
                            if sheet_name == "": sheet_name = 0
                            frame = func.read_excel_file(f,sheet_name)
                            print(frame)

                print("Input not recognized. Please enter the digit 1 or the digit 2.")
            

    # gravitometer & dimentiometer
    if option == 2: print( "This option is not currently supported. Aborting..." )
    #ENDOF: run()


"""
Test options function that prints the test menu and gets an input from the user.
Calls the corresponding test function for the option chosen.
"""
def test_options(option):
    print("\n\nWhich component to test?\n\n"
          "1) Camera Pictures\n"
          "2) [potato measurement testing? barcode?]\n"
          "3) IR Sensor\n"
          "4) Servo Motor\n"
          "5) Load Cells\n"
          "6) Stepper Motors\n"
          "7) Limit Switches\n"
          "9) Go back to main screen\n")
    test_option = input("Select an option: ").strip()
    print("\n\n")

    if test_option == "1": test.test_camera_picture()
    elif test_option == "2": pass
    elif test_option == "3": pass            
    elif test_option == "4": test.test_servo_motor()
    elif test_option == "5": test.test_load_cell()
    elif test_option == "6": test.test_stepper_motor()
    elif test_option == "7": test.test_limit_switch()
    elif test_option.lower() in ["9", "b", "back"]: return
    else: print("Invalid Input.")

    return


"""
Help options function that prints a description of each main menu option.
"""
def help_options(option):
    # "help" command
    if option.find(" ") == -1:
        print("\n\n1) Runs dimentiometer to get dimensions of ten potatoes and then runs gravitometer to get specific gravity.\n"
              "2) Runs gravitometer to get specific gravity.\n"
              "3) Measures tare weight of basket in air and in water. Keep basket empty and basin filled with water.\n"
              "4) Allows user to manually enter numerical values for basket tare. \n"
              "5) Measures digital to grams conversion ratio of load cells. Requires object of known weight placed in basket.\n"
              "6) Allows user to manually enter numerical values for conversion ratio.\n"
              "7) Resets position of gravitometer basket.\n"
              "8) Lists options to test various components in the system.\n"
              "9) Stops the program.")
    
    # "help [#]" command 
    else:
        # "help 1"
        if option.split(" ")[1] == "1":
            print("\n\n1) Run Dimentiometer & Gravitometer\n"
                  "Place a potato in the chute. The system will measure dimensions and then drop the potato into the basket below.\n"
                  "Repeat until ten potatoes have been measured. The gravitometer basket will automatically weight the potatoes\n"
                  "in air and water, and then dump the batch out to the side. The measured values are stored in a .csv file.")

        # "help 2"
        elif option.split(" ")[1] == "2":
            print("\n\n2) Run Gravitometer Only\n"
                  "Place ten potatoes in the gravitometer basket and then select this option.\n"
                  "The gravitometer basket will automatically weight the potatoes in air and water, and then dump the batch out to the side.\n"
                  "The measured values are stored in a .csv file.")

        # "help 3"
        elif option.split(" ")[1] == "3":
            print("\n\n3) Measure Tare Automatically\n"
                  "Tare is used to zero the weight of the basket. Empty the basket and fill the basin with water before selecting this option.\n"
                  "The system will automatically measure the basket tare in air and water.\n"
                  "Since this value is stored to a file, tare weight does NOT need to be measured more than once.")

        # "help 4"
        elif option.split(" ")[1] == "4":
            print("\n\n4) Input Tare Manually\n"
                  "Used to manually enter numerical values for tare weigth in air and water.")

        # "help 5"
        elif option.split(" ")[1] == "5":
            print("\n\n5) Measure Load Cell Conversion Ratio Automatically\n"
                  "The load cells measure the weight of the potatoes, but return a digital value. A conversion ratio must be found\n"
                  "to obtain the desired weigth in grams. Place an object of known weight into the basket before selecting this option.\n"
                  "When prompted, enter the weight of the object in grams (e.g. for a 5 gram weight, enter: \"5\").\n"
                  "The conversion ratio will then be calculated automatically.\n"
                  "Since this value is stored to a file, the conversion ratio does NOT need to be measured more than once.")

        # "help 6"
        elif option.split(" ")[1] == "6":
            print("\n\n6) Input Load Cell Conversion Ratio Manually\n"
                  "Used to manually enter numerical values for load cell conversion ratio.")

        # "help 7"
        elif option.split(" ")[1] == "7":
            print("\n\n7) Reset Position\n"
                  "Moves the basket upwards and rotates back to the center.\n"
                  "Should be used if the basket gets stuck.")

        # "help 8"
        elif option.split(" ")[1] == "8":
            print("\n\n8) Test Functions\n"
                  "Camera test displays the live feed of either the top or side camera and prints the grayscale values when stopped.\n"
                  "IR sensor test prints the current value from the IR sensor.\n"
                  "Servo motor test moves the trapdoor to open, closed, or a specified position.\n"
                  "Load cell test prints the raw digital output or final calculated weight.\n"
                  "Stepper motor test moves the basket to the chosen position.\n"
                  "Limit switch test prints the current value of each of the four switches.")

        # "help 9"
        elif option.split(" ")[1] == "9":
            print("\n\n9) Exit\n"
                  "Stops the program. The program can be started again by reopening the terminal. \n"
                  "This system is intended to be kept on, so shutting the system off before each test is NOT required.")
        else:
            print("Invalid Input.")

    print("\nType \"help\" for a general explanation of the commands.\n"
          "Type \"help [#]\" for a detailed explanation on a ceratin command.\n"
          "Or press Enter to return.")
    option = input().strip()

    # Allow user to read more help commands before returning to main screen
    if option.split(" ")[0] == "help":
        help_options(option)
    
    else:
        return


if __name__ == '__main__':
    run()
