import os
import subprocess
import sys
from matrix_library import shapes as s, canvas as c
import time
from evdev import InputDevice, categorize, ecodes

# Initialize canvas
gamepad = InputDevice("/dev/input/event2")

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
countdown_value = 31  # Start countdown from 30
countdown_display = s.Phrase(str(countdown_value), (110, 119), (255, 255, 255), size=1, auto_newline=True)
countdown_expired = False  # Flag to check if countdown has expired

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
    try:
        # Get the path to the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        demo_script = os.path.join(current_dir, 'demoManager.py')
        
        # Check if demoManager.py exists
        if not os.path.exists(demo_script):
            print(f"Error: {demo_script} not found")
            return
            
        # Launch demoManager.py using the same Python interpreter
        python_executable = sys.executable
        subprocess.Popen([python_executable, demo_script])
        
        # Sleep briefly to ensure new script starts
        time.sleep(0.5)
        
        canvas.clear()
        canvas.draw()

        # Exit current script
        sys.exit(0)
        
    except Exception as e:
        print(f"Error switching to demo manager: {e}")

def games_action():
    print("Games option selected!")

actions = [demo_action, games_action]

# Keyboard event handling to prevent blocking
def on_key_w():
    global selected_index, countdown_value, countdown_expired
    selected_index = (selected_index - 1) % len(options)
    countdown_value = 31  # Reset countdown
    countdown_expired = False  # Reset countdown expiration

def on_key_s():
    global selected_index, countdown_value, countdown_expired
    selected_index = (selected_index + 1) % len(options)
    countdown_value = 31  # Reset countdown
    countdown_expired = False  # Reset countdown expiration

def on_key_x():
    global countdown_value, countdown_expired
    actions[selected_index]()  # Call the action associated with the selected option
    countdown_value = 31  # Reset countdown
    countdown_expired = False  # Reset countdown expiration

# keyboard.on_press_key("w", lambda _: on_key_w())
# keyboard.on_press_key("s", lambda _: on_key_s())
# keyboard.on_press_key("x", lambda _: on_key_x())

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

        # Change the 
        if gamepad.active_keys() == [46]:
            on_key_w()
        if gamepad.active_keys() == [32]:
            on_key_s()
        if gamepad.active_keys() == [23]:
            on_key_x()

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

        # Countdown Timer Logic
        if countdown_value > 0:
            countdown_value -= 1 / fps  # Decrease countdown_value based on frame rate
        else:
            if not countdown_expired:
                demo_action()  # Call demo action only once
                countdown_expired = True  # Set flag to prevent repeated calls

        # Update countdown display text and position
        countdown_display.set_text(str(int(countdown_value)))  # Update the display text
        if countdown_value < 10:
            countdown_display.set_position((114, 119))  # Move to the right if single-digit
        else:
            countdown_display.set_position((110, 119))  # Keep original position for double-digit

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