import matrix_library as matrix
import sys
import time

# Check if the user provided a filename
if len(sys.argv) < 2:
    print("Usage: python display-image.py <image_filename>")
    sys.exit(1)

# Get the filename from command line arguments
filename = sys.argv[1]

#canvas = c.Canvas(renderMode="zmq",zmqRenderTarget="localhost",zmqRenderPort=5500)
canvas = matrix.Canvas()
canvas.clear()

img = matrix.Image(width=128, height=128, position=[0,0])
img.loadfile(filename=filename)
# for i in img.pixels:
#     print(i)
canvas.add(img)
canvas.draw()

time.sleep(10)