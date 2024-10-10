import numpy as np
from matrix_library import shapes as s
import time
from PIL import Image

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
    self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
    self.canvas[:,:] = color
    self.points = self.get_points()
    self.prev_frame_time = time.perf_counter()
    self.frame_count = 0

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
    self.canvas[:,:] = [0,0,0]
  
  def fill(self, color):
    """
    Fills the canvas with the specified color.

    Parameters:
    - color: The color to fill the canvas with.

    Returns:
    None
    """
    self.canvas = np.zeros([128, 128, 3], dtype=np.uint8)
    self.canvas[:,:] = color

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

    mask = item.contains_points(self.points)
    color = item.color
    
    reshaped_mask = mask.reshape(self.canvas.shape[:2])
    self.canvas[reshaped_mask] = color

  def draw(self):
    
    # Limit the frame rate to a specified value
    FPS = 30
    passed_time = time.perf_counter() - self.prev_frame_time
    if passed_time < 1/FPS:
      # time.sleep(1/FPS - passed_time)
      pass
    # print("FPS:", 1/(passed_time))
    
    if debug:
      # Check for the close event
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

      # self.screen.fill(self.color)      # NOT sure if needed
      # OLD fill method
      # for i in range(len(self.canvas)):
      #   for j in range(len(self.canvas[i])):
      #     pygame.draw.rect(self.screen, self.canvas[i][j], (j * 5, i * 5, 5, 5))

      # NEW fill method using pygame blit from a PIL image
      # https://www.tutorialspoint.com/how-to-convert-pil-image-into-pygame-surface-image
      frame = Image.fromarray(self.canvas)
      resized_frame = frame.resize(size = (self.screen.get_height(),self.screen.get_width()), resample = Image.NEAREST)
      pygame_surface = pygame.image.fromstring(resized_frame.tobytes(), resized_frame.size, "RGB")
      self.screen.blit(pygame_surface,(0,0))
    
      pygame.display.flip()

    else: # Display on LED matrix display

      # OLD WAY
      # canvas = self.canvas # Cache locally
      # set_pixel = self.frame_canvas.SetPixel # Cache locally
      # for x, row in enumerate(canvas):
      #   for y, color in enumerate(row):
      #     set_pixel(y, x, color[0], color[1], color[2])

      # convert the numpy array to a PIL image
      frame = Image.fromarray(self.canvas)
      self.frame_canvas.SetImage(frame)
          
      # Swap the frames between the working frames
      self.frame_canvas = self.matrix.SwapOnVSync(self.frame_canvas)
    
    self.prev_frame_time = time.perf_counter() # Track the time at which the frame was drawn
    self.frame_count += 1
    
