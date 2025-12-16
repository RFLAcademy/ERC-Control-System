from motor_library import *

set_motor_config("SIX")  # Change as needed for your device

stop_all()
print("All motors stopped and system ready.")

oled_status("   RFL ACADEMY", "System Ready", "Press START", "Hello Prashant")
wait_for_start()

while True:
    # Wait until START button is pressed
   
    if sensor_3() == 1:
        FW(speed=50)
    else:
        stop_drive(FW)
    
#     led_on()
#     buzz(1, 10)   #buzzer (duration, no. of beeps for the duration
#     wait(1)
#                             
#     led_off()
#     wait(1)
#     
#     servo1.pos(0)
#     wait(1)
# 
#     # ---------------- Mecanum Movements ----------------
#     run("front_right", speed=100, direction=1)
#     oled_status("Front Right", "Speed = 100%", "Direction = 1", "Duration = 2 Sec")
#     wait(2)
#     
#     run("front_left", speed=100, direction=1)
#     oled_status("Front Left", "Speed = 100%", "Direction = 1", "Duration = 2 Sec")
#     wait(2)
#     stop("front_right");
#     
#     run("back_right", speed=100, direction=1)
#     oled_status("Back_Right", "Speed = 100%", "Direction = 1", "Duration = 2 Sec")
#     wait(2)
#     stop("front_left");
#     
#     run("back_left", speed=100, direction=1)
#     wait(2)
#     stop("back_right")
#     
#     run("extra_motor", speed=100, direction =1)
#     wait(2)
#     stop("back_left")
#     stop("extra_motor")
#     
#     FW(speed=100)
#     wait(1)
#     stop_drive(FW)
#     wait(2)
#     BW(speed=100)
#     wait(1)
#     stop_drive(BW)
#     wait(2)
#     L(speed=100)
#     wait(1)
#     stop_drive(L)
#     wait(2)
#     R(speed=100)
#     wait(1)
#     stop_drive(R)
#     wait(2)
#     CCW(speed=100)
#     wait(1)
#     stop_drive(CCW)
#     wait(2)
#     CW(speed=100)
#     wait(1)
#     stop_drive(CW)
#     wait(1)
#     FL(speed=100)
#     wait(1)
#     stop_drive(FL)
#     wait(2)
#     BR(speed=100)
#     wait(1)
#     stop_drive(BR)
#     wait(2)
#     FR(speed=100)
#     wait(1)
#     stop_drive(FR)
#     wait(2)
#     BL(speed=100)
#     wait(1)
#     stop_drive(BL)
#     wait(2)

    # Stop all motors at the end
#     stop_all()
#     print("Sequence completed. All motors stopped.")


