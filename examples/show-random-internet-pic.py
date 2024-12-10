from PIL import Image
import matrix_library as matrix
import time
import requests
import io
import sys

# program setup
controller = matrix.Controller()
canvas = matrix.Canvas()

# variables
exited = False
loading = matrix.Phrase(text="Loading image...",position=[0,120],size=1)

def exit_prog():
    global exited
    exited = True

# random picture URL
w = h = 128
url = f"https://picsum.photos/{w}"

controller.add_function("START", exit_prog)

for i in range(0,3):
    if not exited:
        
        canvas.add(loading)
        canvas.draw()

        r = requests.get(url, stream=True, timeout=2)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            pixels = list(img.getdata())
            #print(pixels)
            img = matrix.Image(width=128,height=128,position=[0,0])
            img.loadpixels(pixels)

            canvas.add(img)
            canvas.draw()
        else:
            phrase = matrix.Phrase("Image load failed")
            canvas.add(phrase)
            canvas.draw()
        
        # pause for a second between them, but check for exits
        maxwait = 3
        timer = 0
        sleepstep = 0.25
        while timer < maxwait:
            if exited: timer += 10000
            else: 
                time.sleep(sleepstep)
                timer += sleepstep
    

# clear the screen before exiting
print("quit")
sys.exit(0)