from matrix_library import canvas as c, shapes as s

canvas = c.Canvas()

while True:
  canvas.clear()
  canvas.add(s.Pixel((64,64)))
  canvas.draw()