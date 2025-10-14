from machine import Pin, PWM, I2C
import ssd1306
import time

# ---------------- OLED Setup ----------------
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ---------------- Motor Pins ----------------
motors = {
    "A": {"pwm": 25, "dir": 23},  # Front Left
    "B": {"pwm": 18, "dir": 19},  # Front Right
    "C": {"pwm": 17, "dir": 16},  # Back Left
    "D": {"pwm": 13, "dir": 14},  # Back Right
}

# ---------------- Motor Init ----------------
motor_pwm = {}
motor_dir = {}
for key, pins in motors.items():
    motor_pwm[key] = PWM(Pin(pins["pwm"]), freq=50)
    motor_dir[key] = Pin(pins["dir"], Pin.OUT)

# ---------------- Button ----------------
button = Pin(0, Pin.IN, Pin.PULL_UP)

speed = 1023

def motor_run(name, speed, direction):
    # No reverse logic anymore; direction is directly specified in move
    motor_dir[name].value(direction)
    motor_pwm[name].duty(speed)

def stop_all():
    for m in motors:
        motor_pwm[m].duty(0)

def show_text(text):
    oled.fill(0)
    oled.text("MECANUM MODE", 10, 0)
    oled.text(text, 10, 25)
    oled.show()
    print(text)

def move(fl, fr, bl, br, label, duration=1.5):
    show_text(label)
    motor_run("A", fl[0], fl[1])
    motor_run("B", fr[0], fr[1])
    motor_run("C", bl[0], bl[1])
    motor_run("D", br[0], br[1])
    time.sleep(duration)
    stop_all()
    show_text("STOP")
    time.sleep(0.5)

# ---------------- Movement Functions ----------------
def forward(): move((speed,1),(speed,1),(speed,1),(speed,1),"FORWARD")
def backward(): move((speed,0),(speed,0),(speed,0),(speed,0),"BACKWARD")
def left(): move((speed,0),(speed,1),(speed,1),(speed,0),"LEFT")
def right(): move((speed,1),(speed,0),(0,0),(speed,1),"RIGHT")
def rotate_cw(): move((speed,1),(speed,0),(speed,1),(speed,0),"ROTATE CW")
def rotate_ccw(): move((speed,0),(speed,1),(speed,0),(speed,1),"ROTATE CCW")
def forward_left(): move((0,0),(speed,1),(speed,1),(0,0),"FORWARD LEFT")
def forward_right(): move((speed,1),(0,0),(0,0),(speed,1),"FORWARD RIGHT")
def backward_left(): move((speed,0),(0,0),(0,0),(speed,0),"BACKWARD LEFT")
def backward_right(): move((0,0),(speed,0),(speed,0),(0,0),"BACKWARD RIGHT")

# ---------------- Main Loop ----------------
stop_all()
show_text("RFL ERC")
time.sleep(3)
show_text("WAITING FOR BUTTON")

while True:
    if button.value() == 0:
        show_text("BUTTON PRESSED")
        time.sleep(0.3)  # debounce

        forward()
        backward()
        left()
        right()
        rotate_cw()
        rotate_ccw()
        forward_left()
        forward_right()
        backward_left()
        backward_right()

        while button.value() == 0:
            pass

        stop_all()
        show_text("WAITING FOR BUTTON")
