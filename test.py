import matrix_library as m

canvas = m.Canvas()
polygon = m.Polygon(m.get_polygon_vertices(5, 20, (64,96)), (255, 0, 0))
polygon.rotate(45, (64, 96))
circle = m.Circle(10, (64,64), (0, 255, 0))
line = m.Line((0, 0), (128, 128), (0, 0, 255))

canvas.add(polygon)
canvas.add(circle)
canvas.add(line)
while True:
  canvas.draw()