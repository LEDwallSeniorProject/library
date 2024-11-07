from matrix_library import canvas as c, shapes as s
import time
import random

programs = ["clock-test.py","letters-test.py","spin2-test.py","fps-test.py","bounce2-test.py"]

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

# stdout a "random" program from my list
# This would mimic a "button press" to exit the menu with output so that the main thread could startup the subprocess
randomprog = random.choice(programs)
print(randomprog)