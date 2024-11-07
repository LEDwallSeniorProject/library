import time
import subprocess
import os
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

def run_program(program):
	result = subprocess.run(["sudo","/usr/bin/python3.11",program], capture_output=True, text=True)
	return result.stdout.rstrip()

def run_shutdown():
	result = subprocess.run(["sudo","/usr/sbin/halt"], capture_output=True, text=True)
	return result.stdout.rstrip()

# initial setup
dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)

while True:
    # run main program
    print("Loop start")
    mainthread = ThreadWithReturnValue(target=run_program, args=("mainMenu.py",))
    mainthread.start()
    subDemo = mainthread.join()

    if subDemo == "demos":
        programs = ["demos/clock-test.py","demos/spin2-test.py","demos/fps-test.py","demos/bounce2-test.py"]

        for prog in programs:
            thread = ThreadWithReturnValue(target=run_program, args=(prog,))
            thread.start()
            result = thread.join()
            if result == "quit":
                break
    elif subDemo == "shutdown":
        thread = ThreadWithReturnValue(target=run_shutdown)
        thread.start()

    # elif subDemo == "snake":
    # 	thread = ThreadWithReturnValue(target=run_other_program, args=(subDemo,))
    # 	thread.start()
    # elif subDemo == "pong":
    # 	thread = ThreadWithReturnValue(target=run_other_program, args=(subDemo,))
    # 	thread.start()

    # create a thread
    else:
        print(f"Executing {subDemo}")
        thread = ThreadWithReturnValue(target=run_program, args=(subDemo,))
        thread.start()

        # Wait until the thread joins -- note that if the thread never dies I'll never come back!
        thread.join()