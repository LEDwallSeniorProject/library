import matrix_library as matrix
import time


canvas = matrix.Canvas()
controller = matrix.Controller()


# Setup the controller functions
# If you want to use any outside variables, you need to use the global keyword
def up():
    global snake_dir
    snake_dir = [0, -1]


def down():
    global snake_dir
    snake_dir = [0, 1]


def left():
    global snake_dir
    snake_dir = [-1, 0]


def right():
    global snake_dir
    snake_dir = [1, 0]


# Add the functions from above to the controller buttons
controller.add_function("UP", up)
controller.add_function("DOWN", down)
controller.add_function("LEFT", left)
controller.add_function("RIGHT", right)


snake_pos = [16, 16]
snake_body = [[16, 16], [15, 16], [14, 16]]

snake_dir = [1, 0]

game_over = False

food_spawned = True
food_pos = [16, 8]


while not game_over:

    if snake_pos == food_pos:
        food_spawned = False

    start = time.time()

    while time.time() - start < 0.1:
        pass

    canvas.clear()

    for pos in snake_body:
        verts = matrix.get_polygon_vertices(4, 2, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
        body = matrix.Polygon(verts, (0, 255, 0))
        body.rotate(45, ((pos[0] * 4) + 2, (pos[1] * 4) + 2))
        canvas.add(body)

    if not game_over:
        snake_body.insert(0, snake_pos.copy())
        if snake_pos != food_pos:
            snake_body.pop()

    if not food_spawned:
        food_pos = [(int(time.time()) % 28) + 2, (int(time.time()) % 28) + 2]
        food_spawned = True

    food = matrix.Polygon(
        matrix.get_polygon_vertices(
            4, 2, ((food_pos[0] * 4) + 2, (food_pos[1] * 4) + 2)
        ),
        (255, 0, 0),
    )
    food.rotate(45, ((food_pos[0] * 4) + 2, (food_pos[1] * 4) + 2))

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
        canvas.add(matrix.Phrase("GAME OVER", [32, 64], size=1))
        canvas.draw()
        time.sleep(1)
        break
