from PIL import Image
import matrix_library as matrix
import zmq
import time
import requests
import io
import sys

# program setup
controller = matrix.Controller()
# canvas = matrix.Canvas()

def exit_prog():
    global canvas, exited
    print("quit")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

# Create the ZMQ connection
context = zmq.Context()

#  Socket to talk to server
#print("Connecting to LED ZMQ server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:55000")

# random picture URL
w = h = 128
url = f"https://picsum.photos/{w}"

controller.add_function("START", exit_prog)

for i in range(0,3):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        img = Image.open(io.BytesIO(r.content))
        # pixels = list(img.getdata())
        # print(pixels)

        # Convert the image to RGBA mode
        img = img.convert("RGBA")

        # covert to raw bytes
        rawimage = img.tobytes()

        # # send the request
        socket.send(rawimage)

        # #  Get the reply.
        message = socket.recv()

    for j in range(0,100):
        if exited: sys.exit(0)
        time.sleep(0.05)