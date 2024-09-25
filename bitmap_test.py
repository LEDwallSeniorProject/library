from matrix_library import canvas as c, shapes as s

# Define dimensions
width = 8
height = 8

# Create a blank bitmap (initialized to white) in 1D format
bitmap = [[None]] * (width * height)
print(bitmap)

# Function to set a pixel color
def set_pixel(x, y, color):
  if 0 <= x < width and 0 <= y < height:
    index = y * width + x
    bitmap[index] = color

# Example: Draw a simple pattern (a diagonal line)
for i in range(min(width, height)):
  set_pixel(i, i, (0, 0, 0))  # Set the pixel to black
    
canvas = c.Canvas()

while True:
    canvas.clear()
    canvas.add(s.ColoredBitMap(bitmap, width, height, (0, 0), 1))
    canvas.draw()