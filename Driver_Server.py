from flask import Flask
import socket
import RPi.GPIO as GPIO
import time
import wave
import pyaudio

def setup():
    for i in rnage(3):
        GPIO.output(motor1, True)
        time.sleep(0.5)
        GPIO.output(motor1, False)
        time.sleep(0.5)

# 오디오 파일 재생 함수
def play_audio(file_path):
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(1024)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()

GPIO.setwarnings(False)
app = Flask(__name__)

@app.route('/')
def hello():
    return "hello"

@app.route('/wakeup')
def wakeup():
    global handler
    GPIO.output(motor1, True)
    play_audio("/home/raspberrypi/Junee/ALERT.wav")
    GPIO.output(motor1, False)
    return "wakeup"
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    motor1 = 26
    GPIO.setup(motor1, GPIO.OUT)

    app.run(host = "192.168.211.38", port = 9999)
    # app.run(host = "192.168.0.103" , port = 9999)
        
