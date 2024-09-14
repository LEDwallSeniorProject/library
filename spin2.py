from matrix_library import shapes as s, canvas as c
import time

canvas = c.Canvas()
triangle = s.Polygon(s.get_polygon_vertices(3, 20, (32,32)), (255, 0, 0))
square = s.Polygon(s.get_polygon_vertices(4, 20, (96,32)), (0, 255, 0))
pentagon = s.Polygon(s.get_polygon_vertices(5, 20, (64,64)), (0, 0, 255))
hexagon = s.Polygon(s.get_polygon_vertices(6, 20, (32,96)), (255, 255, 0))
heptagon = s.Polygon(s.get_polygon_vertices(7, 20, (96,96)), (0, 255, 255))

polygons = [triangle, square, pentagon, hexagon, heptagon]

while True:
  canvas.clear()
  for polygon in polygons:
    polygon.rotate(1, (polygon.center[0], polygon.center[1]))
    canvas.add(polygon)
  canvas.draw()
  time.sleep(0)