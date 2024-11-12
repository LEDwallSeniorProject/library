from matrix_library import shapes as s
from PIL import Image
import numpy as np
import time

class Canvas:
    def __init__(self, backgroundcolor=(0, 0, 0), renderMode="zmq"):
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

        if renderMode == "zmq":
            import zmq

            # Create the ZMQ connection
            self.context = zmq.Context()

            #  Socket to talk to server
            #print("Connecting to LED ZMQ server…")
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect("tcp://localhost:55000")

        if renderMode == "pygame":
            import pygame

            # Initialize pygame
            pygame.init()
            self.screen = pygame.display.set_mode((640, 640))
            pygame.display.set_caption("Canvas")

        if renderMode == "led":
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
            options.limit_refresh_rate_hz = 60
            options.show_refresh_rate = False
            self.matrix = m.RGBMatrix(options=options)
            self.frame_canvas = self.matrix.CreateFrameCanvas()

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

        if isinstance(item, s.ColoredBitMap):
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
        # FPS = 30
        # passed_time = time.perf_counter() - self.prev_frame_time
        # if passed_time < 1 / FPS:
        #     # time.sleep(1/FPS - passed_time)
        #     pass
        # # print("FPS:", 1/(passed_time))

        # # # # # # ## 
        # START - Rendering functions

        # Rendering for PyGame
        if renderMode == "pygame":
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
        if renderMode == "led":

            # convert the numpy array to a PIL image
            frame = Image.fromarray(self.canvas)
            self.frame_canvas.SetImage(frame)

            # Swap the frames between the working frames
            self.frame_canvas = self.matrix.SwapOnVSync(self.frame_canvas)
        
        # Rendering for ZMQ
        if renderMode == "zmq":
            
            # convert the numpy array to a PIL image
            frame = Image.fromarray(self.canvas)

            # Convert the image to RGBA mode and rawbytestring
            img = img.convert("RGBA")
            rawimage = img.tobytes()

            # # send the request and receive back a "blank" response
            # # both of these are blocking
            socket.send(rawimage)
            message = socket.recv()

        # END - Rendering functions
        # # # # # # ## 

        # keep track of frame timing for FPS limiter
        # self.prev_frame_time = (
        #     time.perf_counter()
        # )  # Track the time at which the frame was drawn
        # self.frame_count += 1
