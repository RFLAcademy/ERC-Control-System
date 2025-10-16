import time
from machine import Pin
from motor_library import movement, servo1, servo2, stop_all, check_stop, is_running

# ---------------- Buttons ----------------
button_start = Pin(34, Pin.IN, Pin.PULL_DOWN)  # Start/resume
button_stop = Pin(0, Pin.IN, Pin.PULL_UP)      # Emergency stop

stop_all()
print("All motors stopped.")

while True:
    # Wait until start button is pressed
    print("Waiting for START button (D34)...")
    while button_start.value() == 0:
        check_stop()  # Emergency stop has highest priority
        time.sleep(0.1)

    print("START pressed. Running sequence...")
    
    # Move servos
    servo1.write_angle(90)
    check_stop()
    time.sleep(1)
    servo1.write_angle(0)
    check_stop()
    time.sleep(1)

    servo2.write_angle(45)
    check_stop()
    time.sleep(1)
    servo2.write_angle(135)
    check_stop()
    time.sleep(1)

    # Run mecanum movements
    movement("FORWARD", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("BACKWARD", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("TURN_RIGHT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("TURN_LEFT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("GLIDE_RIGHT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("GLIDE_LEFT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("FORWARD_RIGHT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("BACKWARD_LEFT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("FORWARD_LEFT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    movement("BACKWARD_RIGHT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)

    stop_all()
    print("Sequence completed. All motors stopped.")
    
    # After finishing, wait for START again
    while button_start.value() == 0:
        check_stop()
        time.sleep(0.1)

