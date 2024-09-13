from matrix_library import shapes as s, canvas as c
import time

canvas = c.Canvas()
circle = s.Circle(10, (64,96), (0, 255, 0))

velocity_y = 2
velocity_x = 3

while True:

  circle.translate(velocity_x, velocity_y)

  if circle.center[1] + circle.radius >= 128 or circle.center[1] - circle.radius <= 64:
    velocity_y *= -1
  if circle.center[0] + circle.radius >= 128 or circle.center[0] - circle.radius <= 0:
    velocity_x *= -1

  canvas.clear()
  canvas.add(circle)
  canvas.draw()
  time.sleep(0)