import numpy as np
import matrix_library
from matrix_library import shapes as s

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
  
  def add(self, polygon: s.Polygon):
    """
    Adds a polygon to the canvas.

    Parameters:
      polygon (s.Polygon): The polygon to be added.

    Returns:
      None
    """
    mask = polygon.contains_points(self.points)
    for i in range(len(self.canvas)):
      for j in range(len(self.canvas[i])):
        if mask[i * 128 + j]:
          self.canvas[i][j] = polygon.color

  def draw(self):
    # TODO: Detect if we are connected to the LED matrix
    row = ""
    for i in range(len(self.canvas)):
      for j in range(len(self.canvas[i])):
        if self.canvas[i][j][0] == 0 and self.canvas[i][j][1] == 0 and self.canvas[i][j][2] == 0:
          row += "-"
        else:
          row += "X"
        # row += f"{self.canvas[i][j][0]} {self.canvas[i][j][1]} {self.canvas[i][j][2]} "
      row += "\n"
    print(row)