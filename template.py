import matrix_library as matrix

canvas = matrix.Canvas()  # Create a canvas object
controller = matrix.Controller()  # Create a controller object


# Keyboard to controller mappings:
# -------------------------------
#
#  |   Q   |          |   E   |
#
#     ---                ---
#    | W |              | I |
#  --     --        ---  ---  ---
# | A     D |      | J |     | L |
#  --     --        ---  ---  ---
#    | S |              | K |
#     ---                ---
controller.add_function("UP", canvas.clear)


# Main game loop
while True:
    canvas.clear()  # Clear the canvas to start fresh each frame
    controller.check_key_presses()  # Check for key presses here

    # Add shapes to canvas here:
    # canvas.add(shape)

    canvas.draw()
