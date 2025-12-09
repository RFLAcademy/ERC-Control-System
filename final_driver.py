from machine import Pin, PWM
import time

# Replace default wait with safety-checked wait
def wait(duration):
    interval = 0.05
    elapsed = 0
    while elapsed < duration:
        check_stop()
        if not _running:
            stop_all()
            return
        time.sleep(interval)
        elapsed += interval


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
        check_stop()
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
    "EIGHT": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "NINE": {
        "front_left": {"pwm": 23, "dir": 25},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 16, "dir": 17},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "TEN": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "ELEVEN": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
    "TWELVE": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "SIXTEEN": {
        "front_left": {"pwm": 5, "dir": 4},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 23, "dir": 25},
    },
    "THIRTY": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 16, "dir": 17},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
}


# ---------------- Global Motors ----------------
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
    check_stop()
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
button_stop = Pin(0, Pin.IN, Pin.PULL_UP)
led_warning = Pin(2, Pin.OUT)
buzzer_pin = Pin(15, Pin.OUT)


def wait_for_start():
    global _running
    print("Waiting for START button (D34)...")
    while button_start.value() == 0:
        wait(0.01)
    print("START pressed!")
    _running = True


def check_stop():
    global _running
    if button_stop.value() == 0:
        stop_all()
        _running = False
        print("EMERGENCY STOP! LED blinking for 5 sec...")

        # Blink LED for 5 seconds
        blink_time = 5
        interval = 0.2
        elapsed = 0
        while elapsed < blink_time:
            led_warning.value(1)
            time.sleep(interval)
            led_warning.value(0)
            time.sleep(interval)
            elapsed += interval * 2

        print("Waiting for STOP release...")
        while button_stop.value() == 0:
            time.sleep(0.05)

        led_warning.value(0)  # Ensure LED off after release
        
def led_on():
    led_warning.value(1)

def led_off():
    led_warning.value(0)
    
def buzz(duration, times):
    if times <= 0 or duration <= 0:
        return

    interval = duration / (times * 2)  # ON + OFF cycles

    for _ in range(times):
        buzzer_pin.value(1)
        time.sleep(interval)
        buzzer_pin.value(0)
        time.sleep(interval)


def is_running():
    return _running


# ---------------- Movements ----------------
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
        
    elif motion == "L":  # Strafe Left
        motors["front_left"]["dir"].value(1)
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(0)

    elif motion == "R":  # Strafe Right
        motors["front_left"]["dir"].value(0)
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(1)

    elif motion == "FL":  # Forward Left Diagonal
        motors["front_right"]["dir"].value(1)
        motors["back_left"]["dir"].value(0)
        motors["front_left"]["pwm"].duty(0)
        motors["back_right"]["pwm"].duty(0)

    elif motion == "FR":  # Forward Right Diagonal
        motors["front_left"]["dir"].value(0)
        motors["back_right"]["dir"].value(1)
        motors["front_right"]["pwm"].duty(0)
        motors["back_left"]["pwm"].duty(0)

    elif motion == "BL":  # Backward Left Diagonal
        motors["front_right"]["dir"].value(0)
        motors["back_left"]["dir"].value(1)
        motors["front_left"]["pwm"].duty(0)
        motors["back_right"]["pwm"].duty(0)

    elif motion == "BR":  # Backward Right Diagonal
        motors["front_left"]["dir"].value(1)
        motors["back_right"]["dir"].value(0)
        motors["front_right"]["pwm"].duty(0)
        motors["back_left"]["pwm"].duty(0)

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

    elapsed = 0
    interval = 0.05
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

        time.sleep(interval)
        elapsed += interval

    stop_all()


