import numpy as np
from matrix_library import shapes as s, controller as ctrl
import time
from PIL import Image
import platform
import re
import os
import sys

# Detection of Platform for import
# load pygame on NOT on csledpi
if not (re.search("armv|aarch64", platform.machine()) and re.search("csledpi", platform.node())):
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame

class Canvas:
    def __init__(self, backgroundcolor=(0, 0, 0), fps=30, limitFps=True, renderMode="", zmqRenderTarget="localhost", zmqRenderPort="55000"):
        """
        Initializes a Canvas object with the specified color.

        Parameters:
        - color (tuple): The RGB color value to fill the canvas with. Defaults to (0, 0, 0).

        Attributes:
        - color (tuple): The RGB color value used to fill the canvas.
        - canvas (ndarray): The 4-dimensional NumPy array representing the canvas. RGB+alpha (always 255)
        - points (numpy.ndarray): The NumPy array of points on the canvas.

        Returns:
        None
        """
        self.color = backgroundcolor
        self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
        self.canvas[:, :] = self.color
        self.points = np.array(self.get_points())  # Ensure points are stored as a NumPy array
        self.prev_frame_time = time.perf_counter()
        self.frame_count = 0
        self.fps = fps
        self.limitFps = limitFps
        self.zmqRenderTarget = zmqRenderTarget
        self.zmqRenderPort = zmqRenderPort

        # Auto-detect rendering mode
        if renderMode == "":
            if re.search("armv|aarch64", platform.machine()) and re.search("csledpi", platform.node()):
                self.render = "zmq"
            else:
                self.render = "pygame"
        else:
            self.render = renderMode

        # Set up rendering
        if self.render == "zmq":
            if "zmq" not in sys.modules:
                import zmq
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(f"tcp://{self.zmqRenderTarget}:{self.zmqRenderPort}")

        elif self.render == "led":
            import rgbmatrix as m
            options = m.RGBMatrixOptions()
            options.rows = 64
            options.cols = 64
            options.chain_length = 4
            options.parallel = 1
            options.hardware_mapping = "adafruit-hat-pwm"
            options.pixel_mapper_config = "U-mapper"
            options.gpio_slowdown = 3
            options.drop_privileges = True
            options.limit_refresh_rate_hz = 120
            options.pwm_bits = 6
            options.show_refresh_rate = False
            self.matrix = m.RGBMatrix(options=options)
            self.frame_canvas = self.matrix.CreateFrameCanvas()

        elif self.render == "pygame":
            pygame.init()
            self.screen = pygame.display.set_mode((640, 640))
            pygame.display.set_caption("Canvas")

        else:
            print("Unsupported renderMode given.")
            exit(1)

    def clear(self):
        """Clears the canvas by filling it with black."""
        self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)

    def fill(self, fillcolor):
        """Fills the canvas with the specified color."""
        self.canvas[:, :] = fillcolor

    def get_points(self):
        """
        Returns a 2D array of points representing a grid on a canvas.

        Returns:
            numpy.ndarray: A 2D array of points, where each row represents a point (x, y).
        """
        x, y = np.meshgrid(np.arange(128), np.arange(128))
        x, y = x.flatten(), y.flatten()
        return np.vstack((x, y)).T  # Ensuring it returns a NumPy array

    def add(self, item):
        """
        Adds a shape or bitmap to the canvas.

        Parameters:
            item: The item to be added.

        Returns:
            None
        """
        if isinstance(item, s.ColoredBitMap) or isinstance(item, s.Image):
            for pixel in item.pixels:
                mask = np.array(pixel.contains_points(self.points))  # Convert mask to NumPy array
                color = pixel.color
                reshaped_mask = mask.reshape(self.canvas.shape[:2])
                self.canvas[reshaped_mask] = color
            return

        mask = np.array(item.contains_points(self.points)).reshape(self.canvas.shape[:2])  # Convert mask to NumPy array
        self.canvas[mask] = item.color

    def draw(self):
        """Renders the current frame to the appropriate output device."""

        # Frame rate limiting
        if self.limitFps:
            frame_time = 1 / self.fps
            while (time.perf_counter() - self.prev_frame_time) < frame_time:
                time.sleep(1 / self.fps / 20)  # Small sleep for efficiency

        # Rendering for PyGame
        if self.render == "pygame":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            frame = Image.fromarray(self.canvas)
            resized_frame = frame.resize(
                size=(self.screen.get_height(), self.screen.get_width()),
                resample=Image.NEAREST,
            )
            pygame_surface = pygame.image.fromstring(
                resized_frame.tobytes(), resized_frame.size, "RGB"
            )
            self.screen.blit(pygame_surface, (0, 0))
            pygame.display.flip()

        # Rendering for LED Matrix
        if self.render == "led":
            frame = Image.fromarray(self.canvas)
            self.frame_canvas.SetImage(frame)
            self.frame_canvas = self.matrix.SwapOnVSync(self.frame_canvas)

        # Rendering for ZMQ
        if self.render == "zmq":
            frame = Image.fromarray(self.canvas)
            img = frame.convert("RGBA")
            rawimage = img.tobytes()
            self.socket.send(rawimage)
            message = self.socket.recv()

        # Track frame timing for FPS limiter
        self.prev_frame_time = time.perf_counter()
        self.frame_count += 1

