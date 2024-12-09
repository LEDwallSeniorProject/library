import sys
import matrix_library as matrix
import time
import os

# Initialize controller
controller = matrix.Controller()

# Initialize the canvas
canvas = matrix.Canvas()

# Create shapes and phrases for main menu
square = matrix.Polygon(matrix.get_polygon_vertices(4, 60, (0, 100)), (90, 200, 90))
headerline = matrix.Line((3, 28), (115, 28), (255, 255, 255), thickness=1)
menuheader = matrix.Phrase("MENU", (2, 0), (255, 255, 255), size=3.5, auto_newline=True)
demoheader = matrix.Phrase("Demos", (0, 33), (255, 255, 255), size=3, auto_newline=True)
gamesheader = matrix.Phrase("Games", (0, 60), (255, 255, 255), size=3, auto_newline=True)
creatornames = matrix.Phrase("created by Alex Ellie and Palmer", (0, 100), (255, 255, 255), size=1)

# Countdown setup
countdown_value = 16
countdown_display = matrix.Phrase(str(countdown_value), (110, 119), (255, 255, 255), size=1, auto_newline=True)
countdown_expired = False

# Main menu options and selection
exited = False
options = [demoheader, gamesheader]
selected_index = 0
actions = [lambda: demo_action(), lambda: games_action()]

# Initialize selectors
selector = matrix.Polygon(matrix.get_polygon_vertices(4, 12, (20, 120)), (0, 255, 0))

# Games scene to manage game folders
class GamesScene:
    def __init__(self):
        self.game_folders = self.load_game_folders()
        self.selected_index = 0
        self.page_index = 0
        self.items_per_page = 7

    def load_game_folders(self):
        current_dir = os.path.dirname(__file__)
        games_dir = os.path.join(current_dir, "games")
        return [folder for folder in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, folder))]

    def get_current_page(self):
        start = self.page_index * self.items_per_page
        end = start + self.items_per_page
        return self.game_folders[start:end]

    def next_page(self):
        if (self.page_index + 1) * self.items_per_page < len(self.game_folders):
            self.page_index += 1
            self.selected_index = 0

    def previous_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.selected_index = 0

    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.get_current_page())

    def select_previous(self):
        self.selected_index = (self.selected_index - 1) % len(self.get_current_page())

    def get_selected_game(self):
        current_page = self.get_current_page()
        return current_page[self.selected_index] if current_page else None

# Scene management
main_scene = True
games_scene = GamesScene()

def demo_action():
    global canvas, exited
    print("demos")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

def games_action():
    global main_scene
    main_scene = False

def main_action():
    global main_scene
    main_scene = True

def shutdown():
    global canvas, exited
    print("shutdown")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

# Keyboard event handlers
def on_up():
    global selected_index, countdown_value, countdown_expired, canvas
    if main_scene:
        selected_index = (selected_index - 1) % len(options)
    else:
        games_scene.select_previous()
    countdown_value = 16
    countdown_expired = False

def on_down():
    global selected_index, countdown_value, countdown_expired, canvas
    if main_scene:
        selected_index = (selected_index + 1) % len(options)
    else:
        games_scene.select_next()
    countdown_value = 16
    countdown_expired = False

def on_y():
    global countdown_value, countdown_expired, canvas, exited
    if main_scene:
        actions[selected_index]()
    else:
        selected_game = games_scene.get_selected_game()
        if selected_game:
            print(f"game/{selected_game}")
            canvas.clear()
            canvas.draw()
            time.sleep(0.15)
            exited = True
    countdown_value = 16
    countdown_expired = False

def on_left():
    if not main_scene:
        games_scene.previous_page()

def on_right():
    if not main_scene:
        games_scene.next_page()

def on_a():
    if not main_scene:
        main_action()

# Main loop
fps = 30
frame_time = 1 / fps
last_frame_time = time.time()

controller.add_function("UP",on_up)
controller.add_function("DOWN",on_down)
controller.add_function("LEFT",on_left)
controller.add_function("RIGHT",on_right)
controller.add_function("Y",on_y)
controller.add_function("A",on_a)
controller.add_function("SELECT",shutdown)

controller.add_function("UP2",on_up)
controller.add_function("DOWN2",on_down)
controller.add_function("LEFT2",on_left)
controller.add_function("RIGHT2",on_right)
controller.add_function("Y2",on_y)
controller.add_function("A2",on_a)
controller.add_function("SELECT2",shutdown)

while True:
    
    # Clear the canvas and redraw
    canvas.clear()
    time.sleep(0.15)

    # check if exited
    if exited: sys.exit(0)

    # draw different items based on where I am
    if main_scene:

        selected_option = options[selected_index]
        
        # Calculate desired selector position for the main menu based on selected_index
        selector_x = 132  # Adjust X position as needed for the main menu
        selector_y = 46 + selected_index * 27  # Update Y based on selected_index
        
        # Get current selector position and calculate translation
        current_center = selector.get_center()
        dx = selector_x - current_center[0]
        dy = selector_y - current_center[1]
        
        # Move selector to new position
        selector.translate(dx, dy)

        # Update scrolling creator names
        creatornames.translate(-2, 0)
        if creatornames.get_width() + creatornames.position[0] < 0:
            creatornames.set_position([128, 100])

        # Countdown Timer Logic
        if countdown_value > 0:
            countdown_value -= 2 / fps
        else:
            if not countdown_expired:
                demo_action()
                countdown_expired = True

        # Update countdown display text and position
        countdown_display.set_text(str(int(countdown_value)))
        if countdown_value < 10:
            countdown_display.set_position((114, 119))
        else:
            countdown_display.set_position((110, 119))

        # Draw everything
        canvas.add(square)
        canvas.add(headerline)
        canvas.add(menuheader)
        canvas.add(demoheader)
        canvas.add(gamesheader)
        canvas.add(creatornames)
        canvas.add(countdown_display)
        canvas.add(selector)
    
    else:

        game_names = games_scene.get_current_page()
        for i, game in enumerate(game_names):
            game_phrase = matrix.Phrase(game, (9, 7 + i * 15), (255, 255, 255), size=1)
            canvas.add(game_phrase)
        
        selected_game = games_scene.get_selected_game()
        if selected_game:
            # Calculate desired selector position for games menu
            selector_x = -6
            selector_y = 10 + games_scene.selected_index * 15
            
            # Get current selector position and calculate translation
            current_center = selector.get_center()
            dx = selector_x - current_center[0]
            dy = selector_y - current_center[1]
            
            # Move selector to new position
            selector.translate(dx, dy)
            canvas.add(selector)
        
    canvas.draw()