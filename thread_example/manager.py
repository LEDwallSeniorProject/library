import time
import subprocess
from threading import Thread
from matrix_library import shapes as s, canvas as c
from evdev import InputDevice, categorize, ecodes

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

def run_other_program(program):
	subprocess.run(["sudo","/usr/bin/python3.11",program])

def run_main_program(program):
	result = subprocess.run(["sudo","/usr/bin/python3.11",program], capture_output=True, text=True)
	return result.stdout.rstrip()

while True:
    # run main program
    mainthread = ThreadWithReturnValue(target=run_main_program, args=("mainMenu.py",))
    mainthread.start()
    subDemo = mainthread.join()

    # if subDemo == "demos":
    #     print(f"Executing {subDemo}")
    # 	thread = ThreadWithReturnValue(target=run_other_program, args=(subDemo,))
    # 	thread.start()
    # elif subDemo == "snake":
    #     print(f"Executing {subDemo}")
    # 	thread = ThreadWithReturnValue(target=run_other_program, args=(subDemo,))
    # 	thread.start()
    # elif subDemo == "pong":
    #     print(f"Executing {subDemo}")
    # 	thread = ThreadWithReturnValue(target=run_other_program, args=(subDemo,))
    # 	thread.start()

    # create a thread
    print(f"Executing {subDemo}")
    thread = ThreadWithReturnValue(target=run_other_program, args=(subDemo,))
    thread.start()

    # Wait until the thread joins -- note that if the thread never dies I'll never come back!
    thread.join()