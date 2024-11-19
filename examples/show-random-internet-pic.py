# Imports
from PIL import Image
import time
import requests
import io
import sys
from matrix_library import canvas as c, shapes as s

def exit_prog():
    print(quit)
    # canvas.delete()
    sys.exit()

# random picture URL
w = h = 128
url = f"https://picsum.photos/{w}"

#canvas = c.Canvas(renderMode="zmq",zmqRenderTarget="localhost",zmqRenderPort=5500)
canvas = c.Canvas()
canvas.clear()

r = requests.get(url, stream=True)
if r.status_code == 200:
    img = Image.open(io.BytesIO(r.content))
    pixels = list(img.getdata())
    #print(pixels)

    img = s.Image(width=128,height=128,position=[0,0])
    img.loadpixels(pixels)

    canvas.add(img)
    canvas.draw()

    time.sleep(10)