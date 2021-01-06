from tkinter import *
from tkinter.filedialog import askopenfilename

import PIL.Image
import cv2
import numpy as np
from PIL import ImageChops
from PIL.ExifTags import TAGS

#Tk().withdraw()
imgName = askopenfilename()

window = Tk()
window.title("Level 1 Testing")
lab = Label(window, text="Metadata analysis", width=60, height=15)
lab.pack()


def win_dest():
    window.destroy()


def level2():
    window.title("Level 2 Testing")
    lab['text'] = "Doing ELA analysis ... Please wait for a minute"
    window.update_idletasks()
    TEMP = 'temp.jpg'
    SCALE = 10
    original = PIL.Image.open(imgName)
    original.save(TEMP, quality=90)
    temporary = PIL.Image.open(TEMP)
    diff = ImageChops.difference(original, temporary)
    d = diff.load()
    WIDTH, HEIGHT = diff.size
    for x in range(WIDTH):
        for y in range(HEIGHT):
            d[x, y] = tuple(k * SCALE for k in d[x, y])

    diff.save("img.jpg")
    lab['text'] = lab['text'] + "\nDoing Histogram Analysis ..."
    window.update_idletasks()
    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read("Training.yml")
    imggray = PIL.Image.open("img.jpg").convert('L')
    gray = np.array(imggray, 'uint8')
    lab['text'] = lab['text'] + "\nResult : "
    id, conf = rec.predict(gray)
    if (id == 2 and not (test1)):
        lab['text'] = lab['text'] + "\nREAL "
        lab['text'] = lab['text'] + str(100 - conf)
    else:
        lab['text'] = lab['text'] + "\nFAKE "
        lab['text'] = lab['text'] + str(100 - conf)
    b1.pack_forget()


try:
    f = 1
    test1 = ""
    img = PIL.Image.open(imgName)
    info = img._getexif()
    if info:
        for (tag, value) in info.items():
            if "Software" == TAGS.get(tag, tag):
                lab['text'] = lab['text'] + "\nFake Image"
                lab['text'] = lab['text'] + "\nFound Software Signature : " + value
                test1 = "Signature"
                f = 0

    if f:
        lab['text'] = lab['text'] + "\nNo Software Signature Found"
        lab['text'] = lab['text'] + "\nLooks like Real"
    b1 = Button(window, text="Continue", command=level2)
    b2 = Button(window, text="Exit", command=win_dest)
    b1.pack()
    b2.pack()
except Exception as e:
    lab['text'] = lab['text'] + "\nFailed to Load Metadata : " + str(e)
    b3 = Button(window, text="Exit", command=win_dest)
    b3.pack()

window.mainloop()