# python 3.11

import random
from paho.mqtt import client as mqtt_client


RPI = False

if RPI:
    import control
    import time


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'emqx'
password = 'abcd'

if RPI:
    pwm = control.controlInit()


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            data = int(msg.payload.decode())
            print('Received data:', data)
            if data == 0:
                if RPI:
                    control.Rotate_Right(100)
                    time.sleep(1)
                    control.servo(pwm,120)
                    time.sleep(3)
                    control.servo(pwm,0)
                    time.sleep(1)
                    control.Rotate_Left(100)
                print(f"current mode is plastic bottle {data}")
            elif data == 1:
                if RPI:
                    control.Rotate_Right(180)
                    time.sleep(1)
                    control.servo(pwm,120)
                    time.sleep(3)
                    control.servo(pwm,0)
                    time.sleep(1)
                    control.Rotate_Left(100)
                print(f"current mode is cans {data}")
            elif data == 2:
                if RPI:
                    control.Rotate_Right(100)
                    time.sleep(1)
                    control.servo(pwm,120)
                    time.sleep(3)
                    control.servo(pwm,0)
                    time.sleep(1)
                    control.Rotate_Left(100)
                print(f"current mode is glass bottle {data}")
            return data
        except Exception as e:
            print('Error:', str(e))
            if RPI:
                control.release(pwm)
            return data




    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
