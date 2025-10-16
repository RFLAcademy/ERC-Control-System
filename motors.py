from machine import Pin, PWM

# ---------------- Motor Pins ----------------
motor_pins = {
    "front_left": {"pwm": 25, "dir": 23},
    "front_right": {"pwm": 18, "dir": 19},
    "back_left": {"pwm": 17, "dir": 16},
    "back_right": {"pwm": 13, "dir": 14},
    "extra_motor": {"pwm": 4, "dir": 5},
}

# Initialize PWM and DIR pins
motors = {}
for name, pins in motor_pins.items():
    motors[name] = {
        "pwm": PWM(Pin(pins["pwm"]), freq=50),
        "dir": Pin(pins["dir"], Pin.OUT)
    }

# ---------------- Motor Functions ----------------
def run_motor(name, speed, direction=1):
    """Run a motor at given speed and direction (1=forward, 0=reverse)."""
    motors[name]["dir"].value(direction)
    motors[name]["pwm"].duty(speed)

def stop_motor(name):
    run_motor(name, 0, 0)

def stop_all():
    for name in motors:
        stop_motor(name)
