import matrix_library as matrix
import time
import random
import numpy as np

class TetrisGame:
    def __init__(self):
        # Initialize canvas and controller
        self.canvas = matrix.Canvas()
        self.controller = matrix.Controller()
        
        # Game settings
        self.grid_width = 10
        self.grid_height = 20
        self.block_size = 5  # Block size in pixels (adjusted for visibility)
        self.grid_offset_x = 24  # Center the grid on the 128×128 canvas
        self.grid_offset_y = 4
        
        # Game state
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.current_piece = None
        self.current_pos = [0, 0]
        self.game_over = False
        self.paused = False
        self.running = True
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.drop_speed = 0.5  # Initial drop speed in seconds
        self.last_drop_time = time.time()
        
        # Tetrimino shapes and colors (I, J, L, O, S, T, Z)
        self.tetriminos = [
            {'shape': [[1, 1, 1, 1]], 'color': (0, 255, 255)},  # I - Cyan
            {'shape': [[1, 0, 0], [1, 1, 1]], 'color': (0, 0, 255)},  # J - Blue
            {'shape': [[0, 0, 1], [1, 1, 1]], 'color': (255, 165, 0)},  # L - Orange
            {'shape': [[1, 1], [1, 1]], 'color': (255, 255, 0)},  # O - Yellow
            {'shape': [[0, 1, 1], [1, 1, 0]], 'color': (0, 255, 0)},  # S - Green
            {'shape': [[0, 1, 0], [1, 1, 1]], 'color': (128, 0, 128)},  # T - Purple
            {'shape': [[1, 1, 0], [0, 1, 1]], 'color': (255, 0, 0)}  # Z - Red
        ]
        
        # Print controls info for reference
        print("Tetris Controls:")
        print("--------------")
        print("LEFT/RIGHT: Move piece")
        print("UP: Rotate piece")
        print("DOWN: Soft drop")
        print("A: Hard drop")
        print("START: Pause/Continue")
        print("SELECT: Restart/Exit")
        
    def setup_controls(self):
        """Setup the controller functions - mapped according to controller.py"""
        # Clear any existing mappings
        self.controller.clear()
        
        # Standard controls (work for keyboard and controller)
        # LEFT, RIGHT, UP, DOWN = WASD keys on keyboard
        self.controller.add_function("LEFT", self.move_left)
        self.controller.add_function("RIGHT", self.move_right)
        self.controller.add_function("UP", self.rotate)
        self.controller.add_function("DOWN", self.move_down)
        
        # Action buttons
        self.controller.add_function("A", self.hard_drop)      # 'g' key
        self.controller.add_function("B", self.rotate)         # 'v' key (alternative rotate)
        self.controller.add_function("START", self.toggle_pause)  # 'c' key
        self.controller.add_function("SELECT", self.toggle_exit)  # 'z' key
        
        # Additional keyboard controls (Player 2 controls from controller.py)
        # Added for more flexibility - these map to IJKL keys
        self.controller.add_function("LEFT2", self.move_left)
        self.controller.add_function("RIGHT2", self.move_right)
        self.controller.add_function("UP2", self.rotate)
        self.controller.add_function("DOWN2", self.move_down)
        self.controller.add_function("A2", self.hard_drop)       # '\'' key
        self.controller.add_function("B2", self.rotate)          # '/' key
        self.controller.add_function("START2", self.toggle_pause)  # '.' key
        self.controller.add_function("SELECT2", self.toggle_exit)  # 'm' key
    
    def setup_start_controls(self):
        """Special controls for the start screen"""
        self.controller.clear()
        
        # Create a mutable list to track button press
        start_pressed = [False]
        
        # Function to handle button press
        def start_game():
            start_pressed[0] = True
        
        # Bind multiple buttons to start the game
        for button in ["UP", "DOWN", "LEFT", "RIGHT", "A", "B", "X", "Y", "START", "SELECT",
                     "UP2", "DOWN2", "LEFT2", "RIGHT2", "A2", "B2", "X2", "Y2", "START2", "SELECT2"]:
            self.controller.add_function(button, start_game)
        
        return start_pressed
    
    def move_left(self):
        """Move the current piece left if possible"""
        if self.game_over or self.paused:
            return
            
        new_pos = [self.current_pos[0] - 1, self.current_pos[1]]
        if self.is_valid_position(new_pos[0], new_pos[1]):
            self.current_pos = new_pos
    
    def move_right(self):
        """Move the current piece right if possible"""
        if self.game_over or self.paused:
            return
            
        new_pos = [self.current_pos[0] + 1, self.current_pos[1]]
        if self.is_valid_position(new_pos[0], new_pos[1]):
            self.current_pos = new_pos
    
    def move_down(self):
        """Move the current piece down if possible"""
        if self.game_over or self.paused:
            return False
            
        new_pos = [self.current_pos[0], self.current_pos[1] + 1]
        if self.is_valid_position(new_pos[0], new_pos[1]):
            self.current_pos = new_pos
            return True
        else:
            # Lock the piece in place and spawn a new one
            self.lock_piece()
            return False
    
    def hard_drop(self):
        """Drop the current piece all the way down"""
        if self.game_over or self.paused:
            return
            
        # Keep moving down until collision
        while self.move_down():
            pass
    
    def rotate(self):
        """Rotate the current piece if possible"""
        if self.game_over or self.paused:
            return
            
        # O piece doesn't rotate
        if self.current_piece == self.tetriminos[3]:
            return
            
        # Create a rotated piece
        piece = self.current_piece.copy()
        shape = piece['shape']
        rotated_shape = list(zip(*reversed(shape)))  # Transpose and reverse rows
        piece['shape'] = [list(row) for row in rotated_shape]
        
        # Check if the rotated piece can fit
        if self.is_valid_position(self.current_pos[0], self.current_pos[1], piece):
            self.current_piece = piece
        else:
            # Try wall kick: move the piece right, left, or up if it can't rotate in place
            offsets = [(1, 0), (-1, 0), (0, -1), (2, 0), (-2, 0)]
            for offset_x, offset_y in offsets:
                new_x = self.current_pos[0] + offset_x
                new_y = self.current_pos[1] + offset_y
                if self.is_valid_position(new_x, new_y, piece):
                    self.current_pos = [new_x, new_y]
                    self.current_piece = piece
                    break
    
    def toggle_pause(self):
        """Pause or unpause the game"""
        if self.game_over:
            return
            
        self.paused = not self.paused
        print("Game " + ("Paused" if self.paused else "Resumed"))
    
    def toggle_exit(self):
        """Exit the game or restart if game over"""
        if self.game_over:
            # Reset the game
            self.reset_game()
        else:
            # Show exit confirmation and exit
            self.running = False
            print("Game Exited")
    
    def reset_game(self):
        """Reset the game to initial state"""
        print("Game Reset")
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.current_piece = None
        self.game_over = False
        self.paused = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.drop_speed = 0.5
        self.last_drop_time = time.time()
        self.spawn_piece()
    
    def spawn_piece(self):
        """Spawn a new tetrimino at the top of the grid"""
        self.current_piece = random.choice(self.tetriminos)
        piece_width = len(self.current_piece['shape'][0])
        self.current_pos = [self.grid_width // 2 - piece_width // 2, 0]
        
        # Check if the game is over (no space to spawn a new piece)
        if not self.is_valid_position():
            self.game_over = True
            return False
        return True
    
    def is_valid_position(self, pos_x=None, pos_y=None, piece=None):
        """Check if the current piece at the specified position is valid"""
        if pos_x is None and pos_y is None:
            pos_x, pos_y = self.current_pos
        if piece is None:
            piece = self.current_piece
            
        shape = piece['shape']
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == 0:
                    continue  # Skip empty cells
                
                grid_x = pos_x + x
                grid_y = pos_y + y
                
                # Check if out of bounds
                if (grid_x < 0 or grid_x >= self.grid_width or 
                    grid_y < 0 or grid_y >= self.grid_height):
                    return False
                
                # Check if collides with existing blocks
                if grid_y >= 0 and self.grid[grid_y][grid_x] != 0:
                    return False
        return True
    
    def lock_piece(self):
        """Lock the current piece in place on the grid"""
        shape = self.current_piece['shape']
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == 0:
                    continue
                
                grid_y = self.current_pos[1] + y
                grid_x = self.current_pos[0] + x
                
                if 0 <= grid_y < self.grid_height and 0 <= grid_x < self.grid_width:
                    self.grid[grid_y][grid_x] = self.current_piece['color']
        
        # Check for completed lines
        self.clear_lines()
        
        # Spawn a new piece
        return self.spawn_piece()
    
    def clear_lines(self):
        """Clear completed lines and update score"""
        lines_to_clear = []
        
        # Find completed lines
        for y in range(self.grid_height):
            if all(cell != 0 for cell in self.grid[y]):
                lines_to_clear.append(y)
                
        # Update score and level
        if lines_to_clear:
            # Classic Tetris scoring system
            self.lines_cleared += len(lines_to_clear)
            points = [100, 300, 500, 800][min(len(lines_to_clear) - 1, 3)] * self.level
            self.score += points
            self.level = min(10, (self.lines_cleared // 10) + 1)
            # Speed increases with level
            self.drop_speed = max(0.1, 0.5 - (self.level - 1) * 0.05)
            
            # Remove the cleared lines and add new empty lines at the top
            for line in sorted(lines_to_clear, reverse=True):
                del self.grid[line]
                self.grid.insert(0, [0 for _ in range(self.grid_width)])
    
    def draw_block(self, grid_x, grid_y, color):
        """Draw a single block on the grid with a border"""
        # Calculate pixel coordinates
        x = self.grid_offset_x + grid_x * self.block_size
        y = self.grid_offset_y + grid_y * self.block_size
        
        # Draw filled block with a border
        block = matrix.Polygon(
            [
                (x, y),
                (x + self.block_size, y),
                (x + self.block_size, y + self.block_size),
                (x, y + self.block_size)
            ],
            color
        )
        
        # Add the block to the canvas
        self.canvas.add(block)
        
        # Add a border around the block
        border = matrix.PolygonOutline(
            [
                (x, y),
                (x + self.block_size, y),
                (x + self.block_size, y + self.block_size),
                (x, y + self.block_size)
            ],
            (min(color[0] + 40, 255), min(color[1] + 40, 255), min(color[2] + 40, 255)),
            1
        )
        self.canvas.add(border)
    
    def draw_grid_border(self):
        """Draw the border around the game grid"""
        grid_width_pixels = self.grid_width * self.block_size
        grid_height_pixels = self.grid_height * self.block_size
        
        # Create grid border
        border = matrix.PolygonOutline(
            [
                (self.grid_offset_x - 1, self.grid_offset_y - 1),
                (self.grid_offset_x + grid_width_pixels + 1, self.grid_offset_y - 1),
                (self.grid_offset_x + grid_width_pixels + 1, self.grid_offset_y + grid_height_pixels + 1),
                (self.grid_offset_x - 1, self.grid_offset_y + grid_height_pixels + 1)
            ],
            (200, 200, 200),
            1
        )
        self.canvas.add(border)
    
    def draw_frame(self):
        """Draw a complete frame of the game"""
        # Clear the canvas
        self.canvas.clear()
        
        # Draw grid border first
        self.draw_grid_border()
        
        # Draw existing blocks in the grid
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x] != 0:
                    self.draw_block(x, y, self.grid[y][x])
        
        # Draw the current falling piece
        if self.current_piece and not self.game_over and not self.paused:
            shape = self.current_piece['shape']
            color = self.current_piece['color']
            
            for y in range(len(shape)):
                for x in range(len(shape[y])):
                    if shape[y][x] == 1:
                        grid_x = self.current_pos[0] + x
                        grid_y = self.current_pos[1] + y
                        if 0 <= grid_y < self.grid_height and 0 <= grid_x < self.grid_width:
                            self.draw_block(grid_x, grid_y, color)
        
        # Draw UI elements
        self.draw_ui()
        
        # Draw extra messages
        if self.paused:
            self.draw_message("PAUSED", 50)
        elif self.game_over:
            self.draw_message("GAME OVER", 50)
            self.draw_message("PRESS SELECT TO RESTART", 70)
        
        # Update the display
        self.canvas.draw()
    
    def draw_ui(self):
        """Draw score, level, and other UI elements"""
        # Display score
        score_label = matrix.Phrase("SCORE", [4, 20])
        score_value = matrix.Phrase(f"{self.score}", [4, 30])
        
        # Display level
        level_label = matrix.Phrase("LEVEL", [90, 20])
        level_value = matrix.Phrase(f"{self.level}", [100, 30])
        
        # Display lines cleared
        lines_label = matrix.Phrase("LINES", [4, 110])
        lines_value = matrix.Phrase(f"{self.lines_cleared}", [4, 120])
        
        # Add UI elements to canvas
        self.canvas.add(score_label)
        self.canvas.add(score_value)
        self.canvas.add(level_label)
        self.canvas.add(level_value)
        self.canvas.add(lines_label)
        self.canvas.add(lines_value)
    
    def draw_message(self, message, y_pos):
        """Draw a centered message on the screen"""
        message_width = len(message) * 8  # Approximate width of the message
        x_pos = (128 - message_width) // 2
        msg_text = matrix.Phrase(message, [x_pos, y_pos])
        self.canvas.add(msg_text)
    
    def show_title_screen(self):
        """Display the title screen with animated effect"""
        # Setup controls for the title screen
        start_pressed = self.setup_start_controls()
        
        # Create title elements
        title = matrix.Phrase("TETRIS", [40, 30], size=1)
        
        # Animation time
        start_time = time.time()
        animation_done = False
        
        # Title screen loop
        while not start_pressed[0] and self.running:
            self.canvas.clear()
            
            # Simple animation for title
            bounce = int(10 * np.sin((time.time() - start_time) * 2))
            
            # Draw title
            title.set_position([40, 30 + bounce])
            self.canvas.add(title)
            
            # Draw controls information
            if int(time.time()) % 2 == 0:  # blink effect
                controls1 = matrix.Phrase("CONTROLS:", [35, 55])
                controls2 = matrix.Phrase("LEFT/RIGHT: MOVE", [15, 65])
                controls3 = matrix.Phrase("UP: ROTATE", [15, 75])
                controls4 = matrix.Phrase("A: HARD DROP", [15, 85])
                controls5 = matrix.Phrase("START: PAUSE", [15, 95])
                
                self.canvas.add(controls1)
                self.canvas.add(controls2)
                self.canvas.add(controls3)
                self.canvas.add(controls4)
                self.canvas.add(controls5)
            
            # Prompt to start
            if int(time.time() * 2) % 2 == 0:  # faster blink
                start_text = matrix.Phrase("PRESS ANY BUTTON", [20, 115])
                self.canvas.add(start_text)
            
            # Draw the frame
            self.canvas.draw()
            
            # Automatic start if no input after 20 seconds
            if time.time() - start_time > 20 and self.running:
                break
                
            # Small delay to prevent CPU overload
            time.sleep(0.03)
        
        # Clear the screen
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.3)  # Short delay for better transition
        
        # Setup game controls
        self.setup_controls()
    
    def run(self):
        """Main game loop"""
        try:
            # Show title screen
            self.show_title_screen()
            
            # Initialize the game
            self.reset_game()
            
            # Main game loop
            while self.running:
                current_time = time.time()
                
                # Auto drop piece after a certain time if game is active
                if not self.game_over and not self.paused:
                    if current_time - self.last_drop_time > self.drop_speed:
                        self.move_down()
                        self.last_drop_time = current_time
                
                # Draw the current frame
                self.draw_frame()
                
                # Small delay to prevent CPU overload
                time.sleep(0.01)
            
            # Final cleanup
            self.canvas.clear()
            self.canvas.draw()
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Clean up controller
            self.controller.stop()

# Run the game
if __name__ == "__main__":
    tetris = TetrisGame()
    tetris.run()