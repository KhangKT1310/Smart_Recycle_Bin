from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import RPi.GPIO as GPIO
import time

# Đặt chế độ chân GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servo_pin = 16

# Đặt chân là OUTPUT
GPIO.setup(servo_pin, GPIO.OUT)

# Khởi tạo PWM với tần số 50Hz
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(7.5)


def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1.1)
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
        # Do something with the data, for example, return it in the response

        set_servo_angle(120)
        time.sleep(3)
        set_servo_angle(0)

        return jsonify({'success': True, 'data': data})
    except Exception as e:
        print('Error:', str(e))
        pwm.stop()
        GPIO.cleanup()
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    #  app.run(debug=True)
    app.run(debug=True, host='localhost',
            port=8080, threaded=True, processes=1)
