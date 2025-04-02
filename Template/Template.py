from matrix_library import LEDWall, Canvas, Controller, shapes


class Template(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        # define any of your variables here

        # begin the code (this triggers execution of the loop)
        super().__init__(canvas, controller)

    # REQUIRED FUNCTION
    # this function will run every frame
    # and should contain graphics code
    # and updates
    def __draw__(self):
        title = shapes.Phrase("Hello World")
        self.canvas.add(title)

    # REQUIRED FUNCTION
    # this function will run once at super().__init__()
    # and should contain mappings to control the program
    def __bind_controls__(self):
        pass

    # code defined here will run before the main loop begins 
    #   but after all init is done
    def preLoop(self):
        pass

    # this code runs after the loop has run
    def postLoop(self):
        pass

# every program needs this line
if __name__ == "__main__":
    Template(Canvas(), Controller())
