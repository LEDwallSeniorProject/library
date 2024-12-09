import matrix_library as matrix

canvas = matrix.Canvas()

while True:
    canvas.clear()
    canvas.add(matrix.Pixel((64, 64)))
    canvas.draw()
