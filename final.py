from motor_library import *

set_motor_config("SIX")  # Change as needed for your device

stop_all()
print("All motors stopped and system ready.")

while True:
    # Wait until START button is pressed
    wait_for_start()
    
    led_on()
    buzz(1, 5)   #buzzer (duration, no. of beeps for the duration
    wait(1)
                            
    led_off()
    wait(1)
    
    servo1.pos(0)
    wait(1)

    # ---------------- Mecanum Movements ----------------
    run("front_right", speed=100, direction=1)
    wait(2)
    
    run("front_left", speed=100, direction=1)
    wait(2)
    stop("front_right");
    
    run("back_right", speed=100, direction=1)
    wait(2)
    stop("front_left");
    
    run("back_left", speed=100, direction=1)
    wait(2)
    stop("back_right")
    
    run("extra_motor", speed=100, direction =1)
    wait(2)
    stop("back_left")
    stop("extra_motor")

    # Stop all motors at the end
    stop_all()
    print("Sequence completed. All motors stopped.")


