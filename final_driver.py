from machine import Pin, PWM
import time

wait = time.sleep

# ---------------- Servo Class ----------------
class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)

    def pos(self, position):
        """Position from 0.0 (min) to 1.0 (max)"""
        position = max(0.0, min(1.0, position))
        duty = int(40 + position * 75)
        self.pwm.duty(duty)

# ---------------- Servo Instances ----------------
servo1 = Servo(33)
servo2 = Servo(32)
servo3 = Servo(27)
servo4 = Servo(26)

# ---------------- Motor Configurations ----------------
motor_configs = {
    "A": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "B": {
        "front_left": {"pwm": 23, "dir": 25},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 16, "dir": 17},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "C": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "D": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "E": {
        "front_left": {"pwm": 23, "dir": 25},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 16, "dir": 17},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
}

# ---------------- Global motors ----------------
motors = {}

def set_motor_config(config_id):
    """Initialize motors based on config A–E"""
    global motors
    if config_id not in motor_configs:
        raise ValueError("Invalid config ID. Use A, B, C, D, or E")
    motors = {}
    pins = motor_configs[config_id]
    for name, p in pins.items():
        motors[name] = {
            "pwm": PWM(Pin(p["pwm"]), freq=50),
            "dir": Pin(p["dir"], Pin.OUT)
        }

# ---------------- Motor Functions ----------------
def run_motor(name, speed, duration, direction=1):
    """Run a single motor with speed 0–100"""
    if name in motors:
        motors[name]["dir"].value(direction)
        duty = int(max(0, min(100, speed)) * 1023 // 100)
        motors[name]["pwm"].duty(duty)
        wait(duration)
        motors[name]["pwm"].duty(0)

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
    """Emergency stop and resume"""
    global _running
    if button_stop.value() == 0:
        stop_all()
        _running = False
        print("EMERGENCY STOP!")
        while button_stop.value() == 0:
            wait(0.1)
    if button_motor.value() == 1:
        _running = True
        wait(0.3)

def is_running():
    return _running

# ---------------- Robot Movements ----------------
def movement(motion, speed=100, duration=1.5):
    """Mecanum robot movements, speed 0–100"""
    if not _running:
        stop_all()
        return

    duty = int(max(0, min(100, speed)) * 1023 // 100)

    # Direction setup
    if motion == "FW":
        motors["front_left"]["dir"].value(0)
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(1)
    elif motion == "BW":
        motors["front_left"]["dir"].value(1)
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(0)
    elif motion == "CCW":
        for m in ["front_left","front_right","back_left","back_right"]:
            motors[m]["dir"].value(1)
    elif motion == "CW":
        for m in ["front_left","front_right","back_left","back_right"]:
            motors[m]["dir"].value(0)
    elif motion == "R":
        motors["front_left"]["dir"].value(1)
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(0)
    elif motion == "L":
        motors["front_left"]["dir"].value(0)
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(1)
    # Additional mecanum moves
    elif motion == "FR":
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(0)
    elif motion == "FL":
        motors["front_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(1)
    elif motion == "BR":
        motors["front_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(0)
    elif motion == "BL":
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(1)
    elif motion == "front_left":
        motors["front_left"]["dir"].value(1)
    elif motion == "front_right":
        motors["front_right"]["dir"].value(1)
    elif motion == "back_left":
        motors["back_left"]["dir"].value(1)
    elif motion == "back_right":
        motors["back_right"]["dir"].value(1)
    else:
        print("Unknown motion:", motion)
        return

    # Movement execution
    interval = 0.05
    elapsed = 0
    while elapsed < duration:
        if not _running:
            stop_all()
            return
        # Apply PWM duty
        if motion in ["FR", "FL", "BR", "BL"]:
            if "FR" in motion:
                motors["front_right"]["pwm"].duty(duty)
                motors["back_left"]["pwm"].duty(duty)
            elif "FL" in motion:
                motors["front_left"]["pwm"].duty(duty)
                motors["back_right"]["pwm"].duty(duty)
            elif "BR" in motion:
                motors["front_left"]["pwm"].duty(duty)
                motors["back_right"]["pwm"].duty(duty)
            elif "BL" in motion:
                motors["front_right"]["pwm"].duty(duty)
                motors["back_left"]["pwm"].duty(duty)
        elif motion == "front_left":
            motors["front_left"]["pwm"].duty(duty)
        elif motion == "front_right":
            motors["front_right"]["pwm"].duty(duty)
        elif motion == "back_left":
            motors["back_left"]["pwm"].duty(duty)
        elif motion == "back_right":
            motors["front_right"]["pwm"].duty(duty)
        else:
            for m in motors:
                if m != "extra_motor":
                    motors[m]["pwm"].duty(duty)

        wait(interval)
        elapsed += interval

    stop_all()


