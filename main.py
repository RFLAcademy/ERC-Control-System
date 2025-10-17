# main.py
from machine import Pin
from motor_library import movement, servo1, servo2, stop_all, check_stop, run_motor, wait

button_start = Pin(34, Pin.IN, Pin.PULL_DOWN)  # Start/resume

stop_all()
print("All motors stopped and system ready.")

while True:
    print("Waiting for START button (D34)...")

    while button_start.value() == 0:
        check_stop()
        wait(0.1)

    print("START pressed. Running sequence...")

    # ---------------- Servo Movements ----------------
    servo1.pos(0)
    check_stop()
    wait(1)

    servo1.pos(0.5)
    check_stop()
    wait(1)

    servo1.pos(1)
    check_stop()
    wait(1)

    servo1.pos(0)
    check_stop()
    wait(1)

    # ---------------- Mecanum Movements ----------------
    movement("FL", speed=100, duration=1.5)
    check_stop()
    wait(2)
    
    movement("FW", speed=100, duration=1.5)
    check_stop()
    wait(2)

    movement("BW", speed=10, duration=1.5)
    check_stop()
    wait(2)

    movement("CW", speed=100, duration=1.5)
    check_stop()
    wait(1)

    movement("CCW", speed=100, duration=1.5)
    check_stop()
    wait(1)

    movement("R", speed=100, duration=1.5)
    check_stop()
    wait(1)

    movement("L", speed=100, duration=1.5)
    check_stop()
    wait(1)

    movement("FR", speed=100, duration=1.5)
    check_stop()
    wait(1)

    movement("BL", speed=100, duration=1.5)
    check_stop()
    wait(1)

    movement("FL", speed=100, duration=1.5)
    check_stop()
    wait(1)

    movement("BR", speed=100, duration=1.5)
    check_stop()
    wait(1)

    stop_all()
    print("Sequence completed. All motors stopped.")

    while button_start.value() == 1:
        check_stop()
        wait(0.1)

