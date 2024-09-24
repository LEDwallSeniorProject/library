from matrix_library import shapes as s, canvas as c
canvas = c.Canvas()
import time

square = s.Polygon(s.get_polygon_vertices(4, 60, (0,100)), (100, 200, 100))

headerline = s.Line((8, 28), (140, 28), (255, 0, 0), thickness= 2)

menuheader = s.Phrase("MENU", (0, 0), (255, 255, 255), size=3.5, auto_newline=True)
demoheader = s.Phrase("Demos", (0, 30), (255, 255, 255), size=3, auto_newline=True)
gamesheader = s.Phrase("Games", (0, 60), (255, 255, 255), size=3, auto_newline=True)
creatornames = s.Phrase("created by Alex Ellie and Palmer", (0, 100), (255, 255, 255), size=1)

controller = s.Polygon(s.get_polygon_vertices(4, 30, (5,150)), (0, 0, 255))
controller2 = s.Polygon(s.get_polygon_vertices(4, 30, (20,150)), (0, 0, 255))
countdown = s.Phrase("30", (110, 120), (255, 255, 255), size=1, auto_newline=True)

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