import numpy as np
import math
import os

# Hide PyGame notifications
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# Empty template
empty_canvas = np.zeros((128 * 128), dtype=bool)


# is the point inside check with Ray Casting Algorithm : 
def ray_casting_contains_points(points: np.ndarray, vertices: np.ndarray) -> np.ndarray:
    result = np.zeros(len(points), dtype=bool)

    for i, (px, py) in enumerate(points):
        crossings = 0
        for j in range(len(vertices)):
            v1 = vertices[j]
            v2 = vertices[(j + 1) % len(vertices)]

            if ((v1[1] > py) != (v2[1] > py)) and (
                px < v1[0] + (py - v1[1]) * (v2[0] - v1[0]) / (v2[1] - v1[1])
            ):
                crossings += 1

        result[i] = crossings % 2 == 1

    return result


# POLYGON CLASS: 
class Polygon:
    def __init__(self, vertices: list, color: tuple = (255, 255, 255)):
        if len(vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        self.vertices = np.array(vertices)
        self.color = color
        self.center = self.calculate_center()

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        return ray_casting_contains_points(points, self.vertices)

    def translate(self, dx: float, dy: float) -> None:
        self.vertices += np.array([dx, dy])
        self.center = (self.center[0] + dx, self.center[1] + dy)

    def rotate(self, angle_degrees: float, center: tuple = (0, 0)) -> None:
        angle_radians = np.radians(angle_degrees)
        cos_angle = np.cos(angle_radians)
        sin_angle = np.sin(angle_radians)

        rotated_vertices = []
        for x, y in self.vertices:
            x_translated = x - center[0]
            y_translated = y - center[1]

            x_rotated = x_translated * cos_angle - y_translated * sin_angle
            y_rotated = x_translated * sin_angle + y_translated * cos_angle

            rotated_vertices.append((x_rotated + center[0], y_rotated + center[1]))

        self.vertices = np.array(rotated_vertices)

    def calculate_center(self) -> tuple:
        cx, cy = np.mean(self.vertices, axis=0)
        return (cx, cy)


# CIRCLE CLASS :
class Circle:
    def __init__(self, radius: float, center: tuple, color: tuple = (255, 255, 255)):
        if radius <= 0:
            raise ValueError("Radius must be greater than zero.")

        self.center = np.array(center)
        self.radius = radius
        self.color = color

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        distances = np.linalg.norm(points - self.center, axis=1)
        return distances <= self.radius


# LINE CLASS:
class Line(Polygon):
    def __init__(self, start: list, end: list, color: list = (255, 255, 255), thickness: float = 0.5):
        if start == end:
            raise ValueError("The start and end points of a line cannot be the same.")
        if thickness <= 0:
            raise ValueError("The thickness of a line must be greater than 0.")

        self.start = np.array(start)
        self.end = np.array(end)
        self.thickness = thickness
        self.vertices = [self.start, self.end]

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        vec = self.end - self.start
        length = np.linalg.norm(vec)
        vec = vec / length if length != 0 else vec

        proj = np.dot(points - self.start, vec)
        proj_clamped = np.clip(proj, 0, length)

        closest_points = self.start + proj_clamped[:, None] * vec
        distances = np.linalg.norm(points - closest_points, axis=1)
        return distances <= self.thickness


# (PolygonOutline)
class PolygonOutline(Polygon):
    def __init__(self, vertices: list, color: tuple = (255, 255, 255), thickness: float = 1):
        super().__init__(vertices, color)
        self.thickness = thickness
        self.inner_vertices = self.calculate_inner_vertices()

    def calculate_inner_vertices(self):
        center = self.calculate_center()
        inner_vertices = []
        for x, y in self.vertices:
            direction_x = x - center[0]
            direction_y = y - center[1]
            magnitude = math.sqrt(direction_x**2 + direction_y**2)
            if magnitude > 0:
                direction_x /= magnitude
                direction_y /= magnitude
                new_x = x - direction_x * self.thickness
                new_y = y - direction_y * self.thickness
                inner_vertices.append((new_x, new_y))
        return np.array(inner_vertices)

    def contains_points(self, points: np.ndarray) -> np.ndarray:
        outer_mask = ray_casting_contains_points(points, self.vertices)
        inner_mask = ray_casting_contains_points(points, self.inner_vertices)
        return np.logical_and(outer_mask, np.logical_not(inner_mask))


# (CircleOutline)
class CircleOutline(PolygonOutline):
    def __init__(self, radius, center, color=(255, 255, 255), thickness=1):
        vertices = get_polygon_vertices(radius * 10, radius, center)
        super().__init__(vertices, color, thickness)
        self.radius = radius

    def contains_points(self, points: np.ndarray):
        circle1_mask = Circle(self.radius, self.center, self.color).contains_points(points)
        circle2_mask = Circle(self.radius - self.thickness, self.center, self.color).contains_points(points)
        return np.logical_and(circle1_mask, np.logical_not(circle2_mask))


# POLYGON corner ponint Calculating:
def get_polygon_vertices(sides: int, radius: float = 1, center: tuple = (0, 0)) -> list:
    if sides < 3:
        raise ValueError("A polygon must have at least 3 sides")

    angle_step = 2 * math.pi / sides
    vertices = [(center[0] + radius * math.cos(i * angle_step), center[1] + radius * math.sin(i * angle_step)) for i in range(sides)]
    return vertices
