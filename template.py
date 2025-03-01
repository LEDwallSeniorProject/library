from LEDWall import *

class Template(LEDProgram):
    def __init__(self, canvas, controller):
        # define any of your variables here

        # begin the code (this triggers execution of the loop)
        super().__init__(canvas, controller)

    # REQUIRED FUNCTION
    # this function will run every frame
    # and should contain graphics code
    # and updates
    def __draw__(self):
        title = Shapes.Phrase("Hello World")
        self.canvas.add(title)

    # REQUIRED FUNCTION
    # this function will run once at super().__init__()
    # and should contain mappings to control the program
    def __bind_controls__(self):
        self.controller.add_function("UP", self.goUp)
        self.controller.add_function("DOWN", self.goDown)

    # controls map to functions
    def goUp(self):
        # code to make something happen on up here
        pass

    def goDown(self):
        # code to make something happen on down here
        pass

    # OPTIONAL FUNCTION
    # this function will override the __loop__() function
    # use super().__loop__() if you just want to add code 
    # before the loop begins or after it ends
    # or write your own looping
    def __loop__(self):
        # code here will run once before loop starts
        super().__loop__()
        # code here will run once after the loop ends


# every program needs this line
if __name__ == "__main__":
    Template(matrix.Canvas(), matrix.Controller())
    
   
