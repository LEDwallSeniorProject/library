import time

class LEDProgram:
    def __init__(self, canvas, controller, fps=60):
        self.canvas = canvas
        self.controller = controller
        # check that things are defined correctly
        try:
            self.__bind_controls__
            self.__draw__
            self.__loop__
            self.preLoop
            self.postLoop
            self.__unbind_controls__
            self.quit
            self.__stop__

        except AttributeError as e:
            error = """
            Not all required functions are bound.
            Required functions:
                self.__bind_controls__
                self.__draw__
            
            Optional functions:
                self.preLoop
                self.postLoop
            
            Overridable functions: 
                self.__unbind_controls__
                self.__loop__
                self.quit  # call or overide this to exit your program
                self.__stop__ # call this to fully exit python

            Attributes:
                self.running # set to False to exit
            """
            raise Exception(error) from e

        self.__bind_controls__()
        self.running = True
        self.__exited__ = False

        self.__fps__ = fps

        self.__loop__()

    """
    Feel free to add code to this by creating your own function 
    called __loop__() in your child class and calling this with super()
    """

    def __loop__(self):
        self.preLoop()
        last_time = time.time()
        frame_time = 1 / self.__fps__
        frames = 0

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - last_time

            while elapsed_time < frame_time:
                current_time = time.time()
                elapsed_time = current_time - last_time
                time.sleep(.001)

            last_time = current_time
            frames += 1

            self.canvas.clear()
            self.__draw__()
            self.canvas.draw()

        self.postLoop()
        self.__unbind_controls__()

    def __unbind_controls__(self):
        self.controller.clear()

    def quit(self):
        self.running = False

    def __stop__(self):
        self.controller.stop()
        self.canvas.clear()
        self.running = False
        self.__exited__ = True

    def preLoop(self):
        pass

    def postLoop(self):
        pass