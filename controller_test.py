import matrix_library as matrix

canvas = matrix.Canvas()
controller = matrix.Controller()
polygon = matrix.Polygon(matrix.get_polygon_vertices(5, 20, (64, 64)), (255, 0, 0))

toggle = True


def toggle_toggle():
    global toggle
    toggle = not toggle


controller.add_function("UP", toggle_toggle)

while True:
    # controller.check_key_presses()
    canvas.clear()
    if toggle:
        polygon.rotate(1, (64, 64))
        canvas.add(polygon)
    canvas.draw()
