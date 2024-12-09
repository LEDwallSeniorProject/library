import matrix_library as matrix
import random

# Define dimensions
width = 8
height = 8

# Create a blank bitmap (initialized to white) in 1D format
bitmap = [[None]] * (width * height)


# Function to set a pixel color
def set_pixel(index, color):
    bitmap[index] = color


for i in range(width * height):
    set_pixel(
        i, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    )

canvas = matrix.Canvas()

while True:
    canvas.clear()
    canvas.add(matrix.ColoredBitMap(bitmap, width, height, (0, 0), 1))
    canvas.draw()
