import numpy as np
from matrix_library import shapes as s, controller as ctrl
import time
from PIL import Image
import platform
import numpy as np
import re
import time
import os
import sys

# load pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# # Detection of Platform for import
# if re.search("armv|aarch64",platform.machine()) and re.search("csledpi",platform.node()):
#     import zmq

class Canvas:
    def __init__(self, backgroundcolor=(0, 0, 0), fps=30, limitFps=True, renderMode="", zmqRenderTarget="localhost", zmqRenderPort="55000"):
        """
        Initializes a Canvas object with the specified color.

        Parameters:
        - color (tuple): The RGB color value to fill the canvas with. Defaults to (0, 0, 0, 255).

        Attributes:
        - color (tuple): The RGB color value used to fill the canvas.
        - canvas (ndarray): The 4-dimensional NumPy array representing the canvas. RGB+alpha (always 255)
        - points (list): The list of points on the canvas.

        Returns:
        None
        """
        self.color = backgroundcolor
        self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
        self.canvas[:, :] = self.color
        self.points = self.get_points()
        self.prev_frame_time = time.perf_counter()
        self.frame_count = 0
        self.fps = fps
        self.limitFps = limitFps
        self.zmqRenderTarget = zmqRenderTarget
        self.zmqRenderPort = zmqRenderPort

        # deal with a blank renderMode; trying to auto-detect the 
        # specific raspberry PI LED Wall we have, otherwise fall back to pygame
        if renderMode == "":

            # first, detect if I'm on a pi/LEDwall system
            if re.search("armv|aarch64",platform.machine()) and re.search("csledpi",platform.node()):
                self.render = "zmq"
            else:
                self.render = "pygame"
        
        else:
            self.render = renderMode

        # specific python module imports and setup depending on rendering mode
        if self.render == "zmq":

            if "zmq" not in sys.modules:
                import zmq

            # Create the ZMQ connection
            self.context = zmq.Context()

            #  Socket to talk to server
            #print("Connecting to LED ZMQ server…")
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(f"tcp://{self.zmqRenderTarget}:{self.zmqRenderPort}")

        elif self.render == "led":
            import rgbmatrix as m

            # Set up the options for the matrix
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


            # Initialize pygame
            pygame.init()
            self.screen = pygame.display.set_mode((640, 640))
            pygame.display.set_caption("Canvas")
        
        else:
            print("Unsupported renderMode given.")
            exit(1)

    def clear(self):
        """
        Clears the canvas by filling it with black.

        Parameters:
        - None

        Returns:
        - None
        """
        self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
        self.canvas[:, :] = [0, 0, 0]

    def fill(self, fillcolor):
        """
        Fills the canvas with the specified color.

        Parameters:
        - color: The color to fill the canvas with.

        Returns:
        None
        """
        self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
        self.canvas[:, :] = fillcolor

    def get_points(self):
        """
        Returns a 2D array of points representing a grid on a canvas.

        Returns:
            numpy.ndarray: A 2D array of points, where each row represents a point (x, y).
        """
        x, y = np.meshgrid(np.arange(128), np.arange(128))
        x, y = x.flatten(), y.flatten()
        return np.vstack((x, y)).T

    def add(self, item):
        """
        Adds a letter or bitmap to the canvas.

        Parameters:
            item: The item to be added.

        Returns:
            None
        """

        if isinstance(item, s.ColoredBitMap) or isinstance(item, s.Image):
            for pixel in item.pixels:
                mask = pixel.contains_points(self.points)
                color = pixel.color

                reshaped_mask = mask.reshape(self.canvas.shape[:2])
                self.canvas[reshaped_mask] = color
            return

        mask = item.contains_points(self.points).reshape(self.canvas.shape[:2])
        self.canvas[mask] = item.color

    def draw(self):

        # # Limit the frame rate to a specified value
        if self.limitFps:
            frame_time = 1 / self.fps
            while((time.perf_counter() - self.prev_frame_time) < frame_time):
                time.sleep(1/self.fps/20)  # sleep for a portion of the frame time

        # # # # # # ## 
        # START - Rendering functions

        # Rendering for PyGame
        if self.render == "pygame":
            # Check for the close event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # NEW fill method using pygame blit from a PIL image
            # https://www.tutorialspoint.com/how-to-convert-pil-image-into-pygame-surface-image
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

        # Rendering for direct LED Matrix
        if self.render == "led":

            # convert the numpy array to a PIL image
            frame = Image.fromarray(self.canvas)
            self.frame_canvas.SetImage(frame)

            # Swap the frames between the working frames
            self.frame_canvas = self.matrix.SwapOnVSync(self.frame_canvas)
        
        # Rendering for ZMQ
        if self.render == "zmq":
            
            # convert the numpy array to a PIL image
            frame = Image.fromarray(self.canvas)

            # Convert the image to RGBA mode and rawbytestring
            img = frame.convert("RGBA")
            rawimage = img.tobytes()

            # # send the request and receive back a "blank" response
            # # both of these are blocking
            self.socket.send(rawimage)
            message = self.socket.recv()

        # END - Rendering functions
        # # # # # # ## 

        # keep track of frame timing for FPS limiter
        self.prev_frame_time = time.perf_counter() # Track the time at which the frame was drawn
        self.frame_count += 1
