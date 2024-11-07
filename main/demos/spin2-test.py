from matrix_library import shapes as s, canvas as c
import time
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice("/dev/input/event2")

canvas = c.Canvas()
thickness = 2
triangle = s.PolygonOutline(
    s.get_polygon_vertices(3, 20, (32, 32)), (255, 0, 0), thickness
)
square = s.PolygonOutline(
    s.get_polygon_vertices(4, 20, (96, 32)), (0, 255, 0), thickness
)
pentagon = s.PolygonOutline(
    s.get_polygon_vertices(5, 20, (64, 64)), (0, 0, 255), thickness
)
hexagon = s.PolygonOutline(
    s.get_polygon_vertices(6, 20, (32, 96)), (255, 255, 0), thickness
)
heptagon = s.PolygonOutline(
    s.get_polygon_vertices(7, 20, (96, 96)), (0, 255, 255), thickness
)

polygons = [triangle, square, pentagon, hexagon, heptagon]

def exit_prog():
    print("quit")
    canvas.delete()
    sys.exit()

counter = 0
while counter <= 20:

    if gamepad.active_keys() == [24]:
        exit_prog()

    canvas.clear()
    for polygon in polygons:
        polygon.rotate(1, (polygon.center[0], polygon.center[1]))
        canvas.add(polygon)
    canvas.draw()
    time.sleep(0.25)
    counter += 1
