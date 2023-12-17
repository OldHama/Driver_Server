from flask import Flask
import socket
import RPi.GPIO as GPIO
import time
import wave 
from playsound import playsound
import threading
import pygame
import pyaudio
import logging
GPIO.setwarnings(False)
def process_requests(request_queue):
    while request_queue:
        request = request_queue.pop(0)
        wf = wave.open("/home/raspberrypi/Junee/ALERT.wav", 'rb')
        data = wf.readframes(1024)
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index = 0)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()
    
        p.terminate()
        print("fprocessing: {request}")
class RequestHandler:
    def __init__(self):
        self.lock = threading.Lock()
        self.thread = None
        
    def handle_request(self, request_queue):
        with self.lock:
            if self.thread is None or not self.thread.is_alive():
                self.thread= threading.Thread(target= process_requests, args= (request_queue,))
                self.thread.start()
            else:
                print("THE THREAD IS ALREADY RUNNING!")
'''
logging.basicConfig(filename = "/home/raspberrypi/Junee/server_log.log", level = logging.DEBUG)
file_handler = logging.FileHandler("/home/raspberrypi/Junee/server_log.log")
'''
app = Flask(__name__)
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('/home/raspberrypi/Junee/server_log.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
    '[in %(pathname)s:%(lineno)d]'
    ))
logger.addHandler(file_handler)
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {str(e)}")
    return "An error occurred", 500

@app.route('/')
def hello():

    return "hello"

@app.route('/vibration')
def vibration():
    GPIO.output(motor1, True)
    time.sleep(2)
    GPIO.output(motor1, False)
    return "vibration"

@app.route('/speaker')
def speaker():
    '''
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
        '''
    return "speaker"

@app.route('/wakeup')
def wakeup():
    global handler
    GPIO.output(motor1, True)
    handler.handle_request(request_queue)
    '''
    t1 = threading.Thread(target = run)
    t1.start()
    '''
    time.sleep(10)
    GPIO.output(motor1, False)
    return "wakeup"
def run():
    wf = wave.open("/home/raspberrypi/Junee/ALERT.wav", 'rb')
    data = wf.readframes(1024)
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index = 0)
    while data != '':
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    
    p.terminate()
    
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    motor1 = 26
    
    GPIO.setup(motor1, GPIO.OUT)
    request_queue = []
    handler = RequestHandler()
    
    app.run(host = "192.168.211.38", port = 9999)
    # app.run(host = "192.168.0.103" , port = 9999)
        
