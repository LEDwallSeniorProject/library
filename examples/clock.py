from datetime import datetime
import sys
import matrix_library as matrix
import time

controller = matrix.Controller()
canvas = matrix.Canvas()

exited = False

def exit_prog():
    global canvas, exited
    print("quit")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

circle = matrix.CircleOutline(64, (64, 64), (255, 255, 255))

markers = []
for i in range(12):
    marker = matrix.Line((64, 16), (64, 8), (255, 255, 255))
    marker.rotate(i * 30, (64, 64))
    markers.append(marker)

controller.add_function("START", exit_prog)

while True:
    if exited: sys.exit(0)
    canvas.clear()

    hour_hand = matrix.Line((64, 64), (64, 24), (255, 0, 0))
    minute_hand = matrix.Line((64, 64), (64, 20), (0, 255, 0))
    second_hand = matrix.Line((64, 64), (64, 16), (0, 0, 255))

    now = datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    millisecond = now.microsecond / 1000

    hour_angle = (hour % 12) * 30 + (minute / 60) * 30
    minute_angle = minute * 6 + (second / 60) * 6
    second_angle = second * 6 + (millisecond / 1000) * 6

    hour_hand.rotate(hour_angle, (64, 64))
    minute_hand.rotate(minute_angle, (64, 64))
    second_hand.rotate(second_angle, (64, 64))

    canvas.add(circle)

    for marker in markers:
        canvas.add(marker)

    canvas.add(hour_hand)
    canvas.add(minute_hand)
    canvas.add(second_hand)
    canvas.draw()
    time.sleep(1)
