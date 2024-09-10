from polygon import Polygon, get_polygon_vertices
import numpy as np


x, y = np.meshgrid(np.arange(128), np.arange(128)) # make a canvas with coordinates
x, y = x.flatten(), y.flatten()
points = np.vstack((x,y)).T

verts1 = get_polygon_vertices(4, 20, (64,96))
polygon = Polygon(verts1, 'red')

print(polygon.vertices)

polygon = polygon.rotate(45, (64,96))

print(polygon.vertices)

mask = polygon.contains_points(points)





# draw to console
row = ""
for i in mask:
  if i:
    row += "X"
  else:
    row += "_"
  if len(row) == 128:
    print(row)
    row = ""