from matrix_library import shapes as s, canvas as c, controller as con
import time

controller = con.Controller()
canvas = c.Canvas()
polygon = s.Polygon(s.get_polygon_vertices(5, 20, (64, 64)), (100, 0, 0))
polygon2 = s.Polygon(s.get_polygon_vertices(3, 70, (64, 64)), (0, 100, 0))

toggle = False


def show_shape():
    global toggle
    toggle = not toggle


controller.add_function("UP", show_shape)

while True:
    canvas.clear()

    polygon.rotate(1, (64, 64))

    if toggle:
        canvas.add(polygon)

    canvas.draw()
    time.sleep(0)
