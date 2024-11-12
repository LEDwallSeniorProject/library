from matrix_library import shapes as s, canvas as c
import time

canvas = c.Canvas(renderMode="zmq")
thickness = 2
pentagon = s.Polygon(s.get_polygon_vertices(5, 45, (64, 64)), (0, 0, 255))

fps_text = s.Phrase("FPS: ...", [0, 0])

polygons = [pentagon]

clear_times = []
rotate_times = []
add_times = []
add_all_times = []
draw_times = []
frame_times = []

frame = 0

while True:
    if frame % 100 == 0 and frame != 0:
        print(f"Frame {frame}")
        print(f"Clear: {sum(clear_times) / len(clear_times)}")
        print(f"Rotate: {sum(rotate_times) / len(rotate_times)}")
        print(f"Add: {sum(add_times) / len(add_times)}")
        print(f"Add All: {sum(add_all_times) / len(add_all_times)}")
        print(f"Draw: {sum(draw_times) / len(draw_times)}")
        print(f"Frame: {sum(frame_times) / len(frame_times)}")
        print(f"Avg FPS: {1 / (sum(frame_times) / len(frame_times))}")

    frame_start = time.perf_counter()
    canvas.clear()
    clear_end = time.perf_counter()
    clear_times.append(clear_end - frame_start)

    add_all_start = time.perf_counter()
    for polygon in polygons:
        rotate_start = time.perf_counter()
        polygon.rotate(1, (polygon.center[0], polygon.center[1]))

        rotate_times.append(time.perf_counter() - rotate_start)

        add_start = time.perf_counter()
        canvas.add(polygon)
        add_times.append(time.perf_counter() - add_start)
    if frame != 0:
        fps_text.set_text(f"FPS: {1 / (sum(frame_times) / len(frame_times)):.2f}")
    canvas.add(fps_text)

    add_all_times.append(time.perf_counter() - add_all_start)

    draw_start = time.perf_counter()
    canvas.draw()
    draw_times.append(time.perf_counter() - draw_start)

    # Total time for the frame
    frame_end = time.perf_counter()
    frame_times.append(frame_end - frame_start)

    frame += 1
