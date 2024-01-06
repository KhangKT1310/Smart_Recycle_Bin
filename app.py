from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import RPi.GPIO as GPIO
import time

# Đặt chế độ chân GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Định nghĩa chân GPIO cho A4988
DIR = 21  # Chân điều khiển hướng (Direction)
STEP = 20  # Chân điều khiển bước (Step)
ENABLE = 18  # Chân điều khiển enable (Enable)
SERVO_PIN = 16

# Đặt chân là OUTPUT
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENABLE, GPIO.OUT)

# Khởi tạo PWM với tần số 50Hz
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)
# Đặt hướng đi mặc định (ví dụ: bước tiến)
GPIO.output(DIR, GPIO.HIGH)
# Kích hoạt motor (bằng cách thả chân ENABLE)
GPIO.output(ENABLE, GPIO.LOW)

def move_motor(steps, delay, direction):
    GPIO.output(DIR, direction) 
    for _ in range(steps):
        # Bắt đầu quay motor
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)

def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)
    print("Servo on angle = \n", angle)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'media'), path)


@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()['data']
        print('Received data:', data)
        if data == 0:
            move_motor(100, 0.001, GPIO.HIGH)
            time.sleep(2)
            set_servo_angle(120)
            time.sleep(5)
            set_servo_angle(0)
            time.sleep(2)
            move_motor(100, 0.001, GPIO.LOW)
        elif data == 1:
            move_motor(100, 0.001, GPIO.LOW)
            time.sleep(2)
            set_servo_angle(120)
            time.sleep(5)
            set_servo_angle(0)
            time.sleep(2)
            move_motor(100, 0.001, GPIO.HIGH)
        elif data == 2:
            move_motor(300, 0.001, GPIO.HIGH)
            time.sleep(2)
            set_servo_angle(120)
            time.sleep(5)
            set_servo_angle(0)
            time.sleep(2)
            move_motor(300, 0.001, GPIO.LOW)
        


            
        # move_motor(350, 0.001, GPIO.HIGH)
        # Do something with the data, for example, return it in the response
        #set_servo_angle(120)
        #time.sleep(3)
        #set_servo_angle(0)
        #time.sleep(3)

        return jsonify({'success': True, 'data': data})
    except Exception as e:
        print('Error:', str(e))
        pwm.stop()
        GPIO.cleanup()
        GPIO.output(ENABLE, GPIO.HIGH)
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    #  app.run(debug=True)
    app.run(debug=True, host='localhost',
            port=8080, threaded=True, processes=1)


