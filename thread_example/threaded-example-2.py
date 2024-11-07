from matrix_library import canvas as c, shapes as s
import subprocess
from threading import Thread
import random
import time

# https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread
class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


# variables
mainprogram = "countdown.py"

def run_other_program(program):
	subprocess.run(["sudo","/usr/bin/python3.11",program])

def run_main_program(program):
	result = subprocess.run(["sudo","/usr/bin/python3.11",program], capture_output=True, text=True)
	return result.stdout.rstrip()

while True:
	
	# run main program
	newrandomprogram = ""
	print(f"Executing main countdown")
	mainthread = ThreadWithReturnValue(target=run_main_program, args=("countdown.py",))
	mainthread.start()
	newrandomprogram = mainthread.join()
	print(f"newrandomprogram is now: {newrandomprogram}")

	# create a thread
	print(f"Executing {newrandomprogram}")
	thread = ThreadWithReturnValue(target=run_other_program, args=(newrandomprogram,))
	thread.start()

    # Wait until the thread joins -- note that if the thread never dies I'll never come back!
	thread.join()
