from matplotlib.path import Path
import numpy as np
import math

class Polygon:
  def __init__(self, vertices, color=(255, 255, 255)):
    if len(vertices) < 3:
      raise ValueError("A polygon must have at least 3 vertices")
    
    self.vertices = vertices
    self.path = Path(vertices)
    self.color = color

  def contains_points(self, points):
    return self.path.contains_points(points)
  
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
    
    self.vertices = rotated_vertices
    return self


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