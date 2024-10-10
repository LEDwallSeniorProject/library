import numpy as np
from matrix_library import shapes as s
import time
from PIL import Image

try:
    import rgbmatrix as m
    debug = False
except ImportError:
    import pygame
    debug = True

class Canvas:
    def __init__(self, color=(0, 0, 0)):
        self.color = color
        self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
        self.canvas[:, :] = color
        self.points = self.get_points()
        self.prev_frame_time = time.perf_counter()
        self.shapes = []  # List to store shapes

        if debug:
            pygame.init()
            self.screen = pygame.display.set_mode((640, 640))
            pygame.display.set_caption("Canvas")
        else:
            # Set up the options for the matrix
            options = m.RGBMatrixOptions()
            options.rows = 64
            options.cols = 64
            options.chain_length = 4
            options.parallel = 1
            options.hardware_mapping = 'adafruit-hat-pwm'
            options.pixel_mapper_config = 'U-mapper'
            options.gpio_slowdown = 3
            
            options.limit_refresh_rate_hz = 60
            options.show_refresh_rate = False
            
            self.matrix = m.RGBMatrix(options=options)
            self.frame_canvas = self.matrix.CreateFrameCanvas()

    def clear(self):
        self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
        self.canvas[:, :] = [0, 0, 0]

    def fill(self, color):
        self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
        self.canvas[:, :] = color

    def get_points(self):
        x, y = np.meshgrid(np.arange(128), np.arange(128))
        x, y = x.flatten(), y.flatten()
        return np.vstack((x, y)).T

    def add(self, item):
        """
        Adds a shape to the shapes list.

        Parameters:
          item: The shape to be added.

        Returns:
          None
        """
        self.shapes.append(item)  # Store the shape in the list

    def draw(self):
        # Clear the canvas before drawing
        self.clear()  # Clear the canvas for the new frame

        for item in self.shapes:
            if isinstance(item, s.ColoredBitMap):
                for pixel in item.pixels:
                    mask = pixel.contains_points(self.points)
                    color = pixel.color
                    reshaped_mask = mask.reshape(self.canvas.shape[:2])
                    self.canvas[reshaped_mask] = color
            else:
                mask = item.contains_points(self.points)
                color = item.color
                reshaped_mask = mask.reshape(self.canvas.shape[:2])
                self.canvas[reshaped_mask] = color

        # Limit the frame rate to a specified value
        FPS = 30
        passed_time = time.perf_counter() - self.prev_frame_time
        if passed_time < 1 / FPS:
            # time.sleep(1/FPS - passed_time)
            pass

        if debug:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # Using PIL to create a Pygame surface
            frame = Image.fromarray(self.canvas)
            resized_frame = frame.resize(size=(self.screen.get_height(), self.screen.get_width()), resample=Image.NEAREST)
            pygame_surface = pygame.image.fromstring(resized_frame.tobytes(), resized_frame.size, "RGB")
            self.screen.blit(pygame_surface, (0, 0))
            pygame.display.flip()
        else:
            # Display on LED matrix display
            frame = Image.fromarray(self.canvas)
            self.frame_canvas.SetImage(frame)
            self.frame_canvas = self.matrix.SwapOnVSync(self.frame_canvas)

        # Clear the shapes list for the next frame
        self.shapes.clear()  # Empty the shapes list

        self.prev_frame_time = time.perf_counter()  # Update the frame time
