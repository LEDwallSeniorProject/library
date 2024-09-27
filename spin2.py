import matrix_library as m
import time

canvas = m.Canvas()
thickness = 2
triangle = m.PolygonOutline(m.get_polygon_vertices(3, 20, (32,32)), (255, 0, 0), thickness)
square = m.PolygonOutline(m.get_polygon_vertices(4, 20, (96,32)), (0, 255, 0), thickness)
pentagon = m.PolygonOutline(m.get_polygon_vertices(5, 20, (64,64)), (0, 0, 255), thickness)
hexagon = m.PolygonOutline(m.get_polygon_vertices(6, 20, (32,96)), (255, 255, 0), thickness)
heptagon = m.PolygonOutline(m.get_polygon_vertices(7, 20, (96,96)), (0, 255, 255), thickness)

polygons = [triangle, square, pentagon, hexagon, heptagon]

while True:
  canvas.clear()
  for polygon in polygons:
    polygon.rotate(1, (polygon.center[0], polygon.center[1]))
    canvas.add(polygon)
  canvas.draw()
  time.sleep(0)