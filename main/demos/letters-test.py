from matrix_library import canvas as c, shapes as s
import string
import time
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice("/dev/input/event2")

canvas = c.Canvas()
alphabet = ''
for i in string.ascii_lowercase:

    alphabet += i
    test = s.Phrase(
        alphabet,
        (0, 0),
        (255, 255, 255),
        auto_newline=True,
        size=1,
    )

    canvas.clear()
    canvas.add(test)
    canvas.draw()
    time.sleep(0.3)
