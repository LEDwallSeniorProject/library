from matrix_library import utils
import numpy as np
import math
import os

# load pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Init some variables to reduce overhead
empty_canvas = np.zeros((128 * 128), dtype=bool)


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
        self.center = self.calculate_center()
        
        # Precompute bounding box for faster contains_points
        self._update_bounds()

    def _update_bounds(self):
        """Update bounding box for faster point containment checks"""
        self.x_min = np.min(self.vertices[:, 0])
        self.x_max = np.max(self.vertices[:, 0])
        self.y_min = np.min(self.vertices[:, 1])
        self.y_max = np.max(self.vertices[:, 1])

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """
        Check if the given points are inside the polygon using NumPy.

        Parameters:
        - points (np.ndarray): An array of shape (N, 2) with (x, y) coordinates.

        Returns:
        - mask (np.ndarray): Boolean array where True means the point is inside the polygon.
        """
        # Quick bounding box test to eliminate obvious non-containment
        valid_mask = (
            (points[:, 0] >= self.x_min) &
            (points[:, 0] <= self.x_max) &
            (points[:, 1] >= self.y_min) &
            (points[:, 1] <= self.y_max)
        )
        
        if not np.any(valid_mask):
            return np.zeros(points.shape[0], dtype=bool)
        
        # Only process points inside the bounding box
        filtered_points = points[valid_mask]
        
        # Ray casting algorithm vectorized
        mask = np.zeros(filtered_points.shape[0], dtype=bool)
        
        x_points = filtered_points[:, 0]
        y_points = filtered_points[:, 1]
        x_poly = self.vertices[:, 0]
        y_poly = self.vertices[:, 1]
        n = len(self.vertices)
        
        # Vectorized ray-casting algorithm
        for i in range(n):
            j = (i - 1) % n
            xi, yi = x_poly[i], y_poly[i]
            xj, yj = x_poly[j], y_poly[j]
            
            # Avoid division by zero
            valid_edge = yi != yj
            if not valid_edge:
                continue
                
            # Check if the horizontal ray from the point intersects with this edge
            intersect = ((yi > y_points) != (yj > y_points)) & (
                x_points < (xj - xi) * (y_points - yi) / (yj - yi + 1e-12) + xi
            )
            
            # Toggle the inside status
            mask ^= intersect
        
        # Map results back to original points array
        result = np.zeros(points.shape[0], dtype=bool)
        result[valid_mask] = mask
        return result

    def translate(self, dx: float, dy: float) -> None:
        """
        Translate the polygon by a specified distance along the x and y axes.

        Parameters:
        - dx (float): The distance to translate along the x-axis.
        - dy (float): The distance to translate along the y-axis.
        """
        self.vertices += np.array([dx, dy])
        self.center = (self.center[0] + dx, self.center[1] + dy)
        self._update_bounds()

    def rotate(self, angle_degrees: float, center: tuple = None) -> None:
        """
        Rotate the polygon by a specified angle around a given center.

        Parameters:
        - angle_degrees (float): The angle by which to rotate the polygon (in degrees).
        - center (tuple, optional): The center of rotation (default is the polygon center).
        """
        if center is None:
            center = self.center
            
        angle_radians = np.radians(angle_degrees)
        cos_angle = np.cos(angle_radians)
        sin_angle = np.sin(angle_radians)
        
        # Vectorized rotation
        translated = self.vertices - np.array(center)
        rotation_matrix = np.array([
            [cos_angle, -sin_angle],
            [sin_angle, cos_angle]
        ])
        rotated = np.dot(translated, rotation_matrix.T)
        self.vertices = rotated + np.array(center)
        
        self._update_bounds()

    def calculate_center(self) -> tuple:
        """Calculate the centroid of the polygon."""
        n = len(self.vertices)
        if n < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        # Simple centroid calculation for faster performance
        cx = np.mean(self.vertices[:, 0])
        cy = np.mean(self.vertices[:, 1])
        
        return (cx, cy)

    def get_polygon_mask(self, shape: tuple) -> np.ndarray:
        """
        Create a binary mask for the polygon on a given image shape using only NumPy.

        Parameters:
        - shape (tuple): The shape of the image (height, width).

        Returns:
        - mask (numpy.ndarray): A binary mask with the polygon filled in.
        """
        height, width = shape
        mask = np.zeros((height, width), dtype=bool)

        # Limit computation to the polygon's bounding box
        min_x = max(0, int(np.floor(self.x_min)))
        max_x = min(width - 1, int(np.ceil(self.x_max)))
        min_y = max(0, int(np.floor(self.y_min)))
        max_y = min(height - 1, int(np.ceil(self.y_max)))
        
        # Skip if polygon is outside the image
        if min_x >= width or max_x < 0 or min_y >= height or max_y < 0:
            return mask

        # Generate coordinates within the bounding box
        y_coords, x_coords = np.meshgrid(
            np.arange(min_y, max_y + 1), 
            np.arange(min_x, max_x + 1), 
            indexing='ij'
        )
        
        # Reshape for point containment
        points = np.column_stack((x_coords.ravel(), y_coords.ravel()))
        
        # Get containment mask and reshape to bounding box
        inside = self.contains_points(points)
        box_mask = inside.reshape((max_y - min_y + 1, max_x - min_x + 1))
        
        # Update the main mask
        mask[min_y:max_y+1, min_x:max_x+1] = box_mask
        
        return mask

    def get_center(self) -> tuple:
        """Get the polygon center as a tuple."""
        return self.center


def get_polygon_vertices(sides: int, radius: float = 1, center: tuple = (0, 0)) -> list:
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

    # Vectorized vertex calculation
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    
    return list(zip(x, y))


class Circle:
    def __init__(self, radius: float, center: tuple, color: tuple = (255, 255, 255)) -> None:
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
        
        # Precompute for faster contains_points
        self.radius_squared = radius * radius

    def get_circle_points(self) -> np.ndarray:
        """Get points on the circle's perimeter."""
        theta = np.linspace(0, 2 * np.pi, num=100)
        x = self.center[0] + self.radius * np.cos(theta)
        y = self.center[1] + self.radius * np.sin(theta)
        return np.column_stack((x, y))

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """Check if the given points are inside the circle."""
        # Quick bounds check
        x_min, y_min = self.center - self.radius
        x_max, y_max = self.center + self.radius
        
        valid_mask = (
            (points[:, 0] >= x_min) &
            (points[:, 0] <= x_max) &
            (points[:, 1] >= y_min) &
            (points[:, 1] <= y_max)
        )
        
        if not np.any(valid_mask):
            return np.zeros(points.shape[0], dtype=bool)
        
        # Vectorized distance calculation - only for points in bounding box
        filtered_points = points[valid_mask]
        
        # Faster squared distance calculation without square root
        dx = filtered_points[:, 0] - self.center[0]
        dy = filtered_points[:, 1] - self.center[1]
        distances_squared = dx*dx + dy*dy
        
        inside_mask = distances_squared <= self.radius_squared
        
        # Map results back to original points array
        result = np.zeros(points.shape[0], dtype=bool)
        result[valid_mask] = inside_mask
        return result

    def translate(self, dx: float, dy: float) -> None:
        """
        Translate the circle by a specified distance along the x and y axes.

        Parameters:
        - dx (float): The distance to translate along the x-axis.
        - dy (float): The distance to translate along the y-axis.
        """
        self.center += np.array([int(dx), int(dy)])

    def rotate(self, angle_degrees: float, center: tuple = (0, 0)) -> None:
        """
        Rotate the circle by a specified angle around a given center.

        Parameters:
        - angle_degrees (float): The angle by which to rotate the circle (in degrees).
        - center (tuple, optional): The center of rotation (default is (0, 0)).
        """
        # For consistency with Polygon class, but rotation doesn't change a circle
        pass

    def get_circle_mask(self, shape: tuple) -> np.ndarray:
        """
        Create a binary mask for the circle on a given image shape using only NumPy.

        Parameters:
        - shape (tuple): The shape of the image (height, width).

        Returns:
        - mask (numpy.ndarray): A binary mask with the circle filled in.
        """
        height, width = shape
        mask = np.zeros((height, width), dtype=bool)

        # Define bounding box to limit the area of computation
        min_x = max(0, int(np.floor(self.center[0] - self.radius)))
        max_x = min(width - 1, int(np.ceil(self.center[0] + self.radius)))
        min_y = max(0, int(np.floor(self.center[1] - self.radius)))
        max_y = min(height - 1, int(np.ceil(self.center[1] + self.radius)))
        
        # Skip if circle is outside the image
        if min_x >= width or max_x < 0 or min_y >= height or max_y < 0:
            return mask

        # Create coordinate grid
        y, x = np.ogrid[min_y:max_y + 1, min_x:max_x + 1]
        
        # Faster squared distance calculation
        dist_sq = (x - self.center[0]) ** 2 + (y - self.center[1]) ** 2

        # Fill mask where distance is within the circle
        mask[min_y:max_y + 1, min_x:max_x + 1] = dist_sq <= self.radius_squared
        
        return mask


class Line(Polygon):
    def __init__(self, start: list, end: list, color: list = (255, 255, 255), thickness: float = 0.5) -> None:
        if start == end:
            raise ValueError("The start and end points of a line cannot be the same.")
        elif thickness <= 0:
            raise ValueError("The thickness of a line must be greater than 0.")
        elif len(start) != 2 or len(end) != 2:
            raise ValueError("The start and end points must be list of length 2.")
        elif len(color) != 3:
            raise ValueError("The color must be a list of length 3.")

        self.start = np.array(start)
        self.end = np.array(end)
        self.thickness = thickness
        
        # Calculate length and angle more efficiently
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        self.length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        
        # Calculate the angle of the line
        self.angle = self.calculate_angle()
        temp_end = [self.start[0], self.start[1] + self.length]

        verts1 = [self.start[0] + self.thickness, self.start[1] + self.thickness]
        verts2 = [self.start[0] + self.thickness, self.start[1] - self.thickness]
        verts3 = [self.start[0] - self.thickness, self.start[1] - self.thickness]
        verts4 = [self.start[0] - self.thickness, self.start[1] + self.thickness]
        verts5 = [temp_end[0] - self.thickness, temp_end[1] - self.thickness]
        verts6 = [temp_end[0] - self.thickness, temp_end[1] + self.thickness]
        verts7 = [temp_end[0] + self.thickness, temp_end[1] + self.thickness]
        verts8 = [temp_end[0] + self.thickness, temp_end[1] - self.thickness]
        self.vertices = [verts1, verts2, verts3, verts4, verts5, verts6, verts7, verts8]
        
        # Create polygon and then rotate
        super().__init__(self.vertices, color)
        self.rotate(-self.angle, self.start)

    def calculate_angle(self):
        """Calculate angle between line and positive y-axis"""
        line1 = (self.end[0] - self.start[0], self.end[1] - self.start[1])
        line2 = (0, 1)

        dot_product = line1[0] * line2[0] + line1[1] * line2[1]
        magnitude_line1 = math.sqrt(line1[0] ** 2 + line1[1] ** 2)
        magnitude_line2 = math.sqrt(line2[0] ** 2 + line2[1] ** 2)

        cos_angle = dot_product / (magnitude_line1 * magnitude_line2)
        angle_rads = math.acos(min(max(cos_angle, -1.0), 1.0))  # Clamp to avoid numerical issues
        angle_deg = math.degrees(angle_rads)

        return angle_deg


class PolygonOutline(Polygon):
    def __init__(self, vertices: tuple, color: tuple = (255, 255, 255), thickness: float = 1) -> None:
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
        
        # Calculate center first using the vertices
        sum_x = sum(v[0] for v in vertices)
        sum_y = sum(v[1] for v in vertices)
        self.center = (sum_x / len(vertices), sum_y / len(vertices))
        
        # Now that self.center exists, calculate inner vertices
        inner_radius = max(self.distance(
            self.center[0], self.center[1], self.vertices[0][0], self.vertices[0][1]
        ) - thickness, 0.1)
        
        self.inner_vertices = get_polygon_vertices(
            len(self.vertices), inner_radius, self.center
        )
        
        # Initialize as polygon for inheritance
        super().__init__(vertices, color)

    def change_inner_vertices(self, inner_vertices) -> None:
        self.inner_vertices = inner_vertices

    def rotate_inner(self, angle_degrees: float, center: tuple = (0, 0)) -> None:
        # Convert angle from degrees to radians
        angle_radians = math.radians(angle_degrees)
        cos_angle = math.cos(angle_radians)
        sin_angle = math.sin(angle_radians)

        rotated_vertices = []

        for x, y in self.inner_vertices:
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

    def rotate(self, angle_degrees: float, center: tuple = (0, 0)) -> None:
        super().rotate(angle_degrees, center)
        self.rotate_inner(angle_degrees, center)

    def distance(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def contains_points(self, points: np.ndarray) -> np.ndarray:
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
        # Create many-sided polygon to approximate circle
        num_points = max(int(radius * 4), 24)  # Increase for smoother circles
        vertices = get_polygon_vertices(num_points, radius, center)
        super().__init__(vertices, color, thickness)
        self.radius = radius
        self.center = center
        
        # Precompute squared radii for faster contains_points
        self.outer_radius_squared = radius * radius
        self.inner_radius = max(radius - thickness, 0.1)  # Prevent negative radius
        self.inner_radius_squared = self.inner_radius * self.inner_radius

    def contains_points(self, points: np.ndarray):
        # More efficient implementation using distance calculation
        # instead of constructing temporary circles
        distances = np.sqrt(np.sum((points - self.center) ** 2, axis=1))
        
        # Points must be within outer radius but outside inner radius
        return (distances <= self.radius) & (distances > self.inner_radius)


class Phrase:
    def __init__(self, text: str, position: list = [0, 0], color: list = [255, 255, 255], size: int = 1, auto_newline: bool = False):
        self.text: str = text
        self.position: list = list(position)
        self.color = color
        self.auto_newline = auto_newline
        self.size: int = size
        self.letters = self.get_letters()
        
        # Precompute bounds for faster checks
        self._update_bounds()
        
    def _update_bounds(self):
        """Calculate phrase bounds for faster containment checks"""
        if not self.letters:
            self.x_min = self.position[0]
            self.y_min = self.position[1]
            self.x_max = self.position[0] + len(self.text) * 8 * self.size
            self.y_max = self.position[1] + 8 * self.size
            return
            
        self.x_min = min(letter.position[0] for letter in self.letters)
        self.y_min = min(letter.position[1] for letter in self.letters)
        self.x_max = max(letter.position[0] + 8 * letter.size for letter in self.letters)
        self.y_max = max(letter.position[1] + 8 * letter.size for letter in self.letters)

    def set_text(self, text: str):
        """Only update letters for characters that have changed."""
        if text != self.text:
            self.update_letters(text)
            self.text = text
            self._update_bounds()

    def set_position(self, position: list):
        """Only update letters if the position has changed."""
        if position != self.position:
            dx = position[0] - self.position[0]
            dy = position[1] - self.position[1]
            self.position = position
            self.translate(dx, dy)

    def get_width(self):
        return sum([letter.get_width() for letter in self.letters])

    def translate(self, dx: float, dy: float):
        for letter in self.letters:
            letter.translate(dx, dy)
        self.position[0] += dx
        self.position[1] += dy
        
        # Update bounds
        self.x_min += dx
        self.x_max += dx
        self.y_min += dy
        self.y_max += dy

    def get_letters(self):
        """Initial creation of the letters based on the text and position."""
        letters = []
        x, y = self.position
        for char in self.text:
            if self.auto_newline and x > 128 - (8 * self.size):
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
                letter = self.letters[i]
                if letter.char != char:
                    letter.set_char(char)
                letter.set_position([x, y])
                new_letters.append(letter)
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
        """Optimized containment check with bounding box"""
        # Quick bounds check
        valid_mask = (
            (points[:, 0] >= self.x_min) &
            (points[:, 0] <= self.x_max) &
            (points[:, 1] >= self.y_min) &
            (points[:, 1] <= self.y_max)
        )
        
        if not np.any(valid_mask):
            return np.zeros(len(points), dtype=bool)
            
        # Initialize result array
        result = np.zeros(len(points), dtype=bool)
        
        # Check each letter (only for points within phrase bounds)
        filtered_points = points[valid_mask]
        filtered_result = np.zeros(len(filtered_points), dtype=bool)
        
        for letter in self.letters:
            letter_result = letter.contains_points(filtered_points)
            filtered_result = np.logical_or(filtered_result, letter_result)
            
        # Map back to full points array
        result[valid_mask] = filtered_result
        return result


class Pixel:
    def __init__(self, position: list, color: list = [255, 255, 255], scale: int = 1):
        self.position = position
        self.color = color
        self.scale = scale
        
        # Precompute bounds
        self.x_min = position[0]
        self.y_min = position[1]
        self.x_max = position[0] + scale
        self.y_max = position[1] + scale

    def contains_points(self, points: np.ndarray):
        # Quick bounds check
        valid_mask = (
            (points[:, 0] >= self.x_min) &
            (points[:, 0] < self.x_max) &
            (points[:, 1] >= self.y_min) &
            (points[:, 1] < self.y_max)
        )
        
        return valid_mask

    def translate(self, dx: float, dy: float):
        self.position[0] += dx
        self.position[1] += dy
        
        # Update bounds
        self.x_min += dx
        self.x_max += dx
        self.y_min += dy
        self.y_max += dy

    def __str__(self):
        return f"[{self.position[0]},{self.position[1]}] -> ({self.color[0]},{self.color[1]},{self.color[2]})"


class ColoredBitMap:
    def __init__(self, pixels: list, width: int, height: int, position: list = [0, 0], scale: int = 1):
        self.position = position
        self.width = width
        self.height = height
        self.scale = scale
        self.pixels = []

        for i in range(len(pixels)):
            if pixels[i] != [] and pixels[i] != [None]:  # Skip empty pixels
                x = (i % width) * scale + position[0]
                y = (i // width) * scale + position[1]
                self.pixels.append(Pixel([x, y], pixels[i], scale))
                
        # Precompute bounds
        self._update_bounds()
        
    def _update_bounds(self):
        """Calculate bitmap bounds for faster containment checks"""
        if not self.pixels:
            self.x_min = self.position[0]
            self.y_min = self.position[1]
            self.x_max = self.position[0] + self.width * self.scale
            self.y_max = self.position[1] + self.height * self.scale
            return
            
        self.x_min = min(pixel.x_min for pixel in self.pixels)
        self.y_min = min(pixel.y_min for pixel in self.pixels)
        self.x_max = max(pixel.x_max for pixel in self.pixels)
        self.y_max = max(pixel.y_max for pixel in self.pixels)
        
    def contains_points(self, points: np.ndarray):
        """Optimized containment check with bounding box"""
        # Quick bounds check
        valid_mask = (
            (points[:, 0] >= self.x_min) &
            (points[:, 0] <= self.x_max) &
            (points[:, 1] >= self.y_min) &
            (points[:, 1] <= self.y_max)
        )
        
        if not np.any(valid_mask):
            return np.zeros(len(points), dtype=bool)
            
        # Check each pixel (only for points within bitmap bounds)
        result = np.zeros(len(points), dtype=bool)
        
        for pixel in self.pixels:
            pixel_result = pixel.contains_points(points)
            result = np.logical_or(result, pixel_result)
            
        return result
        
    def translate(self, dx: float, dy: float):
        """Move all pixels and update bounds"""
        for pixel in self.pixels:
            pixel.translate(dx, dy)
            
        self.position[0] += dx
        self.position[1] += dy
        
        # Update bounds
        if hasattr(self, 'x_min'):
            self.x_min += dx
            self.x_max += dx
            self.y_min += dy
            self.y_max += dy


# Global character cache for Letter class
char_mask_cache = {}

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
        self.cached_points_x = None
        self.cached_points_y = None
        
        # Precompute important values
        self._update_bounds()
        self._precompute_active_pixels()

    def _update_bounds(self):
        """Update bounds for faster containment checks"""
        self.x_min = self.position[0]
        self.y_min = self.position[1]
        self.x_max = self.x_min + self.width * self.scale
        self.y_max = self.y_min + self.height * self.scale

    def _precompute_active_pixels(self):
        """Precompute active pixel coordinates for faster containment checks"""
        # Find indices of active pixels
        active_indices = np.where(np.array(self.pixels) == 1)[0]
        
        # Calculate corresponding x, y coordinates in bitmap space
        self.active_x = (active_indices % self.width) 
        self.active_y = (active_indices // self.width)
        
        # Save active indices for faster lookups
        self.active_indices = active_indices

    def _get_valid_points_mask(self, points, x_min, y_min, x_max, y_max):
        """Helper to check if points are within a bounding box"""
        return (
            (points[:, 0] >= x_min) &
            (points[:, 0] < x_max) &
            (points[:, 1] >= y_min) &
            (points[:, 1] < y_max)
        )

    def contains_points(self, points: np.ndarray):
        """Check if points are contained within any active pixels of the bitmap"""
        # Quick bounding box check
        if (self.x_min > 128 or self.y_min > 128 or
            self.x_max < 0 or self.y_max < 0):
            return np.zeros(points.shape[0], dtype=bool)
        
        # Check overall bounding box
        valid_points_mask = self._get_valid_points_mask(
            points, self.x_min, self.y_min, self.x_max, self.y_max
        )
        
        if not np.any(valid_points_mask):
            return np.zeros(points.shape[0], dtype=bool)
        
        # Only process potentially valid points
        valid_points = points[valid_points_mask]
        
        # Calculate relative positions in bitmap
        rel_x = ((valid_points[:, 0] - self.position[0]) / self.scale).astype(int)
        rel_y = ((valid_points[:, 1] - self.position[1]) / self.scale).astype(int)
        
        # Ensure coordinates are in bounds
        in_bounds = (
            (rel_x >= 0) & (rel_x < self.width) &
            (rel_y >= 0) & (rel_y < self.height)
        )
        
        if not np.any(in_bounds):
            return np.zeros(points.shape[0], dtype=bool)
            
        # Calculate indices in bitmap
        rel_x_in = rel_x[in_bounds]
        rel_y_in = rel_y[in_bounds]
        point_indices = rel_y_in * self.width + rel_x_in
        
        # Check which points are in active pixels using numpy's isin function
        mask_in_bounds = np.isin(point_indices, self.active_indices)
        
        # Map back to valid points
        result_valid = np.zeros(valid_points.shape[0], dtype=bool)
        result_valid[in_bounds] = mask_in_bounds
        
        # Map back to all points
        result = np.zeros(points.shape[0], dtype=bool)
        result[valid_points_mask] = result_valid
        
        return result

    def translate(self, dx: float, dy: float):
        """Translate the bitmap by dx, dy and update cached values"""
        self.position[0] += dx
        self.position[1] += dy
        
        # Update bounds
        self.x_min += dx
        self.x_max += dx
        self.y_min += dy
        self.y_max += dy

    def set_bitmap(self, pixels: list, width: int, height: int):
        """Update the bitmap with new pixel data"""
        self.pixels = pixels
        self.width = width
        self.height = height
        
        # Update cached values
        self._update_bounds()
        self._precompute_active_pixels()

    def set_position(self, position: list):
        """Set a new position and update cached values"""
        if position == self.position:
            return
            
        # Calculate delta for translation
        dx = position[0] - self.position[0]
        dy = position[1] - self.position[1]
        
        self.position = position
        
        # Update bounds
        self.x_min += dx
        self.x_max += dx
        self.y_min += dy
        self.y_max += dy

    def _bbox_intersects(self, bbox1, bbox2):
        """Check if two bounding boxes intersect"""
        x1_min, y1_min, x1_max, y1_max = bbox1
        x2_min, y2_min, x2_max, y2_max = bbox2

        return not (
            x1_max <= x2_min or x1_min >= x2_max or 
            y1_max <= y2_min or y1_min >= y2_max
        )


class Image(ColoredBitMap):
    def __init__(self, width: int, height: int, position: list = [0, 0], scale: int = 1):
        super().__init__(pixels=[], width=width, height=height, position=position, scale=scale)

    def loadfile(self, filename: str):
        """Load image from file and convert to pixels"""
        if os.path.exists(filename):
            imgsurface = pygame.image.load(filename)

            # check to make sure size matches
            if(imgsurface.get_height() != self.height or imgsurface.get_width() != self.width):
                imgsurface = pygame.transform.scale(imgsurface,(self.width,self.height))
            
            # Clear existing pixels
            self.pixels = []
            
            # Loop through and make a bitmap of pixels
            for x in range(0,self.width):
                for y in range(0,self.height):
                    pos_x = x * self.scale + self.position[0]
                    pos_y = y * self.scale + self.position[1]
                    color = tuple(imgsurface.get_at((x,y))[0:3])
                    self.pixels.append(Pixel([pos_x, pos_y], color=color, scale=self.scale))
                    
            # Update bounds
            self._update_bounds()
        else:
            print(f"File {filename} does not exist. Try again.")
    
    def loadpixels(self, pixels: list):
        # Clear existing pixels
        self.pixels = []
        
        # Create new pixels
        for i, color in enumerate(pixels):
            if color and color != [None]:  # Skip empty pixels
                x = (i % self.width) * self.scale + self.position[0]
                y = (i // self.width) * self.scale + self.position[1]
                self.pixels.append(Pixel([x, y], color=color, scale=self.scale))
                
        # Update bounds
        self._update_bounds()


class Letter(BitMap):
    def __init__(self, char: str, position: list = [0, 0], color: list = [255, 255, 255], size: int = 1):
        # Default mask (blank)
        self.char = ""
        self.mask = [False] * 64
        self.position = list(position)
        self.color = color
        self.size = size
        
        # Initialize bitmap with default mask
        super().__init__(self.mask, 8, 8, position, color, size)
        
        # Set the actual character
        self.set_char(char)

    def set_char(self, new_char: str):
        """Update character bitmap if changed"""
        if new_char == self.char:
            return
            
        self.char = new_char
        
        # Use cached mask if available
        if new_char in char_mask_cache:
            self.mask = char_mask_cache[new_char]
        else:
            # Get from utils or use default pattern
            if new_char in utils.char_mask:
                self.mask = utils.char_mask[new_char]
            else:
                # Checkered pattern for unknown characters
                self.mask = [((i + j) % 2 == 1) for i in range(8) for j in range(8)]
                
            # Cache for future use
            char_mask_cache[new_char] = self.mask
            
        # Update bitmap with new mask
        self.set_bitmap(self.mask, 8, 8)

    def contains_points(self, points: np.ndarray):
        """Optimized letter containment check"""
        # Use pre-computed bounds from parent class
        valid_mask = self._get_valid_points_mask(
            points, self.x_min, self.y_min, self.x_max, self.y_max
        )
        
        if not np.any(valid_mask):
            return np.zeros(points.shape[0], dtype=bool)
        
        # Only process points in bounds
        valid_points = points[valid_mask]
        
        # Calculate relative position in letter grid
        rel_x = ((valid_points[:, 0] - self.position[0]) / self.size).astype(int)
        rel_y = ((valid_points[:, 1] - self.position[1]) / self.size).astype(int)
        
        # Ensure coordinates are in bounds
        rel_x = np.clip(rel_x, 0, 7)
        rel_y = np.clip(rel_y, 0, 7)
        
        # Calculate indices in mask array
        indices = rel_y * 8 + rel_x
        
        # Check mask values
        mask_array = np.array(self.mask)
        mask_values = mask_array[indices]
        
        # Map results back to original points
        result = np.zeros(points.shape[0], dtype=bool)
        result[valid_mask] = mask_values
        
        return result

    def set_position(self, new_position: list):
        """Update position"""
        if new_position == self.position:
            return
            
        # Calculate delta and translate
        dx = new_position[0] - self.position[0]
        dy = new_position[1] - self.position[1]
        self.translate(dx, dy)

    def set_color(self, new_color: list):
        """Update color"""
        if new_color != self.color:
            self.color = new_color

    def get_width(self):
        """Get letter width"""
        return 8 * self.size