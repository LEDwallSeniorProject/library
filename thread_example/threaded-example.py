from matrix_library import canvas as c, shapes as s
import subprocess
import threading
import random
import time

def run_other_program(program):
	subprocess.run(["sudo","/usr/bin/python3.11",program])

programs = ["clock-test.py","letters-test.py","spin2-test.py","fps-test.py","bounce2-test.py"]

while True:
	# initialize canvas
	canvas = c.Canvas()
	for i in reversed(range(1,4)):
		test = s.Phrase(
    	    "Test threading",
    	    (0, 0),
    	    (255, 255, 255),
    	    auto_newline=True,
    	    size=1,
    	)

		count = s.Phrase(
			f"in {i} ...",
			(0,10),
			(255,255,255),
			auto_newline=True,
			size=1,
		)

		canvas.clear()
		canvas.add(test)
		canvas.add(count)
		canvas.draw()
		time.sleep(1)

	# sleep 3 seconds, delete my canvas, then launch a random program
	del canvas

	# create a thread
	randomprog = random.choice(programs)
	print(f"Executing {randomprog}")
	thread = threading.Thread(target=run_other_program, args=(randomprog,))
	thread.start()

    # Wait until the thread joins -- note that if the thread never dies I'll never come back!
	thread.join()
