import matrix_library as matrix

# Authors: Chris Wieringa, Alex Miller, Ellie Sand, Palmer Ford
# Purpose: Simple test program for controllers. Shows in STDOUT debug
#  all keypresses for controllers and keyboards, and which button
#  they all map to internally. Each internal button (LB, LB2, RB, X2, etc)
#  can be bound to a function using add_function

# Controller mappings:
# Player 1:                          Player 2:
#   | LB |              | RB |                 | LB2 |            | RB2 |
#
#       ---               ---                     ---               ---
#      | UP |            | X |                  | UP2 |            | X2 |
#  --           --     --     --             --          --     --       --
# | LEFT    RIGHT |   | Y     A |          | LEFT2    RIGHT2 | | Y2      A2 | 
#  --           --     --     --             --          --     --       --
#     | DOWN |           | B |                 | DOWN2 |           | B2 |
#       ---                                       ---               ---
#       SELECT      START                           SELECT2    START2

# Keyboard to controller mappings:
# -------------------------------
# Player 1:                          Player 2:
# | Q |            | E |             | U |           | O |
#
#     ---           ---                  ---          ---
#    | W |         | T |                | I |        | [ |
#  --     --     --     --            --     --    --     --
# | A     D |   | F     G |          | J     L |  | ;     ' | 
#  --     --     --     --            --     --    --     --
#    | S |         | V |                | K |        | / |
#     ---                                ---          ---
# SELECT: Z                           SELECT: M
# START:  C                           START: .

# Setup the basic program, getting the Canvas, Controllers, and a single polygon
canvas = matrix.Canvas()
controller = matrix.Controller(debug=True)
polygon = matrix.Polygon(matrix.get_polygon_vertices(5, 20, (64, 64)), (255, 0, 0))

# Whether to show the polygon or not
toggle = True

phrase = matrix.Phrase(text="Key: ",position=[5,115])

# Function to bind to a controller button press
def toggle_toggle():
    print("Pressed button UP")
    global phrase
    phrase.set_text("Key: UP")
    
    global toggle
    toggle = not toggle

        
# Example binding of a controller presses to a function
controller.add_function("UP", toggle_toggle)
controller.add_function("UP2", toggle_toggle)

# Make a whole lot of functions programatically for all our other possible buttons
leftoverbuttons = {
    # controller for player one, use WASD and nearby keps
    "LB": "q", "RB": "e", "DOWN": "s", "LEFT": "a", "RIGHT": "d", 
    "A": "g", "B": "v", "Y": "f", "X": "t","SELECT": "z", "START": "c",
    # controller for player two, use IJKL and nearby keys
    "LB2": "u", "RB2": "o", "DOWN2": "k", "LEFT2": "j", "RIGHT2": "l",
    "A2": "'", "B2": "/", "Y2": ";", "X2": "[", "SELECT2": "m", "START2": ".",
}
for key, value in leftoverbuttons.items():
    exec(f"def {key}(): \n\tglobal phrase\n\tphrase.set_text(\"Key: {key}\")\n\tprint(\"Pressed button {key}\")")

# Add all these functions to the controller add_functions
for button in leftoverbuttons.keys():
    controller.add_function(button, globals()[button])
    
########################
# MAIN PROGRAM

# Animation loop
while True:
    # clear the canvas
    canvas.clear()

    # check if visibility of the polygon is set to True or False; if True draw it
    if toggle:
        polygon.rotate(1, (64, 64))
        canvas.add(polygon)

    # add the phrase
    canvas.add(phrase)

    # draw to the screen
    canvas.draw()
