import sys
import io
import time
import datetime
from flask import Flask, Response, request

try:
  import picamera
except:
  sys.exit(0)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def capture_photo():
  try:
    with picamera.PiCamera(sensor_mode=3) as camera:
      camera.resolution = (3280, 2464)
      camera.hflip = True
      camera.vflip = True
      camera.annotate_background = picamera.Color('black')
      camera.annotate_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      camera.annotate_text_size = 100
      time.sleep(2) # warmup for camera
      stream = io.BytesIO()
      camera.capture(stream, format='jpeg', use_video_port=True)
      stream.seek(0)
  except:
    return 'Error: camera is unavailable!', 503
  return Response(stream.read(), mimetype='image/jpeg')


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False)
