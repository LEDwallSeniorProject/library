import random
import sys
import matrix_library as matrix
import time

MENU_STATE = 0
ONE_PLAYER_STATE = 1
TWO_PLAYER_STATE = 2

class PongGame:
    def __init__(self):
        self.exited = False
        self.WIDTH, self.HEIGHT = 128, 126
        self.BALL_RADIUS = 10
        self.PADDLE_WIDTH = 8
        self.PADDLE_HEIGHT = 40
        self.PADDLE_SPEED = 6
        self.BALL_SPEED = 5
        self.AI_REACTION_SPEED = 2
        self.VELOCITY_VARIATION_AMOUNT = 1.5
        self.MIN_SPEED = 3
        self.MAX_SPEED = 8

        # Game state variables
        self.controller = matrix.Controller()
        self.canvas = matrix.Canvas()
        self.exited = False
        self.game_state = MENU_STATE
        self.game_mode = None

        # Setup menu elements
        self.setup_menu()

        # Game variables
        self.player1_score = 0
        self.player2_score = 0
        self.initial_countdown = 3
        self.countdown_timer = 0
        self.post_score_pause = 0

        # Game objects will be initialized in start_game method
        self.ball = None
        self.paddle1 = None
        self.paddle2 = None
        self.score1 = None
        self.score2 = None

        self.setup_controllers()

    def setup_menu(self):
        # Menu options
        self.menu_options = [
            matrix.Phrase("1 Player", (15, 48), (255, 255, 255), size=1),
            matrix.Phrase("2 Players", (15, 68), (255, 255, 255), size=1)
        ]
        self.selected_menu_index = 0
        self.menu_selector = matrix.Polygon(
            matrix.get_polygon_vertices(4, 12, (20, 45)), 
            (0, 255, 0)
        )

    def setup_controllers(self):
        # Menu state controls
        # Both controllers should work for this
        if self.game_state == MENU_STATE:
            self.controller.add_function("UP", self.menu_move_up)
            self.controller.add_function("DOWN", self.menu_move_down)
            self.controller.add_function("Y", self.select_game_mode)
            self.controller.add_function("START", self.exit_prog)

            self.controller.add_function("UP2", self.menu_move_up)
            self.controller.add_function("DOWN2", self.menu_move_down)
            self.controller.add_function("Y2", self.select_game_mode)
            self.controller.add_function("START2", self.exit_prog)

        # Game state controls
        # Setup player 1 and 2 states
        elif self.game_state in [ONE_PLAYER_STATE, TWO_PLAYER_STATE]:
            # setup player 1
            self.controller.add_function("UP", self.move_player1_up)
            self.controller.add_function("DOWN", self.move_player1_down)

            # For two-player mode, add second player controls
            if self.game_state == TWO_PLAYER_STATE:
                self.controller.add_function("UP2", self.move_player2_up)
                self.controller.add_function("DOWN2", self.move_player2_down)

            # For a single player game, both controllers should work for player 1
            else:
                self.controller.add_function("UP2", self.move_player1_up)
                self.controller.add_function("DOWN2", self.move_player1_down)
            
            # Both START buttons should exit
            self.controller.add_function("START", self.exit_prog)
            self.controller.add_function("START2", self.exit_prog)

    def menu_move_up(self):
        self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_options)

    def menu_move_down(self):
        self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_options)

    def select_game_mode(self):
        if self.selected_menu_index == 0:
            self.game_mode = ONE_PLAYER_STATE
        else:
            self.game_mode = TWO_PLAYER_STATE
        self.start_game()

    def start_game(self):
        # Initialize game state
        self.game_state = self.game_mode
        self.player1_score = 0
        self.player2_score = 0
        self.initial_countdown = 3
        self.countdown_timer = 3
        self.post_score_pause = 0

        # Recreate game objects
        self.reset_game_objects()
        
        # Update controller for game state
        self.setup_controllers()

    def reset_game_objects(self):
        # Reset ball
        self.ball = Ball(
            self.BALL_RADIUS, 
            (self.WIDTH // 2, self.HEIGHT // 2), 
            (200, 0, 0), 
            0, 0  # No initial velocity during countdown
        )

        # Reset paddles
        self.paddle1 = Paddle(
            (self.PADDLE_WIDTH, self.HEIGHT // 2), 
            self.PADDLE_WIDTH, 
            self.PADDLE_HEIGHT, 
            (0, 220, 0)
        )

        # Determine paddle2 based on game mode
        if self.game_mode == ONE_PLAYER_STATE:
            self.paddle2 = AIpaddle(
                (self.WIDTH - self.PADDLE_WIDTH, self.HEIGHT // 2), 
                self.PADDLE_WIDTH, 
                self.PADDLE_HEIGHT, 
                (15, 120, 15)
            )
        else:  # Two-player mode
            self.paddle2 = Paddle(
                (self.WIDTH - self.PADDLE_WIDTH, self.HEIGHT // 2), 
                self.PADDLE_WIDTH, 
                self.PADDLE_HEIGHT, 
                (0, 0, 255)  # Changed to blue for two-player mode
            )

        # Reset scores
        self.score1 = matrix.Phrase(str(self.player1_score), [13, 120])
        self.score2 = matrix.Phrase(str(self.player2_score), [108, 120])

    def reset_ball(self):
        # Reset ball position to center 
        self.ball.center = (self.WIDTH // 2, self.HEIGHT // 2)
        
        # Randomize ball direction
        direction = random.choice([-1, 1])
        self.ball.velocity_x = direction * self.BALL_SPEED
        self.ball.velocity_y = self.BALL_SPEED / 1.4

    def move_player1_up(self):
        self.paddle1.move(-1)

    def move_player1_down(self):
        self.paddle1.move(1)

    def move_player2_up(self):
        self.paddle2.move(-1)

    def move_player2_down(self):
        self.paddle2.move(1)

    def exit_prog(self):
        global canvas, exited
        print("quit")
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.15)
        self.exited = True

    def run(self):
        move_counter = 0

        while True:
            if self.exited:
                sys.exit(0)

            self.canvas.clear()

            if self.game_state == MENU_STATE:
                self.render_menu()
            else:
                self.update_game(move_counter)
                move_counter += 1

            self.canvas.draw()
            time.sleep(1/30)

    def render_menu(self):
        # Update selector position
        current_center = self.menu_selector.get_center()
        selector_y = 51 + self.selected_menu_index * 20
        dx = -2 - current_center[0]
        dy = selector_y - current_center[1]
        self.menu_selector.translate(dx, dy)

        # Add menu elements
        for option in self.menu_options:
            self.canvas.add(option)
        self.canvas.add(self.menu_selector)

    def update_game(self, move_counter):
        # Initial countdown logic (only at the start of the game)
        if self.initial_countdown and self.countdown_timer > 0:
            self.countdown_timer -= 1/30
            countdown_text = matrix.Phrase(
                str(int(self.countdown_timer) + 1), 
                [56, 30],  # Moved higher on the screen
                (255, 255, 255), 
                size=2
            )
            
            # Add all game objects so the game layout is visible behind countdown
            game_objects = [
                self.ball, 
                self.paddle1, 
                self.paddle2, 
                self.score1, 
                self.score2,
                countdown_text
            ]
            for obj in game_objects:
                self.canvas.add(obj)
            
            # When countdown expires, release the ball
            if self.countdown_timer <= 0:
                self.initial_countdown = False
                self.reset_ball()
            return

        # AI movement for one-player mode
        if self.game_mode == ONE_PLAYER_STATE and move_counter >= self.AI_REACTION_SPEED:
            self.paddle2.ai_move(self.ball.center[1])
            move_counter = 0

        # Ball movement
        self.ball.update_position(
            self, 
            self.paddle1, 
            self.paddle2, 
            self.reset_ball
        )

        # Update scores
        self.score1.set_text(str(self.player1_score))
        self.score2.set_text(str(self.player2_score))

        # Add all game objects
        game_objects = [
            self.ball, 
            self.paddle1, 
            self.paddle2, 
            self.score1, 
            self.score2
        ]
        for obj in game_objects:
            self.canvas.add(obj)

class Ball(matrix.Circle):
    def __init__(self, radius, center, color, velocity_x, velocity_y):
        super().__init__(radius, center, color)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update_position(self, game, paddle1, paddle2, reset_callback):
        # Check for scoring
        if self.center[0] + game.BALL_RADIUS < 0:
            game.player2_score += 1
            reset_callback()
            return
        elif self.center[0] - game.BALL_RADIUS > game.WIDTH:
            game.player1_score += 1
            reset_callback()
            return

        # First ball launch after countdown
        if self.velocity_x == 0 and self.velocity_y == 0:
            direction = random.choice([-1, 1])
            self.velocity_x = direction * game.BALL_SPEED
            self.velocity_y = game.BALL_SPEED / 1.4

        # Vertical boundary bounce
        if (self.center[1] - game.BALL_RADIUS <= 0 or 
            self.center[1] + game.BALL_RADIUS >= game.HEIGHT):
            self.velocity_y *= -1

        # Update position
        new_center = (
            self.center[0] + self.velocity_x,
            self.center[1] + self.velocity_y
        )
        self.center = new_center

        # Paddle collision detection
        self.check_paddle_collision(game, paddle1, paddle2)

    def check_paddle_collision(self, game, paddle1, paddle2):
        # Paddle1 collision
        if (abs(self.center[0] - paddle1.center[0]) < game.BALL_RADIUS + game.PADDLE_WIDTH // 2 and 
            abs(self.center[1] - paddle1.center[1]) < game.PADDLE_HEIGHT // 2):
            self.velocity_x = abs(self.velocity_x)
            self.apply_random_variation(game, 1)

        # Paddle2 collision  
        elif (abs(self.center[0] - paddle2.center[0]) < game.BALL_RADIUS + game.PADDLE_WIDTH // 2 and 
              abs(self.center[1] - paddle2.center[1]) < game.PADDLE_HEIGHT // 2):
            self.velocity_x = -abs(self.velocity_x)
            self.apply_random_variation(game, -1)

    def apply_random_variation(self, game, paddle_direction):
        # Ensure ball continues to move away from the paddle with a small random angle
        self.velocity_x = abs(self.velocity_x) * paddle_direction
        self.velocity_y += random.uniform(-game.VELOCITY_VARIATION_AMOUNT, game.VELOCITY_VARIATION_AMOUNT)
        
        # Limit velocities
        self.velocity_x = max(game.MIN_SPEED, min(game.MAX_SPEED, abs(self.velocity_x))) * paddle_direction
        self.velocity_y = max(game.MIN_SPEED, min(game.MAX_SPEED, abs(self.velocity_y))) * (1 if self.velocity_y > 0 else -1)

class Paddle(matrix.Polygon):
    def __init__(self, center, width, height, color):
        self.width = width
        self.height = height
        self.center = center
        vertices = self._get_rectangle_vertices(center, width, height)
        super().__init__(vertices, color)

    def _get_rectangle_vertices(self, center, width, height):
        x, y = center
        return [
            (x - width // 2, y - height // 2),  # Top-left
            (x + width // 2, y - height // 2),  # Top-right
            (x + width // 2, y + height // 2),  # Bottom-right
            (x - width // 2, y + height // 2),  # Bottom-left
        ]

    def move(self, direction):
        # Calculate new paddle position
        new_y = self.center[1] + (direction * 6)  # Hardcoded paddle speed
        
        # Keep paddle within screen boundaries
        if 20 <= new_y <= 106:  # Adjusted for paddle height
            self.translate(0, direction * 6)
            self.center = (self.center[0], new_y)

class AIpaddle(Paddle):
    def ai_move(self, ball_y):
        # Calculate the difference between ball and paddle position
        diff = ball_y - self.center[1]
        
        # Move paddle based on the difference
        if abs(diff) > 6:  # Only move if the difference is significant
            direction = 1 if diff > 0 else -1
            self.move(direction)

# Main execution
if __name__ == "__main__":
    game = PongGame()
    game.run()