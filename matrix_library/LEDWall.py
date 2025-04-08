import time
from matrix_library import shapes

class LEDProgram:
    def __init__(self, canvas, controller, fps=30, trackFPS=False):
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
        self.trackFPS = trackFPS

        self.__fps__ = fps

        self.__loop__()

    """
    Feel free to add code to this by creating your own function 
    called __loop__() in your child class and calling this with super()
    """

    def __loop__(self):
        self.preLoop()
        last = time.time()
        max_fps = self.__fps__
        max_frame_time = 1 / max_fps
        expected_frame_time = max_frame_time
        start = last
        fps_count = 0
        fps_time = 0
        avg_fps = 0

        while self.running:
            start_time = time.time()
            
            self.canvas.clear()
            self.__draw__()
            if self.trackFPS:
                fps_phrase = shapes.Phrase(f"FPS: {avg_fps:.0f}", [0,0])
                self.canvas.add(fps_phrase)
            self.canvas.draw()

            elapsed = time.time() - start_time
            sleep_time = expected_frame_time - elapsed

            if sleep_time > 0:
                time.sleep(sleep_time)
            
            now = time.time()
            dif = now - last
            last = now

            fps_time += dif
            fps_count += 1

            if fps_time >= 1:
                avg_fps = fps_count
                fps_count = 0
                fps_time = 0

                if avg_fps > max_fps:
                    expected_frame_time += max_frame_time * 0.05
                elif (max_fps - avg_fps) > 3:
                    expected_frame_time -= max_frame_time * 0.01
                
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