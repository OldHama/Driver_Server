from flask import Flask
import socket
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
app = Flask(__name__)

@app.route('/')
def hello():
    return "hello"

@app.route('/wakeup')
def wakeup():
    global handler
    GPIO.output(motor1, True)
    time.sleep(10)
    GPIO.output(motor1, False)
    return "wakeup"
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    motor1 = 26
    GPIO.setup(motor1, GPIO.OUT)
    app.run(host = "192.168.211.38", port = 9999)
    # app.run(host = "192.168.0.103" , port = 9999)
        
