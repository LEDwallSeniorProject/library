from matplotlib.path import Path
import numpy as np
import math

class Polygon:
  def __init__(self, vertices, color=(255, 255, 255)):
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
    """
    Check if the shape contains the given points.

    Parameters:
    - points (array-like): An array-like object containing the points to check.

    Returns:
    - bool: True if the shape contains all the points, False otherwise.
    """
    return self.path.contains_points(points)

  def translate(self, dx, dy):
    """
    Translate the shape by a specified distance along the x and y axes.

    Parameters:
    - vertices: List of tuples representing the vertices of the shape.
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
  
  def rotate(self, angle_degrees, center=(0, 0)):
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

  def change_vertices(self, vertices):
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


def get_polygon_vertices(sides, radius=1, center=(0, 0)):
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
  def __init__(self, radius, center, color=(255, 255, 255)):
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
    self.center = center