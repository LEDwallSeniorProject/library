from matrix_library import shapes as s, canvas as c
import time
# import asyncio
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice('/dev/input/event2')
canvas = c.Canvas()
polygon = s.Polygon(s.get_polygon_vertices(5, 20, (64, 64)), (100, 0, 0))
polygon2 = s.Polygon(s.get_polygon_vertices(3, 70, (64, 64)), (0, 100, 0))

# async def main(dev):
#     async for ev in dev.async_read_loop():
#         print(repr(ev))

while True:
    canvas.clear()
    # print(gamepad.active_keys())
    if gamepad.active_keys() == [34]:
        canvas.add(polygon2)
    
    polygon.rotate(1, (64, 64))
    canvas.add(polygon)
    canvas.draw()
    time.sleep(0)
