from matplotlib.path import Path
import numpy as np
import math

class Polygon:
  def __init__(self, vertices: list, color: tuple=(255, 255, 255)):
    """
    Initializes a Polygon object with the given vertices and color.
    Parameters:
    - vertices (list): A list of vertices that define the polygon. Must have at least 3 vertices.
    - color (tuple, optional): The color of the polygon. Defaults to (255, 255, 255).
    Raises:
    - ValueError: If the number of vertices is less than 3.
    Returns:
    - None
    """
    if len(vertices) < 3:
      raise ValueError("A polygon must have at least 3 vertices")
    
    self.vertices = vertices
    self.path = Path(vertices)
    self.color = color
    self.center = self.get_center()

  def contains_points(self, points):
    return self.path.contains_points(points)

  def translate(self, dx: float, dy: float):
    """
    Translate the shape by a specified distance along the x and y axes.

    Parameters:
    - dx: The distance to translate the shape along the x axis.
    - dy: The distance to translate the shape along the y axis.

    Returns:
    - A list of tuples representing the translated vertices of the shape.
    """
    translated_vertices = []
    
    for (x, y) in self.vertices:
        x_translated = x + dx
        y_translated = y + dy
        translated_vertices.append((x_translated, y_translated))
    
    self.change_vertices(translated_vertices)
    self.center = (self.center[0] + dx, self.center[1] + dy)
  
  def rotate(self, angle_degrees: float, center: tuple=(0, 0)):
    """
    Rotate the shape by a specified angle around a given center.

    Parameters:
    - vertices: List of tuples representing the vertices of the shape.
    - angle_degrees: The angle by which to rotate the shape (in degrees).
    - center: Tuple (x, y) representing the center of rotation (default is (0, 0)).

    Returns:
    - A list of tuples representing the rotated vertices of the shape.
    """
    # Convert angle from degrees to radians
    angle_radians = math.radians(angle_degrees)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    
    rotated_vertices = []
    
    for (x, y) in self.vertices:
        # Translate point to origin
        x_translated = x - center[0]
        y_translated = y - center[1]
        
        # Apply rotation
        x_rotated = x_translated * cos_angle - y_translated * sin_angle
        y_rotated = x_translated * sin_angle + y_translated * cos_angle
        
        # Translate point back
        x_final = x_rotated + center[0]
        y_final = y_rotated + center[1]
        
        rotated_vertices.append((x_final, y_final))
    
    self.change_vertices(rotated_vertices)

  def change_vertices(self, vertices: tuple):
    self.vertices = vertices
    self.path = Path(vertices)
  
  def get_center(self):
    n = len(self.vertices)
    if n < 3:
        raise ValueError("A polygon must have at least 3 vertices.")

    # Initialize variables
    cx, cy = 0.0, 0.0
    area = 0.0

    # Calculate the signed area of the polygon
    for i in range(n):
        x1, y1 = self.vertices[i]
        x2, y2 = self.vertices[(i + 1) % n]
        a = x1 * y2 - x2 * y1
        area += a
        cx += (x1 + x2) * a
        cy += (y1 + y2) * a

    area *= 0.5
    if area == 0:
        raise ValueError("Area of the polygon is zero.")
    
    cx /= (6 * area)
    cy /= (6 * area)

    return (cx, cy)

def get_polygon_vertices(sides: int, radius: float=1, center: tuple=(0, 0)):
    """
    Calculate the vertices of a regular polygon.

    Parameters:
    - sides: Number of sides of the polygon.
    - radius: Radius of the circumcircle of the polygon (default is 1).
    - center: Tuple (x, y) representing the center of the polygon (default is (0, 0)).

    Returns:
    - A list of tuples representing the vertices of the polygon.
    """
    if sides < 3:
        raise ValueError("A polygon must have at least 3 sides")
    
    vertices = []
    angle_step = 2 * math.pi / sides
    
    for i in range(sides):
        angle = i * angle_step
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
    
    return vertices

class Circle(Polygon):
  def __init__(self, radius: float, center: tuple, color: tuple=(255, 255, 255)):
    """
    Initializes a Shape object with the given radius, center, and color.

    Parameters:
    - radius (float): The radius of the shape.
    - center (tuple): The center coordinates of the shape.
    - color (tuple, optional): The RGB color values of the shape. Defaults to (255, 255, 255).
    """
    vertices = get_polygon_vertices(radius * 10, radius, center)
    super().__init__(vertices, color)
    self.radius = radius
    # self.center = center

class Line(Polygon):
  def __init__(self, start: list, end: list, color: list=(255, 255, 255), thickness: float=0.5):
    if start == end:
      raise ValueError("The start and end points of a line cannot be the same.")
    elif thickness <= 0:
      raise ValueError("The thickness of a line must be greater than 0.")
    elif len(start) != 2 or len(end) != 2:
      raise ValueError("The start and end points must be list of length 2.")
    elif len(color) != 3:
      raise ValueError("The color must be a list of length 3.")
    
    self.start = start
    self.end = end
    self.thickness = thickness
    self.length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    
    # Calculate the angle of the line
    self.angle = self.calculate_angle()
    self.end = [self.start[0], self.start[1] + self.length]
    
    verts1 = [self.start[0] + self.thickness, self.start[1] + self.thickness]
    verts2 = [self.start[0] + self.thickness, self.start[1] - self.thickness]
    verts3 = [self.start[0] - self.thickness, self.start[1] - self.thickness]
    verts4 = [self.start[0] - self.thickness, self.start[1] + self.thickness]
    verts5 = [self.end[0] - self.thickness, self.end[1] - self.thickness]
    verts6 = [self.end[0] - self.thickness, self.end[1] + self.thickness] 
    verts7 = [self.end[0] + self.thickness, self.end[1] + self.thickness]
    verts8 = [self.end[0] + self.thickness, self.end[1] - self.thickness]
    self.vertices = [verts1, verts2, verts3, verts4, verts5, verts6, verts7, verts8]

    self.rotate(-self.angle, self.start)

    self.path = Path(self.vertices)
    self.color = color
  
  def calculate_angle(self):
    line1 = (self.end[0] - self.start[0], self.end[1] - self.start[1])
    line2 = (0, 1)
    
    dot_product = line1[0] * line2[0] + line1[1] * line2[1]
    magnitude_line1 = math.sqrt(line1[0] ** 2 + line1[1] ** 2)
    magnitude_line2 = math.sqrt(line2[0] ** 2 + line2[1] ** 2)
    
    cos_angle = dot_product / (magnitude_line1 * magnitude_line2)
    angle_rads = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rads)
    
    return angle_deg

# TODO: Implement PolygonOutline class features
class PolygonOutline(Polygon):
  def __init__(self, vertices: tuple, color: tuple=(255, 255, 255), thickness: float=1):
    """
    Initializes a PolygonOutline object with the given vertices, color, and thickness.

    Parameters:
    - vertices (list): A list of vertices that define the polygon.
    - color (tuple, optional): The color of the polygon outline. Defaults to (255, 255, 255).
    - thickness (float, optional): The thickness of the polygon outline. Defaults to 1.
    """
    self.vertices = vertices
    self.color = color
    self.thickness = thickness
    self.center = self.get_center()
    self.inner_vertices = get_polygon_vertices(len(self.vertices), self.distance(self.center[0], self.center[1], self.vertices[0][0], self.vertices[0][1]) - self.thickness, self.center)

  def change_inner_vertices(self, inner_vertices):
    self.inner_vertices = inner_vertices
    self.path = Path(self.inner_vertices)
  
  def rotate_inner(self, angle_degrees: float, center: tuple=(0, 0)):
    # Convert angle from degrees to radians
    angle_radians = math.radians(angle_degrees)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    
    rotated_vertices = []
    
    for (x, y) in self.inner_vertices:
        # Translate point to origin
        x_translated = x - center[0]
        y_translated = y - center[1]
        
        # Apply rotation
        x_rotated = x_translated * cos_angle - y_translated * sin_angle
        y_rotated = x_translated * sin_angle + y_translated * cos_angle
        
        # Translate point back
        x_final = x_rotated + center[0]
        y_final = y_rotated + center[1]
        
        rotated_vertices.append((x_final, y_final))
    
    self.change_inner_vertices(rotated_vertices)

  def rotate(self, angle_degrees: float, center: tuple=(0, 0)):
    super().rotate(angle_degrees, center)
    self.rotate_inner(angle_degrees, center)
  
  def distance(self, x1, y1, x2, y2): 
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

  def contains_points(self, points: np.ndarray):
    mask = np.zeros(len(points), dtype=bool)

    poly1_mask = Polygon(self.vertices, self.color).contains_points(points)
    poly2_mask = Polygon(self.inner_vertices, self.color).contains_points(points)

    mask = np.logical_and(poly1_mask, np.logical_not(poly2_mask))
    return mask
  

class CircleOutline(PolygonOutline):
  def __init__(self, radius, center, color=(255, 255, 255), thickness=1):
    """
    Initializes a CircleOutline object with the given radius, center, color, and thickness.

    Parameters:
    - radius (float): The radius of the circle outline.
    - center (tuple): The center coordinates of the circle outline.
    - color (tuple, optional): The RGB color values of the circle outline. Defaults to (255, 255, 255).
    - thickness (float, optional): The thickness of the circle outline. Defaults to 1.
    """
    vertices = get_polygon_vertices(radius * 10, radius, center)
    super().__init__(vertices, color, thickness)
    self.radius = radius
  
  def contains_points(self, points: np.ndarray):
    mask = np.zeros(len(points), dtype=bool)
    
    circle1_mask = Circle(self.radius, self.center, self.color).contains_points(points)
    circle2_mask = Circle(self.radius - self.thickness, self.center, self.color).contains_points(points)

    mask = np.logical_and(circle1_mask, np.logical_not(circle2_mask))
    return mask

class Phrase:
    def __init__(self, text: str, position: list=[0, 0], color:list=[255, 255, 255], size: int=1, auto_newline:bool=False):
        self.text: str = text
        self.position: list = list(position)
        self.color = color
        self.auto_newline = auto_newline
        self.size: int = size
        self.letters = self.get_letters()
    
    def set_text(self, text: str):
        # Only update letters for characters that have changed
        if text != self.text:
            self.update_letters(text)
        self.text = text
    
    def set_position(self, position: list):
        # Only update letters if the position has changed
        if position != self.position:
            self.position = position
            self.update_positions()
    
    def get_width(self):
        return sum([letter.get_width() for letter in self.letters])

    def translate(self, dx: float, dy: float):
        for letter in self.letters:
            letter.translate(dx, dy)
        self.position[0] += dx
        self.position[1] += dy
    
    def get_letters(self):
        """Initial creation of the letters based on the text and position."""
        letters = []
        x, y = self.position
        for char in self.text:
            if self.auto_newline and x >= 128 - (8 * self.size):
                x = self.position[0]
                y += 8 * self.size
            letters.append(Letter(char, [x, y], self.color, size=self.size))
            x += 8 * self.size
        return letters

    def update_letters(self, new_text: str):
        """Update only the letters that have changed."""
        x, y = self.position
        new_letters = []
        for i, char in enumerate(new_text):
            if self.auto_newline and x >= 128 - (8 * self.size):
                x = self.position[0]
                y += 8 * self.size
            # Update existing letters if they match the index, otherwise create a new one
            if i < len(self.letters) and self.letters[i].char == char:
                new_letters.append(self.letters[i])  # Reuse the existing letter
            else:
                new_letters.append(Letter(char, [x, y], self.color, size=self.size))  # New letter for changed or new char
            x += 8 * self.size
        
        self.letters = new_letters

    def update_positions(self):
        """Update the positions of all letters based on the new starting position."""
        x, y = self.position
        for letter in self.letters:
            letter.set_position([x, y])
            x += 8 * self.size
            if self.auto_newline and x >= 128 - (8 * self.size):
                x = self.position[0]
                y += 8 * self.size

    def contains_points(self, points: np.ndarray):
        mask = np.zeros(len(points), dtype=bool)
        for letter in self.letters:
            mask |= letter.contains_points(points)
        return mask


class Pixel:
  def __init__(self, position: list, color: list=[255, 255, 255], scale: int=1):
    self.position = position
    self.color = color
    self.scale = scale
  
  def contains_points(self, points: np.ndarray):
    mask = np.zeros(len(points), dtype=bool)
    x, y = self.position
    for i in range(self.scale):
      for j in range(self.scale):
        mask |= np.logical_and(
            np.logical_and(points[:, 0] >= x + i, points[:, 0] < x + i + 1),
            np.logical_and(points[:, 1] >= y + j, points[:, 1] < y + j + 1)
        )
    return mask
  
  def translate(self, dx: float, dy: float):
    self.position[0] += dx
    self.position[1] += dy

class ColoredBitMap:
  def __init__(self, pixels: list, width: int, height: int, position: list=[0, 0], scale: int=1):
    self.pixels = pixels
    self.position = position
    self.width = width
    self.height = height
    self.scale = scale
    self.pixels = []
    
    for i in range(len(pixels)):
      if pixels[i] != [] and pixels[i] != [None]: # Skip empty pixels
        x = (i % width) * scale
        y = (i // width) * scale
        
        self.pixels.append(Pixel([x, y], pixels[i]))

class BitMap:
  def __init__(self, pixels: list, width: int, height: int, position: list=[0, 0], color: list = (255, 255, 255), scale: int=1):
    self.pixels = pixels
    self.position = position
    self.width = width
    self.height = height
    self.scale = scale
    self.color = color
  
  def contains_points(self, points: np.ndarray):
    mask = np.zeros(len(points), dtype=bool)
    
    for i in range(len(self.pixels)):
        x = (i % self.width) * self.scale
        y = (i // self.width) * self.scale
        if self.pixels[i] == 1:
            mask |= np.logical_and(
                np.logical_and(points[:, 0] >= x + self.position[0], points[:, 0] < x + self.position[0] + self.scale),
                np.logical_and(points[:, 1] >= y + self.position[1], points[:, 1] < y + self.position[1] + self.scale)
            )
    
    return mask

  def translate(self, dx: float, dy: float):
    self.position[0] += dx
    self.position[1] += dy
  
class Letter(BitMap):
  def __init__(self, char: str, position: list=[0, 0], color:list=[255, 255, 255], size: int=1):
    self.char = char
    
    self.mask_lookup = self.init_char_mask_lookup()
    
    # Make the char_mask a bitmap
    char_mask = self.get_char_mask()
    
    super().__init__(char_mask, 8, 8, position, color, size)
  
  def get_width(self):
    return 8 * self.scale
  
  def get_char_mask(self):
    if self.char in self.mask_lookup:
      return self.mask_lookup[self.char]
    else:
      return [ # Return an checkered pattern if the character is not found
        False,True,False,True,False,True,False,True,
        True,False,True,False,True,False,True,False,
        False,True,False,True,False,True,False,True,
        True,False,True,False,True,False,True,False,
        False,True,False,True,False,True,False,True,
        True,False,True,False,True,False,True,False,
        False,True,False,True,False,True,False,True,
        True,False,True,False,True,False,True,False,
      ]
    
  def init_char_mask_lookup(self):
    return { # 8x8 mask for each letter
      ' ': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '0': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,True,True,True,False,
        False,True,True,True,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '1': [
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '2': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      '3': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '4': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,True,True,False,False,
        False,True,True,False,True,True,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '5': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,True,False,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,False,False,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False, 
        False,False,False,False,False,False,False,False, 
      ],
      '6': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '7': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '8': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '9': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,True,False,
        False,False,False,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'a': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,False,True,True, 
        False,False,False,False,False,False,False,False,
      ],
      'b': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'c': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'd': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,True,True,False,
        False,False,False,False,False,True,True,False,
        False,False,True,True,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'e': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,False,False,False,
        False,False,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'f': [
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,True,False,False,
        False,False,True,True,False,False,False,False,
        False,True,True,True,True,False,False,False,
        False,False,True,True,False,False,False,False,
        False,False,True,True,False,False,False,False,
        False,False,True,True,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'g': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,True,False,
        False,False,False,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
      ],
      'h': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'i': [
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'j': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,True,True,False,False,
        False,True,True,False,True,True,False,False,
        False,False,True,True,True,False,False,False,
      ],
      'k': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,True,True,True,True,False,False,False,
        False,True,True,False,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'l': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'm': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,True,False,True,True,False,
        False,True,True,False,True,False,True,True,
        False,True,True,False,True,False,True,True,
        False,True,True,False,True,False,True,True,
        False,True,True,False,True,False,True,True,
        False,False,False,False,False,False,False,False,
      ],
      'n': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,False,False,False,
        False,True,True,False,True,True,False,False,
        False,True,True,False,True,True,False,False,
        False,True,True,False,True,True,False,False,
        False,True,True,False,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'o': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'p': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
      ],
      'q': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,True,False,
        False,False,False,False,False,True,True,True,
        False,False,False,False,False,True,True,False,
      ],
      'r': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,False,True,True,False,False,
        False,True,True,True,False,True,True,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      's': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      't': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,False,True,True,False,False,False,False,
        False,False,True,True,False,False,False,False,
        False,False,True,True,False,True,True,False,
        False,False,False,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'u': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,False,True,True,
        False,False,False,False,False,False,False,False,
      ],
      'v': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'w': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,False,True,False,True,True,
        False,True,True,False,True,False,True,True,
        False,True,True,False,True,False,True,True,
        False,True,True,False,True,False,True,True,
        False,False,True,True,False,True,True,True,
        False,False,False,False,False,False,False,False,
      ],
      'x': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,True,False,
        False,False,False,True,True,False,False,False,
        False,True,True,True,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'y': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,True,False,
        False,False,False,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
      ],
      'z': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'A': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'B': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'C': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'D': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'E': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'F': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'G': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'H': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'I': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'J': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,True,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,True,True,False,False,
        False,False,False,False,True,True,False,False,
        False,True,True,False,True,True,False,False,
        False,False,True,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'K': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,True,True,False,False,
        False,True,True,True,True,False,False,False,
        False,True,True,True,True,False,False,False,
        False,True,True,False,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'L': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'M': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,False,True,True,
        False,True,True,True,False,True,True,True,
        False,True,True,True,True,True,True,True,
        False,True,True,False,True,False,True,True,
        False,True,True,False,False,False,True,True,
        False,True,True,False,False,False,True,True,
        False,False,False,False,False,False,False,False,
      ],
      'N': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,False,True,True,False,
        False,True,True,True,True,True,True,False,
        False,True,True,False,True,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'O': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'P': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'Q': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,True,True,False,False,
        False,False,True,True,True,False,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'R': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'S': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,False,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'T': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'U': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'V': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'W': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,False,True,True,
        False,True,True,False,False,False,True,True,
        False,True,True,False,True,False,True,True,
        False,True,True,True,True,True,True,True,
        False,True,True,True,False,True,True,True,
        False,True,True,False,False,False,True,True,
        False,False,False,False,False,False,False,False,
      ],
      'X': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      'Y': [
        False,False,False,False,False,False,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,False,True,True,False,
        False,False,True,True,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      'Z': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,False,False,False,False,
        False,True,True,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      '!': [
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '?': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,False,False,False,False,True,True,False,
        False,False,False,True,True,True,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '&': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,False,False,False,
        False,True,True,False,True,True,False,False,
        False,False,True,True,True,False,True,True,
        False,True,True,False,True,True,True,False,
        True,True,False,False,False,True,True,False,
        False,True,True,True,True,False,True,True,
        False,False,False,False,False,False,False,False,
      ],
      '@': [
        False,False,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,True,True,False,False,True,True,False,
        False,True,True,False,True,True,True,False,
        False,True,True,False,True,True,False,False,
        False,True,True,False,False,False,False,False,
        False,False,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
      ],
      '$': [
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,True,True,True,False,
        False,True,False,False,False,False,False,False,
        False,False,True,True,True,True,False,False,
        False,False,False,False,False,False,True,False,
        False,True,True,True,True,True,False,False,
        False,False,False,True,True,False,False,False,
      ],
      '-': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '+': [
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,True,True,True,True,True,True,False,
        False,True,True,True,True,True,True,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '=': [
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
        False,True,True,True,True,True,True,False,
        False,True,True,True,True,True,True,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '*': [
        False,False,False,True,True,False,False,False,
        False,False,True,True,True,True,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,False,False,True,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '%': [
        False,False,False,False,False,False,False,False,
        False,False,True,False,False,False,True,False,
        False,True,False,True,False,True,True,False,
        False,False,True,False,True,True,False,False,
        False,False,False,True,True,False,True,False,
        False,False,True,True,False,True,False,True,
        False,True,True,False,False,False,True,False,
        False,False,False,False,False,False,False,False,
      ],
      '.': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      ',': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,False,False,False,False,
      ],
      ':': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      ';': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,True,True,False,False,False,False,
      ],
      '(': [
        False,False,False,False,False,False,False,False,
        False,False,False,False,True,False,False,False,
        False,False,False,True,False,False,False,False,
        False,False,False,True,False,False,False,False,
        False,False,False,True,False,False,False,False,
        False,False,False,True,False,False,False,False,
        False,False,False,False,True,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      ')': [
        False,False,False,False,False,False,False,False,
        False,False,False,True,False,False,False,False,
        False,False,False,False,True,False,False,False,
        False,False,False,False,True,False,False,False,
        False,False,False,False,True,False,False,False,
        False,False,False,False,True,False,False,False,
        False,False,False,True,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '\'': [
        False,False,False,True,True,False,False,False,
        False,False,False,True,True,False,False,False,
        False,False,False,False,True,False,False,False,
        False,False,False,True,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ],
      '\"': [
        False,False,True,True,False,True,True,False,
        False,False,True,True,False,True,True,False,
        False,False,False,True,False,False,True,False,
        False,False,True,False,False,True,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
        False,False,False,False,False,False,False,False,
      ]
    }