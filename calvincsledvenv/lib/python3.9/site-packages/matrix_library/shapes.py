from matplotlib.path import Path
from matrix_library import utils
import numpy as np
import math
from skimage.draw import polygon, disk
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
        self.path = Path(self.vertices)
        self.center = self.calculate_center()

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """Check if the given points are inside the polygon."""
        return self.path.contains_points(points)

    def translate(self, dx: float, dy: float) -> None:
        """
        Translate the polygon by a specified distance along the x and y axes.

        Parameters:
        - dx (float): The distance to translate along the x-axis.
        - dy (float): The distance to translate along the y-axis.
        """
        self.vertices += np.array([dx, dy])
        self.update_path()
        self.center = (self.center[0] + dx, self.center[1] + dy)

    def rotate(self, angle_degrees: float, center: tuple = (0, 0)) -> None:
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
        for x, y in self.vertices:
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

    def update_path(self) -> None:
        """Update the path of the polygon based on its current vertices."""
        self.path = Path(self.vertices)

    def calculate_center(self) -> tuple:
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

        cx /= 6 * area
        cy /= 6 * area

        return (cx, cy)

    def get_polygon_mask(self, shape: tuple) -> np.ndarray:
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

    def get_center(self) -> tuple:
        # Initialize sums for x and y coordinates
        sum_x = sum_y = 0

        # Loop through each vertex (assumed as a tuple (x, y))
        for x, y in self.vertices:
            sum_x += x
            sum_y += y

        # Calculate the averages of the x and y coordinates
        centroid_x = sum_x / len(self.vertices)
        centroid_y = sum_y / len(self.vertices)

        return (centroid_x, centroid_y)


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

    vertices = []
    angle_step = 2 * math.pi / sides

    for i in range(sides):
        angle = i * angle_step
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))

    return vertices


class Circle:
    def __init__(
        self, radius: float, center: tuple, color: tuple = (255, 255, 255)
    ) -> None:
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

    def create_path(self) -> Path:
        """Create a path representation of the circle."""
        circle_points = self.get_circle_points()
        return Path(circle_points)

    def get_circle_points(self) -> np.ndarray:
        """Get points on the circle's perimeter."""
        theta = np.linspace(0, 2 * np.pi, num=100)
        x = self.center[0] + self.radius * np.cos(theta)
        y = self.center[1] + self.radius * np.sin(theta)
        return np.column_stack((x, y))

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        """Check if the given points are inside the circle."""
        distances = np.linalg.norm(points - self.center, axis=1)
        return distances <= self.radius

    def translate(self, dx: float, dy: float) -> None:
        """
        Translate the circle by a specified distance along the x and y axes.

        Parameters:
        - dx (float): The distance to translate along the x-axis.
        - dy (float): The distance to translate along the y-axis.
        """
        self.center += np.array([int(dx), int(dy)])
        self.path = self.create_path()

    def rotate(self, angle_degrees: float, center: tuple = (0, 0)) -> None:
        """
        Rotate the circle by a specified angle around a given center.

        Parameters:
        - angle_degrees (float): The angle by which to rotate the circle (in degrees).
        - center (tuple, optional): The center of rotation (default is (0, 0)).
        """
        # Rotating a circle around its center does not change its shape
        # This method is included for consistency with the Polygon class
        pass

    def get_circle_mask(self, shape: tuple) -> np.ndarray:
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


class Line(Polygon):
    def __init__(
        self,
        start: list,
        end: list,
        color: list = (255, 255, 255),
        thickness: float = 0.5,
    ) -> None:
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
    def __init__(
        self, vertices: tuple, color: tuple = (255, 255, 255), thickness: float = 1
    ) -> None:
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
        self.inner_vertices = get_polygon_vertices(
            len(self.vertices),
            self.distance(
                self.center[0], self.center[1], self.vertices[0][0], self.vertices[0][1]
            )
            - self.thickness,
            self.center,
        )

    def change_inner_vertices(self, inner_vertices) -> None:
        self.inner_vertices = inner_vertices
        self.path = Path(self.inner_vertices)

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
        vertices = get_polygon_vertices(radius * 10, radius, center)
        super().__init__(vertices, color, thickness)
        self.radius = radius

    def contains_points(self, points: np.ndarray):
        mask = np.zeros(len(points), dtype=bool)

        circle1_mask = Circle(self.radius, self.center, self.color).contains_points(
            points
        )
        circle2_mask = Circle(
            self.radius - self.thickness, self.center, self.color
        ).contains_points(points)

        mask = np.logical_and(circle1_mask, np.logical_not(circle2_mask))
        return mask


class Phrase:
    def __init__(
        self,
        text: str,
        position: list = [0, 0],
        color: list = [255, 255, 255],
        size: int = 1,
        auto_newline: bool = False,
    ):
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
        for i, letter in enumerate(self.letters):
            mask |= letter.contains_points(points)
        return mask


class Pixel:
    def __init__(self, position: list, color: list = [255, 255, 255], scale: int = 1):
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
                    np.logical_and(points[:, 1] >= y + j, points[:, 1] < y + j + 1),
                )
        return mask

    def translate(self, dx: float, dy: float):
        self.position[0] += dx
        self.position[1] += dy

    def __str__(self):
        return f"[{self.position[0]},{self.position[1]}] -> ({self.color[0]},{self.color[1]},{self.color[2]})"


class ColoredBitMap:
    def __init__(
        self,
        pixels: list,
        width: int,
        height: int,
        position: list = [0, 0],
        scale: int = 1,
    ):
        self.pixels = pixels
        self.position = position
        self.width = width
        self.height = height
        self.scale = scale
        self.pixels = []

        for i in range(len(pixels)):
            if pixels[i] != [] and pixels[i] != [None]:  # Skip empty pixels
                x = (i % width) * scale
                y = (i // width) * scale

                self.pixels.append(Pixel([x, y], pixels[i]))


class BitMap:
    def __init__(
        self,
        pixels: list,
        width: int,
        height: int,
        position: list = [0, 0],
        color: list = (255, 255, 255),
        scale: int = 1,
    ):
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

        # self.empty_array = empty_canvas

    def _get_valid_points_mask(self, points: np.ndarray, x_min, y_min, x_max, y_max):
        return (
            (points[:, 0] >= x_min)
            & (points[:, 0] < x_max)
            & (points[:, 1] >= y_min)
            & (points[:, 1] < y_max)
        )

    def contains_points(self, points: np.ndarray):

        # Check bounding box first to eliminate points that are clearly outside
        x_min = self.position[0]
        y_min = self.position[1]
        x_max = x_min + self.width * self.scale
        y_max = y_min + self.height * self.scale

        # Check if the cached result is still valid
        if x_min > 128 or y_min > 128 or x_max < 0 or y_max < 0:
            return empty_canvas

        # Eliminate points outside the bounding box
        self._get_point_axes(points)

        valid_points_mask = self._get_valid_points_mask(
            points, x_min, y_min, x_max, y_max
        )

        valid_points = self._compute_valid_points(points, valid_points_mask)

        if valid_points.size == 0:
            return empty_canvas

        # Proceed with containment checks for valid points
        result_mask = self._compute_contains_points(valid_points)

        # Fill the original points array with results
        return self._compute_final_mask(valid_points_mask, result_mask)

    def _compute_valid_points(self, points: np.ndarray, valid_points_mask):
        # Only process points inside the bounding box
        return points[valid_points_mask]

    def _compute_final_mask(self, valid_points_mask, result_mask):
        final_mask = np.zeros(len(valid_points_mask), dtype=bool)
        final_mask[valid_points_mask] = result_mask
        return final_mask

    def _compute_contains_points(self, points: np.ndarray):
        """Computes the point containment using vectorized NumPy operations."""
        # Generate coordinates for all pixels that are "on" (value = 1)
        pixel_indices = np.where(np.array(self.pixels) == 1)[0]
        x_coords = (pixel_indices % self.width) * self.scale + self.position[0]
        y_coords = (pixel_indices // self.width) * self.scale + self.position[1]

        # Create bounding boxes for each pixel
        x_min = x_coords[:, None]
        y_min = y_coords[:, None]
        x_max = x_min + self.scale
        y_max = y_min + self.scale

        # Check if points fall within any of the pixel bounding boxes

        mask = np.any(
            self._get_valid_points_mask(points, x_min, y_min, x_max, y_max),
            axis=0,
        )
        return mask

    def _get_point_axes(self, points: np.ndarray):
        if self.cached_points_x is None or self.cached_points_y is None:
            self.cached_points_x = points[:, 0]
            self.cached_points_y = points[:, 1]

        return self.cached_points_x, self.cached_points_y

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
        self.cached_points_x = None
        self.cached_points_y = None

    def _bbox_intersects(self, bbox1, bbox2):
        """Check if two bounding boxes intersect."""
        x1_min, y1_min, x1_max, y1_max = bbox1
        x2_min, y2_min, x2_max, y2_max = bbox2

        return not (
            x1_max < x2_min or x1_min > x2_max or y1_max < y2_min or y1_min > y2_max
        )

class Image(ColoredBitMap):
    def __init__(self, width: int, height: int, position: list = [0, 0], scale: int = 1):
        super().__init__(pixels=[], width=width, height=height, position=position, scale=scale)

    def loadfile(self, filename: str):
        if os.path.exists(filename):
            imgsurface = pygame.image.load(filename)

            # check to make sure size matches
            if(imgsurface.get_height() != self.height or imgsurface.get_width() != self.width):
                pygame.transform.scale(imgsurface,(self.width,self.height))
            
            # Loop through and make a bitmap of pixels
            for x in range(0,self.width):
                for y in range(0,self.height):
                    self.pixels.append(Pixel([x,y], color=tuple(imgsurface.get_at((x,y))[0:3])))

        else:
            print(f"File {filename} does not exist. Try again.")
    
    def loadpixels(self, pixels: list):
        for i in range(len(pixels)):
            if pixels[i] != [] and pixels[i] != [None]:  # Skip empty pixels
                x = (i % self.width) * self.scale
                y = (i // self.height) * self.scale

                self.pixels.append(Pixel([x, y], color=pixels[i]))

class Letter(BitMap):
    def __init__(
        self,
        char: str,
        position: list = [0, 0],
        color: list = [255, 255, 255],
        size: int = 1,
    ):
        self.char = ""
        self.mask = [  # Default mask
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
        ]
        self.position = position
        self.color = color
        self.size = size

        # Initialize the character mask and the bitmap
        super().__init__(self.mask, 8, 8, position, color, size)

        # Set the character
        self.set_char(char)

    def set_char(self, new_char: str):
        """Update the character and invalidate the cache."""
        if new_char != self.char:
            self.char = new_char

            if self.char in utils.char_mask:
                self.mask = utils.char_mask[self.char]
            else:
                self.mask = [
                    ((i + j) % 2 == 1) for i in range(8) for j in range(8)
                ]  # Return a checkered pattern if the character is not found
                # self.mask = [  # Return a checkered pattern if the character is not found
                #     False, True, False, True, False, True, False, True,
                #     True, False, True, False, True, False, True, False,
                #     False, True, False, True, False, True, False, True,
                #     True, False, True, False, True, False, True, False,
                #     False, True, False, True, False, True, False, True,
                #     True, False, True, False, True, False, True, False,
                #     False, True, False, True, False, True, False, True,
                #     True, False, True, False, True, False, True, False,
                # ]

            # run_setbitmap
            self.set_bitmap(self.mask, 8, 8)

    def set_position(self, new_position: list):
        """Update the position and invalidate the cache."""
        if new_position != self.position:
            self.position = new_position

    def set_color(self, new_color: list):
        """Update the color and invalidate the cache."""
        if new_color != self.color:
            self.color = new_color

    def get_width(self):
        return 8 * self.size
