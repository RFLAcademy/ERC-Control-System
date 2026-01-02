from machine import Pin, PWM, I2C, ADC
import time
import machine
import ssd1306

# -------- OLED INIT --------
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def oled_clear():
    oled.fill(0)
    oled.show()

def oled_status(line1="", line2="", line3="", line4=""):
    oled.fill(0)
    oled.text(line1, 0, 0)
    oled.text(line2, 0, 18)
    oled.text(line3, 0, 36)
    oled.text(line4, 0, 55)
    oled.show()

def oled_mode(mode):
    oled.fill(0)
    oled.text("MODE", 40, 0)
    oled.text(mode, 40, 25)
    oled.show()
    
_adc1 = ADC(Pin(39))  # VN
_adc2 = ADC(Pin(36))  # VP
_adc3 = ADC(Pin(35))  # D35

for a in (_adc1, _adc2, _adc3):
    a.atten(ADC.ATTN_11DB)
    a.width(ADC.WIDTH_12BIT)

THRESHOLD = 2000   # set once here

# ===== HARD FAIL-SAFE RESET (runs after Thonny STOP, crash, reboot) =====

ALL_PWM_PINS = [4, 5, 13, 14, 16, 17, 18, 19, 23, 25]
ALL_DIR_PINS = [5, 4, 14, 13, 17, 16, 19, 18, 25, 23]

for p in ALL_PWM_PINS:
    try:
        PWM(Pin(p)).deinit()
    except:
        pass

for p in ALL_DIR_PINS:
    try:
        Pin(p, Pin.OUT).value(0)
    except:
        pass
# ======================================================================


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
        """
        position: float between 0.0 (min) and 1.0 (max)
        """
        position = max(0.0, min(1.0, position))
        # Convert normalized position to duty cycle (40-115)
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
        "front_left": {"pwm": 4, "dir": 5},
        "front_right": {"pwm": 13, "dir": 14},
        "back_left": {"pwm": 18, "dir": 19},
        "back_right": {"pwm": 17, "dir": 16},
        "extra_motor": {"pwm": 25, "dir": 23},
    },
    "TWO": {
        "front_left": {"pwm": 18, "dir": 19},
        "front_right": {"pwm": 23, "dir": 25},
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
    "THIRTEEN": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 18, "dir": 19},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 13, "dir": 14},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "FOURTEEN": {
        "front_left": {"pwm": 5, "dir": 4},
        "front_right": {"pwm": 14, "dir": 13},
        "back_left": {"pwm": 18, "dir": 19},
        "back_right": {"pwm": 16, "dir": 17},
        "extra_motor": {"pwm": 25, "dir": 23},
    },
    "FIFTEEN": {
        "front_left": {"pwm": 19, "dir": 18},
        "front_right": {"pwm": 17, "dir": 16},
        "back_left": {"pwm": 13, "dir": 14},
        "back_right": {"pwm": 4, "dir": 5},
        "extra_motor": {"pwm": 25, "dir": 13},
    },
    "SIXTEEN": {
        "front_left": {"pwm": 5, "dir": 4},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 23, "dir": 25},
    },
    "SEVENTEEN": {
        "front_left": {"pwm": 18, "dir": 19},
        "front_right": {"pwm": 23, "dir": 25},
        "back_left": {"pwm": 13, "dir": 14},
        "back_right": {"pwm": 17, "dir": 16},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
    "EIGHTEEN": {
        "front_left": {"pwm": 14, "dir": 13},
        "front_right": {"pwm": 5, "dir": 4},
        "back_left": {"pwm": 18, "dir": 19},
        "back_right": {"pwm": 16, "dir": 17},
        "extra_motor": {"pwm": 23, "dir": 25},
    },
    "NINETEEN": {
        "front_left": {"pwm": 18, "dir": 19},
        "front_right": {"pwm": 23, "dir": 25},
        "back_left": {"pwm": 13, "dir": 14},
        "back_right": {"pwm": 16, "dir": 17},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "TWENTY": {
        "front_left": {"pwm": 18, "dir": 19},
        "front_right": {"pwm": 16, "dir": 17},
        "back_left": {"pwm": 13, "dir": 14},
        "back_right": {"pwm": 4, "dir": 5},
        "extra_motor": {"pwm": 23, "dir": 25},
    },
    "TWENTYONE": {
        "front_left": {"pwm": 17, "dir": 16},
        "front_right": {"pwm": 14, "dir": 13},
        "back_left": {"pwm": 25, "dir": 23},
        "back_right": {"pwm": 19, "dir": 18},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "TWENTYTWO": {
        "front_left": {"pwm": 18, "dir": 19},
        "front_right": {"pwm": 17, "dir": 16},
        "back_left": {"pwm": 13, "dir": 14},
        "back_right": {"pwm": 25, "dir": 23},
        "extra_motor": {"pwm": 4, "dir": 5},
    },
    "TWENTYTHREE": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
    "TWENTYFOUR": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 17, "dir": 16},
        "back_left": {"pwm": 14, "dir": 13},
        "back_right": {"pwm": 19, "dir": 18},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
    "TWENTYFIVE": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
    "TWENTYSIX": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
    "TWENTYSEVEN": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
    "TWENTYEIGHT": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
    "TWENTYNINE": {
        "front_left": {"pwm": 25, "dir": 23},
        "front_right": {"pwm": 19, "dir": 18},
        "back_left": {"pwm": 17, "dir": 16},
        "back_right": {"pwm": 14, "dir": 13},
        "extra_motor": {"pwm": 5, "dir": 4},
    },
}


# ---------------- Global Motors ----------------
motors = {}
_running = False
_current_motion = None


def set_motor_config(config_id):
    global motors
    if config_id not in motor_configs:
        raise ValueError("Invalid config ID")

    _reset_all_pwm_and_dir()

    motors = {}
    for name, pin in motor_configs[config_id].items():
        motors[name] = {
            "pwm": PWM(Pin(pin["pwm"]), freq=50),
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

        print("EMERGENCY STOP! System halted.")
        oled_status("SYSTEM STOPPED", "Press START", "", "")
        led_warning.value(1)

        # Wait until STOP released
        while button_stop.value() == 0:
            time.sleep(0.05)

        # Wait for START press
        while button_start.value() == 0:
            time.sleep(0.05)

        print("Restarting system...")
        led_warning.value(0)
        time.sleep(0.2)

        machine.reset()   # 🔁 FULL RESTART

        
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
    
    # ---------------- NON-BLOCKING MOTOR CONTROL ----------------
def run(name, speed=100, direction=1):
    check_stop()
    if name in motors:
        motors[name]["dir"].value(direction)
        duty = int(max(0, min(100, speed)) * 1023 // 100)
        motors[name]["pwm"].duty(duty)

def stop(name):
    if name in motors:
        motors[name]["pwm"].duty(0)
        
# ================= NON-BLOCKING MOVEMENTS =================

MIN_DUTY = 520   # tune between 200–350 depending on motors

def _calc_duty(speed):
    speed = max(0, min(100, speed))
    if speed == 0:
        return 0
    duty = int(speed * 1023 // 100)
    return max(duty, MIN_DUTY)


def FW(speed=100):
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "FW" 
    duty = _calc_duty(speed)

    motors["front_left"]["dir"].value(0)
    motors["front_right"]["dir"].value(1)
    motors["back_left"]["dir"].value(0)
    motors["back_right"]["dir"].value(1)

    for m in ["front_left","front_right","back_left","back_right"]:
        motors[m]["pwm"].duty(duty)


def BW(speed=100):
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "BW" 
    duty = _calc_duty(speed)

    motors["front_left"]["dir"].value(1)
    motors["front_right"]["dir"].value(0)
    motors["back_left"]["dir"].value(1)
    motors["back_right"]["dir"].value(0)

    for m in ["front_left","front_right","back_left","back_right"]:
        motors[m]["pwm"].duty(duty)


def L(speed=100):
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "L" 
    duty = _calc_duty(speed)

    motors["front_left"]["dir"].value(1)
    motors["front_right"]["dir"].value(1)
    motors["back_left"]["dir"].value(0)
    motors["back_right"]["dir"].value(0)

    for m in ["front_left","front_right","back_left","back_right"]:
        motors[m]["pwm"].duty(duty)


def R(speed=100):
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "R" 
    duty = _calc_duty(speed)

    motors["front_left"]["dir"].value(0)
    motors["front_right"]["dir"].value(0)
    motors["back_left"]["dir"].value(1)
    motors["back_right"]["dir"].value(1)

    for m in ["front_left","front_right","back_left","back_right"]:
        motors[m]["pwm"].duty(duty)


def CCW(speed=100):
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "CCW" 
    duty = _calc_duty(speed)

    for m in ["front_left","front_right","back_left","back_right"]:
        motors[m]["dir"].value(1)
        motors[m]["pwm"].duty(duty)


def CW(speed=100):
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "CW" 
    duty = _calc_duty(speed)

    for m in ["front_left","front_right","back_left","back_right"]:
        motors[m]["dir"].value(0)
        motors[m]["pwm"].duty(duty)


def FL(speed=100):  # Forward Left
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "FL" 
    duty = _calc_duty(speed)

    motors["front_right"]["dir"].value(1)
    motors["back_left"]["dir"].value(0)

    motors["front_right"]["pwm"].duty(duty)
    motors["back_left"]["pwm"].duty(duty)
    motors["front_left"]["pwm"].duty(0)
    motors["back_right"]["pwm"].duty(0)


def FR(speed=100):  # Forward Right
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "FR" 
    duty = _calc_duty(speed)

    motors["front_left"]["dir"].value(0)
    motors["back_right"]["dir"].value(1)

    motors["front_left"]["pwm"].duty(duty)
    motors["back_right"]["pwm"].duty(duty)
    motors["front_right"]["pwm"].duty(0)
    motors["back_left"]["pwm"].duty(0)


def BR(speed=100):  # Backward Left
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "BR" 
    duty = _calc_duty(speed)

    motors["front_right"]["dir"].value(0)
    motors["back_left"]["dir"].value(1)

    motors["front_right"]["pwm"].duty(duty)
    motors["back_left"]["pwm"].duty(duty)
    motors["front_left"]["pwm"].duty(0)
    motors["back_right"]["pwm"].duty(0)


def BL(speed=100):  # Backward Right
    global _current_motion
    check_stop()
    if not _running:
        stop_all(); return
    _current_motion = "BL" 
    duty = _calc_duty(speed)

    motors["front_left"]["dir"].value(1)
    motors["back_right"]["dir"].value(0)

    motors["front_left"]["pwm"].duty(duty)
    motors["back_right"]["pwm"].duty(duty)
    motors["front_right"]["pwm"].duty(0)
    motors["back_left"]["pwm"].duty(0)
    
def stop_drive(motion=None):
    global _current_motion
    stop_all()
    _current_motion = None

def sensor_1():
    if _adc1.read() > THRESHOLD:
        return 1 
    else:
        return 0

def sensor_2():
    if _adc2.read() > THRESHOLD:
        return 1
    else:
        return 0

def sensor_3():
    if _adc3.read() > THRESHOLD:
        return 1
    else:
        return 0


