from machine import Pin, PWM
import time

wait = time.sleep

# ---------------- FAIL-SAFE MOTOR RESET ----------------
def _reset_all_pwm_and_dir():
    used_pwm_pins = set()
    used_dir_pins = set()

    for cfg in motor_configs.values():
        for motor in cfg.values():
            used_pwm_pins.add(motor["pwm"])
            used_dir_pins.add(motor["dir"])

    for p in used_pwm_pins:
        try:
            PWM(Pin(p)).deinit()
        except:
            pass

    for p in used_dir_pins:
        try:
            Pin(p, Pin.OUT).value(0)
        except:
            pass


# ---------------- Servo Class ----------------
class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)

    def pos(self, position):
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
    "ONE": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "TWO": {
        "front_left": {"pwm": 23, "dir": 25},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 16, "dir": 17},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "THREE": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "FOUR": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "FIVE": {
        "front_left": {"pwm": 23, "dir": 25},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 16, "dir": 17},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "SIX": {
        "front_left": {"pwm": 23, "dir": 25},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 16, "dir": 17},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "SEVEN": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "ELEVEN": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 16, "dir": 17},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
}


# ---------------- Global motors ----------------
motors = {}
_running = False


def set_motor_config(config_id):
    global motors
    if config_id not in motor_configs:
        raise ValueError("Invalid config ID")

    _reset_all_pwm_and_dir()

    motors = {}
    for name, pin in motor_configs[config_id].items():
        motors[name] = {
            "pwm": PWM(Pin(pin["pwm"]), freq=1000),
            "dir": Pin(pin["dir"], Pin.OUT)
        }
        motors[name]["pwm"].duty(0)
        motors[name]["dir"].value(0)


# ---------------- Motor Functions ----------------
def run_motor(name, speed, duration, direction=1):
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
    for m in motors:
        try:
            motors[m]["pwm"].duty(0)
        except:
            pass


# ---------------- Buttons ----------------
button_start = Pin(34, Pin.IN, Pin.PULL_DOWN)
button_stop  = Pin(0, Pin.IN, Pin.PULL_UP)


def wait_for_start():
    global _running
    print("Waiting for START button (D34)...")
    while button_start.value() == 0:
        wait(0.01)
    print("START pressed!")
    _running = True


def check_stop():
    global _running

    # Emergency stop pressed
    if button_stop.value() == 0:
        stop_all()
        _running = False
        print("EMERGENCY STOP! Release button to continue.")
        while button_stop.value() == 0:
            wait(0.1)


def is_running():
    return _running


# ---------------- Robot Movements ----------------
def movement(motion, speed=100, duration=1.5, direction=1):
    global _running

    if not _running:
        stop_all()
        return

    duty = int(max(0, min(100, speed)) * 1023 // 100)

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
        for m in motors:
            motors[m]["dir"].value(1)

    elif motion == "CW":
        for m in motors:
            motors[m]["dir"].value(0)

    elif motion in motors:
        motors[motion]["dir"].value(direction)

    else:
        print("Unknown motion:", motion)
        return

    interval = 0.05
    elapsed = 0

    while elapsed < duration:
        check_stop()
        if not _running:
            stop_all()
            return

        if motion in motors:
            motors[motion]["pwm"].duty(duty)
        else:
            for m in motors:
                if m != "extra_motor":
                    motors[m]["pwm"].duty(duty)

        wait(interval)
        elapsed += interval

    stop_all()

