import sys
import io
import time
import datetime
from flask import Flask, Response, request
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

try:
  import picamera
except:
  print("Cannot import picamera. Try 'pip install picamera'")
  sys.exit(0)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def capture_photo():
  GPIO.output(7, 1)
  try:
    with picamera.PiCamera(sensor_mode=3) as camera:
      camera.resolution = (3280, 2464)
      camera.hflip = True
      camera.vflip = True
      camera.annotate_background = picamera.Color('black')
      now = datetime.datetime.now()
      camera.annotate_text = now.strftime("%Y-%m-%d %H:%M:%S")
      camera.annotate_text_size = 100
      time.sleep(2) # warmup for camera
      stream = io.BytesIO()
      camera.capture(stream, format='jpeg', use_video_port=True)
      stream.seek(0)
  except:
    return 'Error: camera is unavailable!', 503
  
  GPIO.output(7, 0)
  filename = now.strftime("%Y_%m_%d_%H_%M_%S")
  r = Response(stream.read(), mimetype='image/jpeg')
  r.headers['Content-Disposition'] = 'inline; filename=qba_' + filename  + '.jpeg'
  r.headers['Cache-control'] = 'no-cache'
  return r

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False)
