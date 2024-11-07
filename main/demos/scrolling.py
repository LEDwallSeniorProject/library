from matrix_library import canvas as c, shapes as s
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice("/dev/input/event2")

canvas = c.Canvas()

text = s.Phrase("WOW!", [64, 64], size=8)

def exit_prog():
    print(quit)
    canvas.delete()
    sys.exit()

while True:
        if gamepad.active_keys() == [24]:
    exit_prog()

    canvas.clear()
    text.translate(-2, 0)
    if text.get_width() + text.position[0] < 0:
        text.set_position([128, (text.position[1] + 64) % 128])
    canvas.add(text)
    canvas.draw()
