from matrix_library import shapes as s, canvas as c
import time
from evdev import InputDevice, categorize, ecodes
import random  # For randomizing ball direction and speed variation after reset

# Initialize canvas
gamepad = InputDevice("/dev/input/event2")

canvas = c.Canvas()
# gamepad = InputDevice("/dev/input/event2")

# Constants
WIDTH, HEIGHT = 128, 126
BALL_RADIUS = 10
PADDLE_WIDTH = 8
PADDLE_HEIGHT = 40
PADDLE_SPEED = 6
BALL_SPEED = 6
SLEEP_TIME = 1 / 30  # Frame rate
AI_REACTION_SPEED = 2  # Lower number = faster reaction
VELOCITY_VARIATION_AMOUNT = 2
MIN_SPEED = 2
MAX_SPEED = 6

# Game scores
player1_score = 0
player2_score = 0

# Helper function to get rectangle vertices
def get_rectangle_vertices(center, width, height):
    x, y = center
    return [
        (x - width // 2, y - height // 2),  # Top-left
        (x + width // 2, y - height // 2),  # Top-right
        (x + width // 2, y + height // 2),  # Bottom-right
        (x - width // 2, y + height // 2),  # Bottom-left
    ]

def reset_ball():
    # Reset ball position to center
    ball.center = (WIDTH // 2, HEIGHT // 2)
    
    # Randomize initial direction while maintaining speed
    angle = random.uniform(-0.5, 0.5)  # Random angle variation
    direction = random.choice([-1, 1])  # Random horizontal direction
    ball.velocity_x = direction * BALL_SPEED
    ball.velocity_y = BALL_SPEED * angle

def exit_prog():
    canvas.delete()
    sys.exit()

# Ball class
class Ball(s.Circle):
    def __init__(self, radius, center, color, velocity_x, velocity_y):
        super().__init__(radius, center, color)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update_position(self):
        global player1_score, player2_score
        
        # Check for scoring (ball leaving canvas horizontally)
        if self.center[0] + BALL_RADIUS < 0:  # Ball passed left boundary
            player2_score += 1
            print(f"Score - Player 1: {player1_score} | Player 2: {player2_score}")
            reset_ball()
            return
        elif self.center[0] - BALL_RADIUS > WIDTH:  # Ball passed right boundary
            player1_score += 1
            print(f"Score - Player 1: {player1_score} | Player 2: {player2_score}")
            reset_ball()
            return

        # Normal ball movement and vertical boundary checking
        if self.center[1] - BALL_RADIUS <= 0 or self.center[1] + BALL_RADIUS >= HEIGHT:
            self.velocity_y *= -1
        new_center = (
            self.center[0] + self.velocity_x,
            self.center[1] + self.velocity_y
        )
        self.center = new_center

    def apply_random_variation(self, paddle_direction):
        # Ensure ball continues to move away from the paddle with a small random angle
        self.velocity_x = abs(self.velocity_x) * paddle_direction  # Ensure direction is away from paddle
        self.velocity_y += random.uniform(-VELOCITY_VARIATION_AMOUNT, VELOCITY_VARIATION_AMOUNT)
        # Keep velocities within minimum and maximum speed limits
        self.velocity_x = max(MIN_SPEED, min(MAX_SPEED, abs(self.velocity_x))) * paddle_direction
        self.velocity_y = max(MIN_SPEED, min(MAX_SPEED, abs(self.velocity_y))) * (1 if self.velocity_y > 0 else -1)

# Paddle class with canvas updates
class Paddle(s.Polygon):
    def __init__(self, center, width, height, color):
        self.width = width
        self.height = height
        self.center = center
        vertices = get_rectangle_vertices(center, width, height)
        super().__init__(vertices, color)

    def move(self, direction):
        new_y = self.center[1] + (direction * PADDLE_SPEED)
        if PADDLE_HEIGHT // 2 <= new_y <= HEIGHT - PADDLE_HEIGHT // 2:
            self.translate(0, direction * PADDLE_SPEED)
            self.center = (self.center[0], new_y)

    def ai_move(self, ball_y):
        # Calculate the difference between ball and paddle position
        diff = ball_y - self.center[1]
        
        # Move paddle based on the difference
        if abs(diff) > PADDLE_SPEED:  # Only move if the difference is significant
            if diff > 0:
                self.move(1)
            else:
                self.move(-1)

# Initialize game objects
ball = Ball(BALL_RADIUS, (WIDTH // 2, HEIGHT // 2), (200, 0, 0), -BALL_SPEED, BALL_SPEED / 1.4)
paddle1 = Paddle((PADDLE_WIDTH, HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT, (0, 220, 0))
paddle2 = Paddle((WIDTH - PADDLE_WIDTH, HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT, (15, 120, 15))

# Add initial shapes to canvas
canvas.add(ball)
canvas.add(paddle1)
canvas.add(paddle2)

# Game loop
move_counter = 0  # Counter to control AI movement frequency
while True:
    canvas.clear()
    
    # Check for paddle movement
    if gamepad.active_keys() == [46]:
        paddle1.move(-1)
    if gamepad.active_keys() == [32]:
        paddle1.move(1)
    if gamepad.active_keys() == [24]:
        exit_prog()
    
    # AI movement for paddle2
    move_counter += 1
    if move_counter >= AI_REACTION_SPEED:
        paddle2.ai_move(ball.center[1])
        move_counter = 0
    
    # Move ball
    ball.update_position()

    # Collision detection with paddles
    if (
        abs(ball.center[0] - paddle1.center[0]) < BALL_RADIUS + PADDLE_WIDTH // 2
        and abs(ball.center[1] - paddle1.center[1]) < PADDLE_HEIGHT // 2
    ):
        ball.velocity_x *= -1  # Reverse direction
        ball.apply_random_variation(1)  # Apply variation moving to the right
    elif (
        abs(ball.center[0] - paddle2.center[0]) < BALL_RADIUS + PADDLE_WIDTH // 2
        and abs(ball.center[1] - paddle2.center[1]) < PADDLE_HEIGHT // 2
    ):
        ball.velocity_x *= -1  # Reverse direction
        ball.apply_random_variation(-1)  # Apply variation moving to the left

    # Re-add all objects to ensure proper rendering
    canvas.add(ball)
    canvas.add(paddle1)
    canvas.add(paddle2)
    
    # Draw the updated canvas
    canvas.draw()

    # Pause for frame rate control
    time.sleep(SLEEP_TIME)
