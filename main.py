from motor_library import *

set_motor_config("SIX")  # Change as needed for your device

stop_all()
print("All motors stopped and system ready.")

oled_status("   RFL ACADEMY", "System Ready", "Press START", "Hello Prashant")
wait_for_start()

while True:

    if key("UP"):
        FW(speed=100)
        oled_status(" FORWARD")

    elif key("DOWN"):
        BW(speed=100)
        oled_status(" BACKWARD")

    elif key("LEFT"):
        L(speed=100)
        oled_status(" LEFT")

    elif key("RIGHT"):
        R(speed=100)
        oled_status(" RIGHT")

    elif key("UPLEFT"):
        FL(speed=100)
        oled_status(" FORWARD LEFT")

    elif key("UPRIGHT"):
        FR(speed=100)
        oled_status(" FORWARD RIGHT")

    elif key("DOWNLEFT"):
        BL(speed=100)
        oled_status(" BACK LEFT")

    elif key("DOWNRIGHT"):
        BR(speed=100)
        oled_status(" BACK RIGHT")

    elif key("Q"):
        CCW(speed=80)
        oled_status(" ROTATE LEFT")

    elif key("E"):
        CW(speed=80)
        oled_status(" ROTATE RIGHT")

    elif key("EXTRAUP"):
        extra_motor(speed=100, direction=1)
        oled_status(" EXTRA UP")

    elif key("EXTRADOWN"):
        extra_motor(speed=100, direction=0)
        oled_status(" EXTRA DOWN")

    elif key("A"):              # A button: servo open
        stop_drive()
        servo1.pos(0.5)
        oled_status(" BUTTON A")

    elif key("B"):              # B button: servo close
        stop_drive()
        servo2.pos(0.5)
        oled_status(" BUTTON B")
        
    elif key("C"):              # C button: servo close
        stop_drive()
        servo3.pos(0.0)
        oled_status(" BUTTON C")
        
    elif key("D"):              # D button: servo close
        stop_drive()
        servo4.pos(0.0)
        oled_status(" BUTTON D")

    else:
        stop_drive()
        oled_status(" STOPPED")

