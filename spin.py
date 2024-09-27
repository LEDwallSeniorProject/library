import matrix_library as m
import time

canvas = m.Canvas()
polygon = m.Polygon(m.get_polygon_vertices(5, 20, (64,64)), (255, 0, 0))

while True:
  canvas.clear()
  polygon.rotate(1, (64, 64))
  canvas.add(polygon)
  canvas.draw()
  time.sleep(0)