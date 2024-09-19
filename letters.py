from matrix_library import canvas as c, shapes as s

canvas = c.Canvas()

test = s.Phrase("Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz 01 23 45 67 89 !? @$ &- += *%", (0, 0), (255, 255, 255), auto_newline=True)

while True:
  canvas.clear()
  canvas.add(test)
  canvas.draw()