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
    time.sleep(0.25)
    canvas.clear()

    for pos in snake_body:
        verts = s.get_polygon_vertices(4, 2, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
        body = s.Polygon(verts, (0, 255, 0))
        body.rotate(45, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
        canvas.add(body)

    if not food_spawned:
        food_pos = [int(time.time()) % 32, int(time.time()) % 32]
        food_spawned = True

    food = s.Polygon(
        s.get_polygon_vertices(4, 2, ((food_pos[0] * 4) + 2, (food_pos[1] * 4) + 2)),
        (255, 0, 0),
    )

    canvas.draw()

    snake_pos[0] += snake_dir[0]
    snake_pos[1] += snake_dir[1]

    if snake_pos[0] < 0 or snake_pos[0] >= 32 or snake_pos[1] < 0 or snake_pos[1] >= 32:
        game_over = True

    if snake_pos in snake_body:
        game_over = True

    if not game_over:
        snake_body.insert(0, snake_pos.copy())
        if len(snake_body) > 3:
            snake_body.pop()

    if game_over:
        canvas.clear()
        canvas.add(s.Phrase("GAME OVER", [32, 64], size=1))
        canvas.draw()
        time.sleep(2)
        break

    # Add your code here
    if game_pad.active_keys() == [46]:
        snake_dir = [0, -1]
    elif game_pad.active_keys() == [33]:
        snake_dir = [1, 0]
    elif game_pad.active_keys() == [32]:
        snake_dir = [0, 1]
    elif game_pad.active_keys() == [18]:
        snake_dir = [-1, 0]