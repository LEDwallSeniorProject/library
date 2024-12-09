import matrix_library as matrix
import time

canvas = matrix.Canvas()

# Spin polygons outlines
spin_create_times = []
spin_clear_times = []
spin_rotate_times = []
spin_add_times = []
spin_draw_times = []
spin_frame_times = []

spin_create_time_start = time.perf_counter()
thickness = 2
triangle = matrix.PolygonOutline(
    matrix.get_polygon_vertices(3, 20, (32, 32)), (255, 0, 0), thickness
)
square = matrix.PolygonOutline(
    matrix.get_polygon_vertices(4, 20, (96, 32)), (0, 255, 0), thickness
)
pentagon = matrix.PolygonOutline(
    matrix.get_polygon_vertices(5, 20, (64, 64)), (0, 0, 255), thickness
)
hexagon = matrix.PolygonOutline(
    matrix.get_polygon_vertices(6, 20, (32, 96)), (255, 255, 0), thickness
)
heptagon = matrix.PolygonOutline(
    matrix.get_polygon_vertices(7, 20, (96, 96)), (0, 255, 255), thickness
)
polygons = [triangle, square, pentagon, hexagon, heptagon]
spin_create_times.append(time.perf_counter() - spin_create_time_start)

for i in range(1000):
    frame_start = time.perf_counter()
    canvas.clear()
    spin_clear_times.append(time.perf_counter() - frame_start)
    for polygon in polygons:
        spin_rotate_time_start = time.perf_counter()
        polygon.rotate(1, (polygon.center[0], polygon.center[1]))
        spin_rotate_times.append(time.perf_counter() - spin_rotate_time_start)
        spin_add_time_start = time.perf_counter()
        canvas.add(polygon)
        spin_add_times.append(time.perf_counter() - spin_add_time_start)
    spin_draw_time_start = time.perf_counter()
    canvas.draw()
    spin_draw_times.append(time.perf_counter() - spin_draw_time_start)
    spin_frame_times.append(time.perf_counter() - frame_start)

# Spin polygons
spin2_create_times = []
spin2_clear_times = []
spin2_rotate_times = []
spin2_add_times = []
spin2_draw_times = []
spin2_frame_times = []

spin2_create_time_start = time.perf_counter()
thickness = 2
triangle = matrix.Polygon(matrix.get_polygon_vertices(3, 20, (32, 32)), (255, 0, 0))
square = matrix.Polygon(matrix.get_polygon_vertices(4, 20, (96, 32)), (0, 255, 0))
pentagon = matrix.Polygon(matrix.get_polygon_vertices(5, 20, (64, 64)), (0, 0, 255))
hexagon = matrix.Polygon(matrix.get_polygon_vertices(6, 20, (32, 96)), (255, 255, 0))
heptagon = matrix.Polygon(matrix.get_polygon_vertices(7, 20, (96, 96)), (0, 255, 255))
polygons = [triangle, square, pentagon, hexagon, heptagon]
spin2_create_times.append(time.perf_counter() - spin2_create_time_start)

for i in range(1000):
    frame_start = time.perf_counter()
    canvas.clear()
    spin2_clear_times.append(time.perf_counter() - frame_start)
    for polygon in polygons:
        spin2_rotate_time_start = time.perf_counter()
        polygon.rotate(1, (polygon.center[0], polygon.center[1]))
        spin2_rotate_times.append(time.perf_counter() - spin2_rotate_time_start)
        spin2_add_time_start = time.perf_counter()
        canvas.add(polygon)
        spin2_add_times.append(time.perf_counter() - spin2_add_time_start)
    spin2_draw_time_start = time.perf_counter()
    canvas.draw()
    spin2_draw_times.append(time.perf_counter() - spin2_draw_time_start)
    spin2_frame_times.append(time.perf_counter() - frame_start)


# Bounce circle
bounce_create_times = []
bounce_clear_times = []
bounce_translate_times = []
bounce_add_times = []
bounce_draw_times = []
bounce_frame_times = []

bounce_create_time_start = time.perf_counter()
circle = matrix.Circle(10, (64, 96), (0, 255, 0))
velocity_y = 2
velocity_x = 3
bounce_create_times.append(time.perf_counter() - bounce_create_time_start)

for i in range(1000):
    frame_start = time.perf_counter()
    circle.translate(velocity_x, velocity_y)
    if circle.center[1] + circle.radius >= 128 or circle.center[1] - circle.radius <= 0:
        velocity_y *= -1
    if circle.center[0] + circle.radius >= 128 or circle.center[0] - circle.radius <= 0:
        velocity_x *= -1
    canvas.clear()
    bounce_clear_times.append(time.perf_counter() - frame_start)
    bounce_translate_time_start = time.perf_counter()
    canvas.add(circle)
    bounce_add_times.append(time.perf_counter() - bounce_translate_time_start)
    bounce_draw_time_start = time.perf_counter()
    canvas.draw()
    bounce_draw_times.append(time.perf_counter() - bounce_draw_time_start)
    bounce_frame_times.append(time.perf_counter() - frame_start)

# Scrolling text
scroll_create_times = []
scroll_clear_times = []
scroll_translate_times = []
scroll_add_times = []
scroll_draw_times = []
scroll_frame_times = []

scroll_create_time_start = time.perf_counter()
text = matrix.Phrase(
    "In the beginning, God created the heavens and the earth. The earth was without form and void, and darkness was over the face of the deep. And the Spirit of God was hovering over the face of the waters. And God said, 'Let there be light,' and there was light. And God saw that the light was good. And God separated the light from the darkness. God called the light Day, and the darkness he called Night. And there was evening and there was morning, the first day. And God said, 'Let there be an expanse in the midst of the waters, and let it separate the waters from the waters.' And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so. And God called the expanse Heaven. And there was evening and there was morning, the second day.",
    [0, 0],
    auto_newline=True,
)
scroll_create_times.append(time.perf_counter() - scroll_create_time_start)

for i in range(500):
    frame_start = time.perf_counter()
    canvas.clear()
    scroll_clear_times.append(time.perf_counter() - frame_start)
    scroll_translate_time_start = time.perf_counter()
    text.translate(0, -1)
    scroll_translate_times.append(time.perf_counter() - scroll_translate_time_start)
    canvas.add(text)
    scroll_add_times.append(time.perf_counter() - scroll_translate_time_start)
    scroll_draw_time_start = time.perf_counter()
    canvas.draw()
    scroll_draw_times.append(time.perf_counter() - scroll_draw_time_start)
    scroll_frame_times.append(time.perf_counter() - frame_start)


# Calculate frame time averages
spin_avg_frame_time = sum(spin_frame_times) / len(spin_frame_times)
spin2_avg_frame_time = sum(spin2_frame_times) / len(spin2_frame_times)
bounce_avg_frame_time = sum(bounce_frame_times) / len(bounce_frame_times)
scroll_avg_frame_time = sum(scroll_frame_times) / len(scroll_frame_times)

# Calculate FPS averages
spin_avg_fps = 1 / spin_avg_frame_time
spin2_avg_fps = 1 / spin2_avg_frame_time
bounce_avg_fps = 1 / bounce_avg_frame_time
scroll_avg_fps = 1 / scroll_avg_frame_time
total_avg_fps = (spin_avg_fps + spin2_avg_fps + bounce_avg_fps + scroll_avg_fps) / 4

print(f"Spin FPS: {spin_avg_fps:.2f}")
print(f"Spin2 FPS: {spin2_avg_fps:.2f}")
print(f"Bounce FPS: {bounce_avg_fps:.2f}")
print(f"Scroll FPS: {scroll_avg_fps:.2f}")

# Get Times for scrolling text
scroll_avg_create_time = sum(scroll_create_times) / len(scroll_create_times)
scroll_avg_clear_time = sum(scroll_clear_times) / len(scroll_clear_times)
scroll_avg_translate_time = sum(scroll_translate_times) / len(scroll_translate_times)
scroll_avg_add_time = sum(scroll_add_times) / len(scroll_add_times)
scroll_avg_draw_time = sum(scroll_draw_times) / len(scroll_draw_times)
scroll_avg_frame_time = sum(scroll_frame_times) / len(scroll_frame_times)

# Print stats for scrolling text
print(f"Scroll Create: {scroll_avg_create_time:.5f}")
print(f"Scroll Clear: {scroll_avg_clear_time:.5f}")
print(f"Scroll Translate: {scroll_avg_translate_time:.5f}")
print(f"Scroll Add: {scroll_avg_add_time:.5f}")
print(f"Scroll Draw: {scroll_avg_draw_time:.5f}")
print(f"Scroll Frame: {scroll_avg_frame_time:.5f}")


spin_fps_title = matrix.Phrase(f"Spin FPS: ", [0, 0])
spin_fps_num = matrix.Phrase(f"{spin_avg_fps:.2f}", [0, 8])
spin2_fps_title = matrix.Phrase(f"Spin2 FPS: ", [0, 16])
spin2_fps_num = matrix.Phrase(f"{spin2_avg_fps:.2f}", [0, 24])
bounce_fps_title = matrix.Phrase(f"Bounce FPS: ", [0, 32])
bounce_fps_num = matrix.Phrase(f"{bounce_avg_fps:.2f}", [0, 40])
scroll_fps_title = matrix.Phrase(f"Scroll FPS: ", [0, 48])
scroll_fps_num = matrix.Phrase(f"{scroll_avg_fps:.2f}", [0, 56])

fps_texts = [
    spin_fps_title,
    spin_fps_num,
    spin2_fps_title,
    spin2_fps_num,
    bounce_fps_title,
    bounce_fps_num,
    scroll_fps_title,
    scroll_fps_num,
]

# while True:
#     canvas.clear()
#     for fps_text in fps_texts:
#         canvas.add(fps_text)
#     canvas.draw()
