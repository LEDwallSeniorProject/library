import matrix_library as m

canvas = m.Canvas()

text = m.Phrase("WOW!", [64, 64], size=8)

while True:
  canvas.clear()
  text.translate(-2, 0)
  if text.get_width() + text.position[0] < 0:
    text.set_position([128, (text.position[1] + 64) % 128])
  canvas.add(text)
  canvas.draw()
  
  
  