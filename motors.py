from machine import Pin, PWM
import time

# ---------------- Motor Pins ----------------
motor_pins = {
    "front_left": {"pwm": 25, "dir": 23},
    "front_right": {"pwm": 18, "dir": 19},
    "back_left": {"pwm": 17, "dir": 16},
    "back_right": {"pwm": 13, "dir": 14}
}

# ---------------- Initialize Motors ----------------
motors = {}
for name, pins in motor_pins.items():
    motors[name] = {
        "pwm": PWM(Pin(pins["pwm"]), freq=50),
        "dir": Pin(pins["dir"], Pin.OUT)
    }

# ---------------- Motor Functions ----------------
def run_motor(name, speed, direction):
    """Run motor with speed 0-1023 and direction 0 or 1"""
    if name in motors:
        motors[name]["dir"].value(direction)
        motors[name]["pwm"].duty(speed)

def stop_motor(name):
    """Stop specific motor"""
    if name in motors:
        motors[name]["pwm"].duty(0)

def stop_all():
    """Stop all motors"""
    for name in motors:
        stop_motor(name)

# ---------------- Servo (software PWM) ----------------
class Servo:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
    
    def write_angle(self, angle):
        angle = max(0, min(180, angle))
        pulse = int(500 + (angle / 180) * 2000)  # microseconds
        self.pin.value(1)
        time.sleep_us(pulse)
        self.pin.value(0)
        time.sleep_ms(20)  # 50Hz repetition

# ---------------- Servo Instances ----------------
servo1 = Servo(33)
servo2 = Servo(32)
servo3 = Servo(27)
servo4 = Servo(26)

