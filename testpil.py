from PIL import Image

image = Image.new(mode="RGBA", size=(128,128), color='black')
canvas = image.load()
for i in range(0,128):
    for j in range(0,128):
        print(i,j,canvas[i,j])
