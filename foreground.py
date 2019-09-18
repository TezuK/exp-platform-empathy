from const_def import *


def menu(menu_type):
    if menu_type == MENU_INITIAL: # Initial screen
        print("----------------")
        print("Menu")
        print("----------------")
        print("1. Robot debug")
        print("2. VS mode")
        print("3. Cooperative mode")
        print("q. Quit")
        print("----------------")
    elif menu_type == MENU_DEBUG:
        print("----------------")
        print("Robot debug menu")
        print("----------------")
        print("1. Movements")
        print("1a. Forward")
        print("1b. Right")
        print("1c. Backwards")
        print("1d. Left")
        print("2. LEDs")
        print("3. Make sounds")
        print("4. Talk")
        print("5. Faces")
        print("6. Tilt")
        print("7. Pan")
        print("8. Presentation")
        print("q. Main Menu")
        print("----------------")
        
    return input("Selection: ")
