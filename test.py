import time
from machine import Pin
from motor_library import movement, servo1, servo2, stop_all, check_stop, run_motor

# ---------------- Buttons ----------------
button_start = Pin(34, Pin.IN, Pin.PULL_DOWN)  # Start/resume
button_stop = Pin(0, Pin.IN, Pin.PULL_UP)      # Emergency stop

stop_all()
print("All motors stopped and system ready.")

while True:
    print("Waiting for START button (D34)...")

    # Wait until start button is pressed
    while button_start.value() == 0:
        check_stop()  # Always check stop first
        time.sleep(0.1)

    print("START pressed. Running sequence...")
    # ---------------- Servo Movements ----------------
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

    # ---------------- Mecanum Movements ----------------
    movement("FL", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)
    
    movement("FORWARD", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)

    movement("BACKWARD", speed=1023, duration=1.5)
    check_stop()
    time.sleep(2)

    movement("TURN_RIGHT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(1)

    movement("TURN_LEFT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(1)

    movement("GLIDE_RIGHT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(1)

    movement("GLIDE_LEFT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(1)

    movement("FORWARD_RIGHT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(1)

    movement("BACKWARD_LEFT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(1)

    movement("FORWARD_LEFT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(1)

    movement("BACKWARD_RIGHT", speed=1023, duration=1.5)
    check_stop()
    time.sleep(1)

    # ---------------- End of Sequence ----------------
    stop_all()
    print("Sequence completed. All motors stopped.")

    # Wait again for next start
    while button_start.value() == 0:
        check_stop()
        time.sleep(0.1)

