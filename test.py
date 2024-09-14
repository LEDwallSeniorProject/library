from matrix_library import shapes as s, canvas as c

canvas = c.Canvas()
polygon = s.Polygon(s.get_polygon_vertices(5, 20, (64,96)), (255, 0, 0))
polygon.rotate(45, (64, 96))
circle = s.Circle(10, (64,64), (0, 255, 0))

canvas.add(polygon)
canvas.add(circle)
while True:
  canvas.draw()