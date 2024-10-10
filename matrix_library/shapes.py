from matplotlib.path import Path
import numpy as np
import math
from skimage.draw import polygon, disk
from skimage import img_as_ubyte
from PIL import Image, ImageDraw, ImageFont


class Polygon:
    def __init__(self, vertices: list, color: tuple = (255, 255, 255)):
        """
        Initializes a Polygon object with the given vertices and color.

        Parameters:
        - vertices (list): A list of vertices that define the polygon. Must have at least 3 vertices.
        - color (tuple, optional): The color of the polygon. Defaults to (255, 255, 255).

        Raises:
        - ValueError: If the number of vertices is less than 3.
        """
        if len(vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        self.vertices = np.array(vertices)
        self.color = color
        self.path = Path(self.vertices)
        self.center = self.calculate_center()

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """Check if the given points are inside the polygon."""
        return self.path.contains_points(points)

    def translate(self, dx: float, dy: float):
        """
        Translate the polygon by a specified distance along the x and y axes.

        Parameters:
        - dx (float): The distance to translate along the x-axis.
        - dy (float): The distance to translate along the y-axis.
        """
        self.vertices += np.array([dx, dy])
        self.update_path()
        self.center = (self.center[0] + dx, self.center[1] + dy)

    def rotate(self, angle_degrees: float, center: tuple = (0, 0)):
        """
        Rotate the polygon by a specified angle around a given center.

        Parameters:
        - angle_degrees (float): The angle by which to rotate the polygon (in degrees).
        - center (tuple, optional): The center of rotation (default is (0, 0)).
        """
        angle_radians = np.radians(angle_degrees)
        cos_angle = np.cos(angle_radians)
        sin_angle = np.sin(angle_radians)

        # Rotate each vertex
        rotated_vertices = []
        for (x, y) in self.vertices:
            # Translate point to origin
            x_translated = x - center[0]
            y_translated = y - center[1]

            # Apply rotation
            x_rotated = x_translated * cos_angle - y_translated * sin_angle
            y_rotated = x_translated * sin_angle + y_translated * cos_angle

            # Translate point back
            rotated_vertices.append((x_rotated + center[0], y_rotated + center[1]))

        self.vertices = np.array(rotated_vertices)
        self.update_path()

    def update_path(self):
        """Update the path of the polygon based on its current vertices."""
        self.path = Path(self.vertices)

    def calculate_center(self):
        """Calculate the centroid of the polygon."""
        n = len(self.vertices)
        if n < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        cx, cy = 0.0, 0.0
        area = 0.0

        # Calculate the signed area and centroid
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

    def get_polygon_mask(self, shape: tuple):
        """
        Create a binary mask for the polygon on a given image shape.

        Parameters:
        - shape (tuple): The shape of the image (height, width).

        Returns:
        - mask (numpy.ndarray): A binary mask with the polygon filled in.
        """
        rr, cc = polygon(self.vertices[:, 1], self.vertices[:, 0], shape=shape)
        mask = np.zeros(shape, dtype=bool)
        mask[rr, cc] = True
        return mask

# Example usage
if __name__ == "__main__":
    vertices = np.array([[100, 100], [150, 50], [200, 100], [150, 150]])
    polygon = Polygon(vertices)

    # Create a binary mask for a 500x500 image
    mask = polygon.get_polygon_mask((500, 500))

    # Visualize the mask
    import matplotlib.pyplot as plt

    plt.imshow(mask, cmap='gray')
    plt.title("Polygon Mask")
    plt.axis('off')
    plt.show()

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

class Circle:
    def __init__(self, radius: float, center: tuple, color: tuple = (255, 255, 255)):
        """
        Initializes a Circle object with the given center, radius, and color.

        Parameters:
        - center (tuple): The (x, y) coordinates of the circle's center.
        - radius (float): The radius of the circle.
        - color (tuple, optional): The color of the circle. Defaults to (255, 255, 255).
        """
        if radius <= 0:
            raise ValueError("Radius must be greater than zero.")

        self.center = np.array(center)
        self.radius = radius
        self.color = color
        self.path = self.create_path()

    def create_path(self):
        """Create a path representation of the circle."""
        circle_points = self.get_circle_points()
        return Path(circle_points)

    def get_circle_points(self):
        """Get points on the circle's perimeter."""
        theta = np.linspace(0, 2 * np.pi, num=100)
        x = self.center[0] + self.radius * np.cos(theta)
        y = self.center[1] + self.radius * np.sin(theta)
        return np.column_stack((x, y))

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """Check if the given points are inside the circle."""
        distances = np.linalg.norm(points - self.center, axis=1)
        return distances <= self.radius

    def translate(self, dx: float, dy: float):
        """
        Translate the circle by a specified distance along the x and y axes.

        Parameters:
        - dx (float): The distance to translate along the x-axis.
        - dy (float): The distance to translate along the y-axis.
        """
        self.center += np.array([dx, dy])
        self.path = self.create_path()

    def rotate(self, angle_degrees: float, center: tuple = (0, 0)):
        """
        Rotate the circle by a specified angle around a given center.

        Parameters:
        - angle_degrees (float): The angle by which to rotate the circle (in degrees).
        - center (tuple, optional): The center of rotation (default is (0, 0)).
        """
        # Rotating a circle around its center does not change its shape
        # This method is included for consistency with the Polygon class
        pass

    def get_circle_mask(self, shape: tuple):
        """
        Create a binary mask for the circle on a given image shape.

        Parameters:
        - shape (tuple): The shape of the image (height, width).

        Returns:
        - mask (numpy.ndarray): A binary mask with the circle filled in.
        """
        rr, cc = disk(self.center.astype(int), self.radius, shape=shape)
        mask = np.zeros(shape, dtype=bool)
        mask[rr, cc] = True
        return mask

class Line:
    def __init__(self, start, end, color=(255, 255, 255), width=1):
        """
        Initializes a Line object with the given start and end points, color, and width.
        """
        self.start = np.array(start, dtype=float)
        self.end = np.array(end, dtype=float)
        self.color = color
        self.width = width
        self.image = self.create_line_image()

    def create_line_image(self):
        """
        Create an image of the line segment.
        """
        # Calculate the bounding box size for the line
        x_min = min(self.start[0], self.end[0])
        y_min = min(self.start[1], self.end[1])
        x_max = max(self.start[0], self.end[0])
        y_max = max(self.start[1], self.end[1])

        # Ensure the image size accounts for the line width
        width = int(x_max - x_min + self.width)
        height = int(y_max - y_min + self.width)

        # Create an RGBA image with a transparent background
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Adjust coordinates relative to the image size
        relative_start = (self.start[0] - x_min, self.start[1] - y_min)
        relative_end = (self.end[0] - x_min, self.end[1] - y_min)

        # Draw the line on the image
        draw.line([relative_start, relative_end], fill=self.color + (255,), width=self.width)

        return img

    def rotate(self, angle_degrees, center=(0, 0)):
        """
        Rotate the line segment by a specified angle around a given center.
        """
        # Convert angle to radians
        angle_radians = np.radians(angle_degrees)

        # Rotation matrix
        rotation_matrix = np.array([
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians), np.cos(angle_radians)]
        ])

        # Translate points to origin (relative to the center), rotate, and translate back
        translated_start = self.start - center
        translated_end = self.end - center

        rotated_start = np.dot(rotation_matrix, translated_start) + center
        rotated_end = np.dot(rotation_matrix, translated_end) + center

        # Update the line's start and end points
        self.start = rotated_start
        self.end = rotated_end

        # Recreate the image with the rotated line
        self.image = self.create_line_image()

    def translate(self, dx, dy):
        """
        Translate the line segment by a given distance along the x and y axes.
        """
        self.start += np.array([dx, dy])
        self.end += np.array([dx, dy])
        self.image = self.create_line_image()

    def contains_points(self, points):
        """
        Check if the given points are on the line segment.
        """
        mask = np.zeros(len(points), dtype=bool)
        for i, point in enumerate(points):
            point = np.array(point)

            # Check if the point lies between the start and end of the line segment
            d_start = np.linalg.norm(point - self.start)
            d_end = np.linalg.norm(point - self.end)
            d_total = np.linalg.norm(self.start - self.end)

            # The point lies on the line if the sum of distances from start and end is equal to the total length
            if np.isclose(d_start + d_end, d_total, atol=self.width / 2):
                mask[i] = True

        return mask

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
    self.center = (64,64)
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
    def __init__(self, text: str, position: list=[0, 0], color: list=[255, 255, 255], size: int=1, auto_newline: bool=False):
        self.text: str = text
        self.position: list = list(position)
        self.color = color
        self.auto_newline = auto_newline
        self.size: int = size
        self.letters = self.get_letters()
    
    def set_text(self, text: str):
        """Only update letters for characters that have changed."""
        if text != self.text:
            self.update_letters(text)
        self.text = text
    
    def set_position(self, position: list):
        """Only update letters if the position has changed."""
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
        """Update only the letters that have changed, reusing existing ones where possible."""
        x, y = self.position
        new_letters = []
        for i, char in enumerate(new_text):
            if self.auto_newline and x >= 128 - (8 * self.size):
                x = self.position[0]
                y += 8 * self.size
            if i < len(self.letters):
                # Reuse the existing letter and update its character if needed
                self.letters[i].set_char(char)
                new_letters.append(self.letters[i])
            else:
                # Create a new letter if this is beyond the current letters list
                new_letters.append(Letter(char, [x, y], self.color, size=self.size))
            x += 8 * self.size
        
        # If the new text is shorter, trim the extra letters
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
    def __init__(self, pixels: list, width: int, height: int, position: list = [0, 0], color: list = (255, 255, 255), scale: int = 1):
        self.pixels = pixels
        self.position = position
        self.width = width
        self.height = height
        self.scale = scale
        self.color = color
        
        # Cache for contains_points
        self.cached_points = None
        self.cached_mask = None
    
    def contains_points(self, points: np.ndarray):
        # If cached_points is None or different, recalculate
        if not np.array_equal(self.cached_points, points):
            self.cached_points = points
            self.cached_mask = self._compute_contains_points(points)
        return self.cached_mask
    
    def _compute_contains_points(self, points: np.ndarray):
        """Computes the point containment without caching."""
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
        """Translate the position of the bitmap and invalidate cache."""
        self.position[0] += dx
        self.position[1] += dy
        self._invalidate_cache()

    def set_bitmap(self, pixels: list, width: int, height: int):
        """Update the bitmap with new pixel data, width, and height. Invalidate the cache."""
        self.pixels = pixels
        self.width = width
        self.height = height
        self._invalidate_cache()

    def set_position(self, position: list):
        """Set a new position for the bitmap and invalidate cache if position changes."""
        if position != self.position:
            self.position = position
            self._invalidate_cache()

    def _invalidate_cache(self):
        """Invalidates the cached result of contains_points."""
        self.cached_points = None
        self.cached_mask = None
  
class Letter(BitMap):
  def __init__(self, char: str, position: list=[0, 0], color:list=[255, 255, 255], size: int=1):
        self.char = char
        self.position = position
        self.color = color
        self.size = size
        
        # Initialize the character mask and the bitmap
        self.mask_lookup = self.init_char_mask_lookup()
        char_mask = self.get_char_mask()
        super().__init__(char_mask, 8, 8, position, color, size)
        

  def set_char(self, new_char: str):
        """Update the character and invalidate the cache."""
        if new_char != self.char:
            self.char = new_char
            self._invalidate_cache()
            # Update the bitmap for the new character
            char_mask = self.get_char_mask()
            self.set_bitmap(char_mask, 8, 8)
  
  def set_position(self, new_position: list):
        """Update the position and invalidate the cache."""
        if new_position != self.position:
            self.position = new_position
  
  def set_color(self, new_color: list):
        """Update the color and invalidate the cache."""
        if new_color != self.color:
            self.color = new_color
  
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