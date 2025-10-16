from machine import Pin, PWM
import time

# ---------------- Servo Class ----------------
class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
    def write_angle(self, angle):
        angle = max(0, min(180, angle))
        duty = int(40 + (angle / 180) * 75)
        self.pwm.duty(duty)

# ---------------- Servo Instances ----------------
servo1 = Servo(33)
servo2 = Servo(32)
servo3 = Servo(27)
servo4 = Servo(26)

# ---------------- Motor Pins ----------------
motor_pins = {
    "front_left": {"pwm": 25, "dir": 23},
    "front_right": {"pwm": 18, "dir": 19},
    "back_left": {"pwm": 17, "dir": 16},
    "back_right": {"pwm": 13, "dir": 14},
    "extra_motor": {"pwm": 4, "dir": 5},
}

# ---------------- Initialize Motors ----------------
motors = {}
for name, pins in motor_pins.items():
    motors[name] = {
        "pwm": PWM(Pin(pins["pwm"]), freq=50),
        "dir": Pin(pins["dir"], Pin.OUT)
    }

# ---------------- Motor Functions ----------------
def run_motor(name, speed, direction=1):
    if name in motors:
        motors[name]["dir"].value(direction)
        motors[name]["pwm"].duty(speed)

def stop_motor(name):
    if name in motors:
        motors[name]["pwm"].duty(0)

def stop_all():
    for name in motors:
        stop_motor(name)

# ---------------- Buttons ----------------
button_motor = Pin(34, Pin.IN, Pin.PULL_DOWN)  # Start/resume
button_stop = Pin(0, Pin.IN, Pin.PULL_UP)      # Emergency stop

# ---------------- Control Container ----------------
_running = False

def check_stop():
    """Emergency stop (D0) and resume (D34)."""
    global _running
    # Emergency stop
    if button_stop.value() == 0:
        stop_all()
        _running = False
        print("EMERGENCY STOP!")
        while button_stop.value() == 0:
            time.sleep(0.1)
    # Resume
    if button_motor.value() == 1:
        _running = True
        print("NORMAL OPERATION STARTED")
        time.sleep(0.3)

def is_running():
    """Return current robot running state."""
    return _running

# ---------------- Robot Movements ----------------
def movement(motion, speed=1023, duration=1.5):
    if not _running:
        stop_all()
        return

    if motion == "FORWARD":
        motors["front_left"]["dir"].value(0)
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(1)
    elif motion == "BACKWARD":
        motors["front_left"]["dir"].value(1)
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(0)
    elif motion == "TURN_LEFT":
        motors["front_left"]["dir"].value(1)
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(1)
    elif motion == "TURN_RIGHT":
        motors["front_left"]["dir"].value(0)
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(0)
    elif motion == "GLIDE_RIGHT":
        motors["front_left"]["dir"].value(1)
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(0)
    elif motion == "GLIDE_LEFT":
        motors["front_left"]["dir"].value(0)
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(1)
    elif motion == "FORWARD_RIGHT":
        motors["front_left"]["dir"].value(0)
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(1)
    elif motion == "FORWARD_LEFT":
        motors["front_left"]["dir"].value(0)
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(0)
    elif motion == "BACKWARD_RIGHT":
        motors["front_left"]["dir"].value(1)
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(1)
    elif motion == "BACKWARD_LEFT":
        motors["front_left"]["dir"].value(1)
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(0)
    else:
        print("Unknown motion:", motion)
        return

    interval = 0.05
    elapsed = 0
    while elapsed < duration:
        if not _running:
            stop_all()
            return
        for m in motors:
            motors[m]["pwm"].duty(speed)
        time.sleep(interval)
        elapsed += interval
    stop_all()

