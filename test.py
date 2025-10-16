import time
from motors import run_motor, stop_motor, stop_all
stop_all()
print("Stop All")
# Run motors
run_motor("front_right", 800, 0)  # forward
print("front right")
time.sleep(2)

stop_motor("front_right")
print("Stop front right")
time.sleep(2)

run_motor("front_left", 800, 1)  # forward
print("front left")
time.sleep(2)

stop_motor("front_left")
print("stop front left")
time.sleep(2)

run_motor("back_right", 800, 0)  # reverse
print("back right")
time.sleep(2)

stop_motor("back_right")
print("stop back right")
time.sleep(2)

run_motor("back_left", 800, 1)  # reverse
print("back left")
time.sleep(2)

stop_motor("back_left")
print("Stop back left")
time.sleep(2)