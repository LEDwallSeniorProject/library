from matrix_library import shapes as s, canvas as c

canvas = c.Canvas()
polygon = s.Polygon(s.get_polygon_vertices(5, 20, (64,96)), (255, 0, 0))
polygon.rotate(45, (64, 96))
circle = s.Circle(10, (64,64), (0, 255, 0))
line = s.Line((0, 0), (128, 128), (0, 0, 255))
letter_a = s.Letter('A', [0, 0], [255, 255, 255], size=8)
letter_a.image.show() 

canvas.add(polygon)
canvas.add(circle)
canvas.add(line)
canvas.add(letter_a)
while True:
  canvas.draw()