import sys
import matrix_library as matrix
import time

controller = matrix.Controller()
canvas = matrix.Canvas()
polygon = matrix.Polygon(matrix.get_polygon_vertices(5, 20, (64, 64)), (100, 0, 0))
polygon2 = matrix.Polygon(matrix.get_polygon_vertices(3, 70, (64, 64)), (0, 100, 0))

toggle = False
exited = False

def exit_prog():
    global canvas, exited
    print("quit")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

def show_shape():
    global toggle
    toggle = not toggle

controller.add_function("UP", show_shape)
controller.add_function("START", exit_prog)

while True:
    if exited: sys.exit(0)
    canvas.clear()
    polygon.rotate(1, (64, 64))

    if toggle:
        canvas.add(polygon)

    canvas.draw()
    time.sleep(0)
