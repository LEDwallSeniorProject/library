import matrix_library as m
canvas = m.Canvas()
import time

square = m.Polygon(m.get_polygon_vertices(4, 60, (0,100)), (100, 200, 100))

headerline = m.Line((8, 28), (120, 28), (255, 0, 0), thickness=1)

menuheader = m.Phrase("MENU", (0, 0), (255, 255, 255), size=3.5, auto_newline=True)
demoheader = m.Phrase("Demos", (0, 30), (255, 255, 255), size=3, auto_newline=True)
gamesheader = m.Phrase("Games", (0, 60), (255, 255, 255), size=3, auto_newline=True)
creatornames = m.Phrase("created by Alex Ellie and Palmer", (0, 100), (255, 255, 255), size=1)

controller = m.Polygon(m.get_polygon_vertices(4, 30, (5,150)), (0, 0, 255))
controller2 = m.Polygon(m.get_polygon_vertices(4, 30, (20,150)), (0, 0, 255))
countdown = m.Phrase("30", (110, 120), (255, 255, 255), size=1, auto_newline=True)

while True:
    canvas.clear()
    canvas.add(square)
    canvas.add(headerline)
    canvas.add(menuheader)
    canvas.add(demoheader)
    canvas.add(gamesheader)
    creatornames.translate(-2, 0)
  # print(text.position[0])
    if creatornames.get_width() + creatornames.position[0] < 0:
        creatornames.set_position([128, 100])
    canvas.add(creatornames)

    canvas.add(controller)
    canvas.add(controller2)
    canvas.add(countdown)

    canvas.draw()
    time.sleep(0)