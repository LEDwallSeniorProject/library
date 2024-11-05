import os
import time
import subprocess
from matrix_library import shapes as s, canvas as c
from evdev import InputDevice, categorize, ecodes

print("Bingo!")

canvas = c.Canvas()
polygon = s.Polygon(s.get_polygon_vertices(5, 20, (64, 64)), (255, 0, 0))

while True:
    canvas.clear()
    polygon.rotate(1, (64, 64))
    canvas.add(polygon)
    canvas.draw()
    time.sleep(0)

# # List of demo programs to run
# demo_programs = [
#     "demo1.py",
#     "demo2.py",
#     "demo3.py",
#     # Add more demo programs here
# ]

# # Current demo index
# current_demo_index = 0

# # Function to run the next demo program
# def run_next_demo():
#     global current_demo_index
    
#     # Close the mainMenu.py program
#     os.system("pkill -f mainMenu.py")
    
#     # Run the next demo program in the background
#     subprocess.Popen(["python", demo_programs[current_demo_index]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     # Increment the demo index, wrapping around if necessary
#     current_demo_index = (current_demo_index + 1) % len(demo_programs)

# # Keyboard event handling to switch between demos
# def on_key_x():
#     run_next_demo()

# # Main loop
# while True:
#     # This loop will keep the program running in the background
#     if gamepad.active_keys() == [23]:
#         on_key_x()
#     time.sleep(1)