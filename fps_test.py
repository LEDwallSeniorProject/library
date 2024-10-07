from matrix_library import shapes as s, canvas as c
import time

canvas = c.Canvas()
thickness = 2
triangle = s.PolygonOutline(s.get_polygon_vertices(3, 20, (32,32)), (255, 0, 0), thickness)
square = s.PolygonOutline(s.get_polygon_vertices(4, 20, (96,32)), (0, 255, 0), thickness)
pentagon = s.PolygonOutline(s.get_polygon_vertices(5, 20, (64,64)), (0, 0, 255), thickness)
hexagon = s.PolygonOutline(s.get_polygon_vertices(6, 20, (32,96)), (255, 255, 0), thickness)
heptagon = s.PolygonOutline(s.get_polygon_vertices(7, 20, (96,96)), (0, 255, 255), thickness)

polygons = [triangle, square, pentagon, hexagon, heptagon]

clear_times = []
rotate_times = []
add_times = []
draw_times = []
frame_times = []

frame = 0

while True:
  if frame % 100 == 0 and frame != 0:
    print(f"Frame {frame}")
    print(f"Clear: {sum(clear_times) / len(clear_times)}")
    print(f"Rotate: {sum(rotate_times) / len(rotate_times)}")
    print(f"Add: {sum(add_times) / len(add_times)}")
    print(f"Draw: {sum(draw_times) / len(draw_times)}")
    print(f"Frame: {sum(frame_times) / len(frame_times)}")
    print(f"FPS: {1 / (sum(frame_times) / len(frame_times))}")
  
  frame_start = time.perf_counter()
  canvas.clear()
  clear_end = time.perf_counter()
  clear_times.append(clear_end - frame_start)
  
  for polygon in polygons:
    rotate_start = time.perf_counter()
    polygon.rotate(1, (polygon.center[0], polygon.center[1]))
    
    rotate_times.append(time.perf_counter() - rotate_start)
    
    add_start = time.perf_counter()
    canvas.add(polygon)
    add_times.append(time.perf_counter() - add_start)
  
  draw_start = time.perf_counter()
  canvas.draw()
  draw_times.append(time.perf_counter() - draw_start)
  
  # Total time for the frame
  frame_end = time.perf_counter()
  frame_times.append(frame_end - frame_start)
  
  frame += 1