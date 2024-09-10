from polygon import Polygon

class Circle(Polygon):
  def __init__(self, radius, center, color=(255, 255, 255)):
    vertices = self.polygon_vertices(100, radius, center)
    super().__init__(vertices, color)
    self.radius = radius
    self.center = center