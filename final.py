from motor_library import *

set_motor_config("NINE")  # Change as needed for your device

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
    movement("front_right", speed=100, duration=2, direction=1)
    wait(2)
    
    movement("front_left", speed=100, duration=2, direction=1)
    wait(2)
    
    movement("back_right", speed=100, duration=2, direction=1)
    wait(2)
    
    movement("back_left", speed=100, duration=2, direction=1)
    wait(2)
    
    movement("extra_motor", speed=100, duration=2, direction =1)
    wait(2)

    # Stop all motors at the end
    stop_all()
    print("Sequence completed. All motors stopped.")


