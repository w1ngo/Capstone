import dimentiometer_functions as dim
import gravitometer_functions as grav
import test_functions as test
import json
import os.path

def main():
    while(True):
        print("[Fancy name here]\n\n"
            "1. Run Dimentiometer & Gravitometer\n"
            "2. Run Gravitometer Only\n"
            "3. Measure Tare Automatically\n"
            "4. Input Tare Manually\n"
            "5. Measure Load Cell Conversion Ratio Automatically\n"
            "6. Input Load Cell Conversion Ratio Manually\n"
            "7. Reset Position\n"
            "8. Test Functions\n"
            "9. Exit\n"  # Probably not neccessary
            )
        option = input("Select an option: ")

        if option == "1":  # Run Dimentiometer & Gravitometer
            if os.path.isfile('tare.json') and os.path.getsize('tare.json') > 0 and os.path.isfile('ratio.json') and os.path.getsize('ratio.json') > 0:
                for i in range(10):  # Loop for each potato
                    top_values = dim.take_picture("Top")
                    side_values = dim.take_picture("Side")
                    # Edge Detection
                    # Measure Potato

                with open('tare.json', 'r') as file:
                    tare_dict = json.load(file)
                with open('ratio.json', 'r') as file:
                    ratio_dict = json.load(file)
                air_weight1, air_weight2 = grav.read_load_cell(tare_dict['Air1'], tare_dict['Air2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])
                grav.motor_control("Vertical Down")
                water_weight1, water_weight2 = grav.read_load_cell(tare_dict['Water1'], tare_dict['Water2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])
                grav.motor_control("Vertical Up")
                # Dump potatoes
                # Store data
            else:
                print("No tare file found. Please calibrate tare first.")

        elif option == "2":  # Run Gravitometer Only
            if os.path.isfile('tare.json') and os.path.getsize('tare.json') > 0 and os.path.isfile('ratio.json') and os.path.getsize('ratio.json') > 0:
                with open('tare.json', 'r') as file:
                    tare_dict = json.load(file)
                with open('ratio.json', 'r') as file:
                    ratio_dict = json.load(file)
                air_weight1, air_weight2 = grav.read_load_cell(tare_dict['Air1'], tare_dict['Air2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])
                grav.motor_control("Vertical Down")
                water_weight1, water_weight2 = grav.read_load_cell(tare_dict['Water1'], tare_dict['Water2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])
                grav.motor_control("Vertical Up")
                # Dump potatoes
                # Store data
            else:
                print("No tare file found. Please calibrate tare first.")
            
        elif option == "3":  # Measure weight of basket (tare) automatically
            air_tare1, air_tare2, water_tare1, water_tare2 = grav.measure_tare()
            tare_dict = {"Air1": air_tare1, "Air2": air_tare2, "Water1": water_tare1, "Water2": water_tare2}
            with open('tare.json', 'w') as file:
                json.dump(tare_dict, file, indent=4)
       
        elif option == "4":  # Input tare values manually
            air_tare1 = input("Enter out-of-water tare for load cell 1: ")
            air_tare2 = input("Enter out-of-water tare for load cell 2: ")
            water_tare1 = input("Enter in-water tare for load cell 1: ")
            water_tare2 = input("Enter in-water tare for load cell 2: ")

            if air_tare1.replace('.', '', 1).isnumeric() and air_tare2.replace('.', '', 1).isnumeric() and water_tare1.replace('.', '', 1).isnumeric() and water_tare2.replace('.', '', 1).isnumeric():
                tare_dict = {"Air1": float(air_tare1), "Air2": float(air_tare2), "Water1": float(water_tare1), "Water2": float(water_tare2)}
                with open('tare.json', 'w') as file:
                    json.dump(tare_dict, file, indent=4)
            else:
                print("Tare values must be numeric")

        elif option == "5":  # Measure digital-to-grams conversion ratio of load cells
            if os.path.isfile('tare.json') and os.path.getsize('tare.json') > 0:
                with open('tare.json', 'r') as file:
                    tare_dict = json.load(file)
                known_weigtht = input("Enter known weight of object in basket: ")
                ratio1, ratio2 = grav.measure_ratio(known_weigtht, tare_dict['Air1'], tare_dict['Air2'])
                ratio_dict = {"Ratio1": ratio1, "Ratio2": ratio2}
                with open('ratio.json', 'w') as file:
                    json.dump(ratio_dict, file, indent=4)

            else:
                print("No tare file found. Please calibrate tare first.")

        elif option == "6":  # Input conversion ratio manually
            ratio1 = input("Enter conversion ratio for load cell 1: ")
            ratio2 = input("Enter conversion ratio for load cell 2: ")

            if ratio1.replace('.', '', 1).isnumeric() and ratio2.replace('.', '', 1).isnumeric():
                ratio_dict = {"Ratio1": float(ratio1), "Ratio2": float(ratio2)}
                with open('ratio.json', 'w') as file:
                    json.dump(ratio_dict, file, indent=4)
            else:
                print("Ratio values must be numeric")
     
        elif option == "7":  # Reset position of basket
            grav.motor_control("Vertical Up")
            grav.motor_control("Rotational In")
       
        elif option ==  "8":
            print("Which component to test?\n\n"
                  "1. Camera Pictures\n"
                  "2. [potato measurement testing?]\n"
                  "3. IR Sensor\n"
                  "4. Servo Motor\n"
                  "5. Load Cells\n"
                  "6. Stepper Motors\n"
                  "7. Limit Switches\n"
                  "9. Go back to main screen\n")
            test_option = input()
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

            elif test_option in ["9", "q", "Q", "e", "E"]:
                continue

            else:
                print("Invalid input")
        
        elif option in ["9", "q", "Q", "e", "E"]:  # Exit program
            break
  
        else:
            print("Invalid input")

if __name__ == '__main__':
    main()
