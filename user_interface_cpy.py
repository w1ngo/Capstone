import dimentiometer_functions as dim
import gravitometer_functions as grav
import peripheral_functions as func
import test_functions as test
import json
import os.path
import RPi.GPIO as GPIO

"""
User interface function that prints the main menu and gets an input from the user.
Calls the required functions based on the option chosen.
"""
def run():
    GPIO.setwarnings(False)
    while(True):
        print("\n\nTuber Analysis System\n"
              "-----------------------------------------------------\n"
              "1) Run Dimentiometer & Gravitometer\n"
              "2) Run Gravitometer Only\n"
              "3) Tare Automatically\n"
              "4) Tare Manually\n"
              "5) Measure Load Cell Conversion Ratio Automatically\n"
              "6) Input Load Cell Conversion Ratio Manually\n"
              "7) Reset Position\n"
              "8) Test Functions\n"
              "9) Exit\n"
              "(Type \"help\" for a more details)\n")
        option = input("Select an option: ").strip()
        
        # Run Dimentiometer & Gravitometer
        if option == "1":  
            run_dimentiometer()
            run_gravitometer()

        # Run Gravitometer Only
        elif option == "2":
            run_gravitometer()
        
        # Measure weight of basket (tare) automatically
        elif option == "3":
            # Find tare
            air_tare1, air_tare2, water_tare1, water_tare2 = grav.measure_tare()

            # Save data to file
            tare_dict = {"Air1": air_tare1, "Air2": air_tare2, "Water1": water_tare1, "Water2": water_tare2}
            with open('tare.json', 'w') as file:
                json.dump(tare_dict, file, indent=4)
        
        # Input tare values manually
        elif option == "4":
            # Input tare values
            air_tare1   = input("Enter out-of-water tare for load cell 1: ").strip()
            air_tare2   = input("Enter out-of-water tare for load cell 2: ").strip()
            water_tare1 = input("Enter in-water tare for load cell 1: ").strip()
            water_tare2 = input("Enter in-water tare for load cell 2: ").strip()

            # Save data to file
            if air_tare1.replace('.', '', 1).isnumeric() and air_tare2.replace('.', '', 1).isnumeric() and water_tare1.replace('.', '', 1).isnumeric() and water_tare2.replace('.', '', 1).isnumeric():
                tare_dict = {"Air1": float(air_tare1), "Air2": float(air_tare2), "Water1": float(water_tare1), "Water2": float(water_tare2)}
                with open('tare.json', 'w') as file:
                    json.dump(tare_dict, file, indent=4)
            else:
                print("Tare values must be numeric.")
       
        # Measure digital-to-grams conversion ratio of load cells
        elif option == "5":
            # Find ratio
            if os.path.isfile('tare.json') and os.path.getsize('tare.json') > 0:
                with open('tare.json', 'r') as file:
                    tare_dict = json.load(file)
                known_weigtht = input("Enter known weight of object in basket (grams): ").strip()
                if known_weigtht.replace('.', '', 1).isnumeric():
                    ratio1, ratio2 = grav.measure_ratio(float(known_weigtht), tare_dict['Air1'], tare_dict['Air2'])

                    # Save data to file
                    ratio_dict = {"Ratio1": ratio1, "Ratio2": ratio2}
                    with open('ratio.json', 'w') as file:
                        json.dump(ratio_dict, file, indent=4)
                else:
                    print("Known weight must be numeric.")
            else:
                print("No tare file found. Please calibrate tare first.")

        # Input conversion ratio manually
        elif option == "6":
            # Input ratio values
            ratio1 = input("Enter conversion ratio for load cell 1: ").strip()
            ratio2 = input("Enter conversion ratio for load cell 2: ").strip()

            # Save data to file
            if ratio1.replace('.', '', 1).isnumeric() and ratio2.replace('.', '', 1).isnumeric():
                ratio_dict = {"Ratio1": float(ratio1), "Ratio2": float(ratio2)}
                with open('ratio.json', 'w') as file:
                    json.dump(ratio_dict, file, indent=4)
            else:
                print("Ratio values must be numeric.")
     
        # Reset position of basket
        elif option == "7":
            grav.motor_control("Vertical Up")
            grav.motor_control("Rotational In")
       
        # Call test functions
        elif option ==  "8":
            test_options(option)
        
        # Exit program
        elif option.lower() in ["9", "q", "e", "quit", "exit", "end"]:
            break

        # Call help function
        elif option.split(" ")[0] == "help":
            help_options(option)
  
        else:
            print("Invalid Input.")

def run_dimentiometer():
    print("This system is not currently supported.\n")
    return 


def run_gravitometer():
    if os.path.isfile('tare.json') and os.path.getsize('tare.json') > 0 and os.path.isfile('ratio.json') and os.path.getsize('ratio.json') > 0:
        # Get tare
        with open('tare.json', 'r') as file:
            tare_dict = json.load(file)

        # Get ratio
        with open('ratio.json', 'r') as file:
            ratio_dict = json.load(file)

        # Measure weight in air
        air_weight1, air_weight2 = grav.read_load_cell(tare_dict['Air1'], tare_dict['Air2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])

        # Measure weight in water
        grav.motor_control("Vertical Down")
        water_weight1, water_weight2 = grav.read_load_cell(tare_dict['Water1'], tare_dict['Water2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])

        # Calculate specific gravity
        #specific_gravity1 = air_weight1 / (air_weight1 - water_weight1)
        specific_gravity2 = air_weight2 / (air_weight2 - water_weight2)
        #avg_specific_gravity = (specific_gravity1 + specific_gravity2) / 2
        print(specific_gravity2)

        grav.motor_control("Vertical Up")
        # potential sleep
        grav.motor_control("Rotational Out")
        # potential sleep
        grav.motor_control("Rotational In")

        # Store data
        dat = ["test_label", (air_weight2), (water_weight2), specific_gravity2]
        func.write_csv( "test_data.csv", [dat] )
    else:
        print("No tare file found. Please tare first.")

    return


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
    if test_option == "1":
        test.test_camera_picture()

    elif test_option == "2":
        pass

    elif test_option == "3":
        test.test_ir_sensor()            

    elif test_option == "4":
        test.test_servo_motor()

    elif test_option == "5":
        test.test_load_cell()

    elif test_option == "6":
        test.test_stepper_motor()

    elif test_option == "7":
        test.test_limit_switch()

    elif test_option.lower() in ["9", "b", "back"]:
        return

    else:
        print("Invalid Input.")
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
                  "Stops the program. The program can be started again by [explanation]\n"
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
