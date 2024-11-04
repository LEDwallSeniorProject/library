from matrix_library import shapes as s, canvas as c
import time
import keyboard

# Initialize the canvas
canvas = c.Canvas()

# Create shapes and phrases
square = s.Polygon(s.get_polygon_vertices(4, 60, (0, 100)), (100, 200, 100))
headerline = s.Line((3, 28), (115, 28), (255, 255, 255), thickness=1)
menuheader = s.Phrase("MENU", (2, 0), (255, 255, 255), size=3.5, auto_newline=True)
demoheader = s.Phrase("Demos", (0, 33), (255, 255, 255), size=3, auto_newline=True)
gamesheader = s.Phrase("Games", (0, 60), (255, 255, 255), size=3, auto_newline=True)
creatornames = s.Phrase(
    "created by Alex Ellie and Palmer", (0, 100), (255, 255, 255), size=1
)
controller = s.Polygon(s.get_polygon_vertices(4, 30, (5, 150)), (0, 0, 255))
controller2 = s.Polygon(s.get_polygon_vertices(4, 30, (20, 150)), (0, 0, 255))

# Countdown setup
countdown_value = 30  # Start countdown from 30
countdown_display = s.Phrase(str(countdown_value), (110, 120), (255, 255, 255), size=1, auto_newline=True)

# Menu options setup
options = [demoheader, gamesheader]
selected_index = 0

# Initialize the green outline box for selection
thickness = 1  # Define the thickness for the outline
outline_box = s.PolygonOutline(
    s.get_polygon_vertices(4, 20, (0, 0)), (0, 255, 0), thickness
)

# Placeholder functions for actions
def demo_action():
    print("Demo option selected!")
    # Reset the countdown when the demo action is called
    global countdown_value
    countdown_value = 30

def games_action():
    print("Games option selected!")
    # Reset the countdown when the games action is called
    global countdown_value
    countdown_value = 30

actions = [demo_action, games_action]

# Keyboard event handling to prevent blocking
def on_key_w():
    global selected_index, countdown_value
    selected_index = (selected_index - 1) % len(options)
    countdown_value = 30  # Reset countdown

def on_key_s():
    global selected_index, countdown_value
    selected_index = (selected_index + 1) % len(options)
    countdown_value = 30  # Reset countdown

def on_key_x():
    global countdown_value
    actions[selected_index]()  # Call the action associated with the selected option
    countdown_value = 30  # Reset countdown

keyboard.on_press_key("w", lambda _: on_key_w())
keyboard.on_press_key("s", lambda _: on_key_s())
keyboard.on_press_key("x", lambda _: on_key_x())

# Set desired framerate
fps = 15
frame_time = 1 / fps
last_frame_time = time.time()

# Main loop
while True:
    current_time = time.time()
    elapsed_time = current_time - last_frame_time
    
    # Update only if enough time has passed since the last frame
    if elapsed_time >= frame_time:
        last_frame_time = current_time  # Reset the frame timer

        # Update the outline box vertices based on the selected option
        selected_option = options[selected_index]
        box_x = selected_option.position[0] - 2  # Add a small margin
        box_y = selected_option.position[1] - 2
        box_width = selected_option.get_width() + 4
        box_height = selected_option.size * 8 + 4

        # Set vertices for the outline box
        outline_box.vertices = s.get_polygon_vertices(4, 20, (box_x + 142, box_y + 15))

        # Update scrolling creator names
        creatornames.translate(-2, 0)
        if creatornames.get_width() + creatornames.position[0] < 0:
            creatornames.set_position([128, 100])

        # Update the countdown timer
        if countdown_value > 0:
            countdown_value -= 1 / fps  # Decrease countdown_value based on frame rate
        else:
            demo_action()  # Call demo action when countdown reaches zero

        # Update countdown display
        countdown_display.text = str(int(countdown_value))  # Update the countdown display text

        # Draw everything
        canvas.clear()
        canvas.add(square)
        canvas.add(headerline)
        canvas.add(menuheader)
        canvas.add(demoheader)
        canvas.add(gamesheader)
        canvas.add(creatornames)
        canvas.add(controller)
        canvas.add(controller2)
        canvas.add(countdown_display)  # Draw the countdown display
        canvas.add(outline_box)  # Add the green outline box
        canvas.draw()
