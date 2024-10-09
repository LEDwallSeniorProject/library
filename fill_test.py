from matrix_library import canvas as c, shapes as s
import random
import time

# Define dimensions
width = 128
height = 128

# colors = [
#     ("black", (0, 0, 0)),
#     ("silver", (192, 192, 192)),
#     ("gray", (128, 128, 128)),
#     ("white", (255, 255, 255)),
#     ("maroon", (128, 0, 0)),
#     ("red", (255, 0, 0)),
#     ("purple", (128, 0, 128)),
#     ("fuchsia", (255, 0, 255)),
#     ("green", (0, 128, 0)),
#     ("lime", (0, 255, 0)),
#     ("olive", (128, 128, 0)),
#     ("yellow", (255, 255, 0)),
#     ("navy", (0, 0, 128)),
#     ("blue", (0, 0, 255)),
#     ("teal", (0, 128, 128)),
#     ("aqua", (0, 255, 255))
# ]

colors = [
  (255, 0, 0), # red
  (255,255,0), # yellow
  (0,0,255), # blue
  (128,0,128), # purple,
  (128,128,128) # gray
]
index = 0
canvas = c.Canvas()

while True:
    canvas.clear()
    canvas.fill(colors[index])
    canvas.draw()

    # increment and sleep
    index = (index+1) % len(colors)
    time.sleep(5)