import numpy as np
from matrix_library import shapes as s
import time

try:
  import rgbmatrix as m
  debug = False
except:
  import pygame
  debug = True

class Canvas:
  def __init__(self, color=(0, 0, 0)):
    """
    Initializes a Canvas object with the specified color.

    Parameters:
    - color (tuple): The RGB color value to fill the canvas with. Defaults to (0, 0, 0).

    Attributes:
    - color (tuple): The RGB color value used to fill the canvas.
    - canvas (ndarray): The 3-dimensional NumPy array representing the canvas.
    - points (list): The list of points on the canvas.

    Returns:
    None
    """
    self.color = color
    self.canvas = np.full((128, 128, 3), self.color)
    self.points = self.get_points()
    self.prev_frame_time = time.perf_counter()

    if debug:
      pygame.init()
      self.screen = pygame.display.set_mode((640, 640))
      pygame.display.set_caption("Canvas")
      self.clock = pygame.time.Clock()
  
  def clear(self):
    """
    Clears the canvas by filling it with the specified color.

    Parameters:
    - None

    Returns:
    - None
    """
    self.canvas = np.full((128, 128, 3), self.color)
  
  def fill(self, color):
    """
    Fills the canvas with the specified color.

    Parameters:
    - color: The color to fill the canvas with.

    Returns:
    None
    """
    self.canvas = np.full((128, 128, 3), color)

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
        for i in range(len(self.canvas)):
          for j in range(len(self.canvas[i])):
            if mask[i * 128 + j]:
              self.canvas[i][j] = color
      return  # Early return after processing all bitmaps

    mask = item.contains_points(self.points)
    color = item.color
    
    # Process the letter after checking it
    for i in range(len(self.canvas)):
      for j in range(len(self.canvas[i])):
          if mask[i * 128 + j]:
              self.canvas[i][j] = color


  def draw(self):
    
    # Limit the frame rate to a specified value
    FPS = 30
    passed_time = time.perf_counter() - self.prev_frame_time
    if passed_time < 1/FPS:
      time.sleep(1/FPS - passed_time)
      
    # TODO: Detect if we are connected to the LED matrix
    if debug:

      # Check for the close event
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

      self.screen.fill(self.color)

      for i in range(len(self.canvas)):
        for j in range(len(self.canvas[i])):
          pygame.draw.rect(self.screen, self.canvas[i][j], (j * 5, i * 5, 5, 5))
    
      pygame.display.flip()

    else: # Display on LED matrix display
      print("START")
      # Set up the options for the matrix
      options = m.RGBMatrixOptions()
      options.rows = 64
      options.cols = 64
      options.chain_length = 4
      options.parallel = 1
      options.hardware_mapping = 'adafruit-hat-pwm'
      options.pixel_mapper_config = 'U-mapper'
      options.gpio_slowdown = 4
      options.drop_privileges = False
      
      matrix = m.RGBMatrix(options=options)
      for x in range(len(self.canvas)):
        for y in range(len(self.canvas[x])):
          matrix.SetPixel(x, y, self.canvas[x][y][0], self.canvas[x][y][1], self.canvas[x][y][2])
      canvas = matrix.CreateFrameCanvas()
      canvas = matrix.SwapOnVSync(canvas)
    
    self.prev_frame_time = time.perf_counter() # Track the time at which the frame was drawn