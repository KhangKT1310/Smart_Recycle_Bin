import time
import RPi.GPIO as GPIO

# Define GPIO for A4988
DIR_PIN = 21  # Chân điều khiển hướng (Direction)
STEP_PIN = 20  # Chân điều khiển bước (Step)
ENABLE_PIN = 18  # Chân điều khiển enable (Enable)
SERVO_PIN = 16
STEP_DELAY_TIME = 0.001

def controlInit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # StepMotor Initialize
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(ENABLE_PIN, GPIO.OUT)
    
    GPIO.output(DIR_PIN, GPIO.HIGH)
    GPIO.output(ENABLE_PIN, GPIO.LOW)

    # Servo Initialize
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, 50) 
    pwm.start(0)
    return pwm

def Rotate_Right(steps):
    GPIO.output(DIR_PIN, GPIO.HIGH) 
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(STEP_DELAY_TIME)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(STEP_DELAY_TIME)

def Rotate_Left(steps):
    GPIO.output(DIR_PIN, GPIO.LOW) 
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(STEP_DELAY_TIME)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(STEP_DELAY_TIME)

def servo(pwm,angle):
    duty_cycle = (angle / 18.0) + 2
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)
    print("Servo on angle = \n", angle)

def release(pwm):
    pwm.stop()
    GPIO.cleanup()
    GPIO.output(ENABLE_PIN, GPIO.HIGH)