from matrix_library import canvas as c, shapes as s
import time

from evdev import InputDevice, categorize, ecodes

game_pad = InputDevice("/dev/input/event2")


canvas = c.Canvas()

snake_pos = [16, 16]
snake_body = [[15, 16], [14, 16], [13, 16]]

snake_dir = [1, 0]

game_over = False

food_spawned = False
food_pos = [16, 8]


while not game_over:

    if snake_pos == food_pos:
        food_spawned = False

    start = time.time()
    while time.time() - start < 0.25:
        if game_pad.active_keys() == [46]:
            snake_dir = [0, -1]
        elif game_pad.active_keys() == [33]:
            snake_dir = [1, 0]
        elif game_pad.active_keys() == [32]:
            snake_dir = [0, 1]
        elif game_pad.active_keys() == [18]:
            snake_dir = [-1, 0]

    canvas.clear()

    for pos in snake_body:
        verts = s.get_polygon_vertices(4, 2, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
        body = s.Polygon(verts, (0, 255, 0))
        body.rotate(45, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
        canvas.add(body)

    if not game_over:
        snake_body.insert(0, snake_pos.copy())
        if snake_pos != food_pos:
            snake_body.pop()

    if not food_spawned:
        food_pos = [int(time.time()) % 32, int(time.time()) % 32]
        food_spawned = True

    food = s.Polygon(
        s.get_polygon_vertices(4, 2, ((food_pos[0] * 4) + 2, (food_pos[1] * 4) + 2)),
        (255, 0, 0),
    )

    canvas.add(food)

    canvas.draw()

    snake_pos[0] += snake_dir[0]
    snake_pos[1] += snake_dir[1]

    if snake_pos[0] < 0 or snake_pos[0] >= 33 or snake_pos[1] < 0 or snake_pos[1] >= 33:
        game_over = True

    if snake_pos in snake_body:
        game_over = True

    if game_over:
        canvas.clear()
        canvas.add(s.Phrase("GAME OVER", [32, 64], size=1))
        canvas.draw()
        time.sleep(1)
        break

    # Add your code here
