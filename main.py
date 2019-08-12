
import time

from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import ntpath
import cv2
import numpy as np
import math

import random

import matplotlib
import matplotlib.pyplot as plt
import skimage.io as io
from skimage.filters import threshold_otsu
from skimage import img_as_ubyte
#"load image data"

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)   

        self.fullImageL = None
        self.imgSize = 600

        self.maxDiff = 20

        #reference to the master widget, which is the tk window                 
        self.master = master
        self.panelA = None
        self.panelB = None

        self.square = None
        self.buttonSet = None
        self.spin = None

        self.textYes, self.textNo = None, None
        self.scoreYes, self.scoreNo = 0, 0

        self.init_window()

    

##########################################################
    def imgInitState(self):
        self.fullImageL = np.zeros((self.imgSize, self.imgSize, 3),np.uint8)

        color = list(np.random.choice(range(40,160), size=3))

        for i in range(10,190):
            for j in range(10,190):
                for c in range(0,3):
                    self.fullImageL[i,j,c] = color[c]
                    self.fullImageL[i + 200, j + 200,c] = color[c]
                    self.fullImageL[i + 400, j + 400,c] = color[c]

                    self.fullImageL[i, j + 200, c] = color[c]
                    self.fullImageL[i, j + 400, c] = color[c]
                    self.fullImageL[i + 200, j + 400, c] = color[c]


                    self.fullImageL[i + 200, j, c] = color[c]
                    self.fullImageL[i + 400, j + 200, c] = color[c]
                    self.fullImageL[i + 400, j, c] = color[c]

        posiR = random.randint(0,2)
        posjR = random.randint(0,2)

        self.square = [posiR, posjR]

        for i in range(10 + posiR * 200, 190 + posiR * 200):
            for j in range(10 + posjR * 200, 190 + posjR * 200):
                for c in range(0,3):
                    self.fullImageL[i,j,c] = color[c] + self.maxDiff


        self.updatePanelL()


    def validatePos(self,cX, cY):
        sQx = self.square[1] * 200
        sQy = self.square[0] * 200

        print(sQx, sQy)
        print(cX, cY)

        if sQx > cX or sQx + 200 < cX or sQy > cY or sQy + 200 < cY:
            self.scoreNo += 1
            return

        self.scoreYes += 1

    def updateScore(self):
        self.textYes.configure(text = str(self.scoreYes))
        self.textNo.configure(text = str(self.scoreNo))

     # get postion of mouse click in imageL 
    def selectSquare( self, event):
        valClickX = event.x
        valClickY = event.y

        self.validatePos(valClickX, valClickY)
        self.updateScore()
        self.imgInitState()


    def setMaxDiff(self):
        self.maxDiff = int(self.spin.get())
        self.imgInitState()


    # update the left panel with self.imageRL
    # transform cv2 image to tkinter image and show
    def updatePanelL(self):
        img = cv2.resize(self.fullImageL,(600,600))

        im = Image.fromarray(img, 'RGB')      
        imgtk = ImageTk.PhotoImage(image = im)
        
        self.panelA = Label(self.master, image=imgtk)
        self.panelA.image = imgtk
        self.panelA.place(x=10, y=10)

        # bind mouse events to window
        self.panelA.bind( "<Button-1>", self.selectSquare)


    #Creation of init_window
    def init_window(self):
        import tkinter as tk

        # changing the title of our master widget      
        self.master.title("eyeTest")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)


        self.imgInitState()


        # Label
        textL = Label(self.master, text="MaxDifference")
        textL.place(y = 150,x = 633)
        # SpinBox
        self.spin = Spinbox(self.master, from_=1, to=15)
        self.spin.place(y = 170, x = 620, width=60)
         # Buttpn
        but = Button(self.master, text = "set", command=self.setMaxDiff)
        but.place(y = 170, x = 690, height = 21, width=60)


        t = Label(self.master, text="yes")
        t.place(y = 250,x = 633)
        t = Label(self.master, text="no")
        t.place(y = 270,x = 633)
        self.textYes = Label(self.master, text="")
        self.textYes.place(y = 250,x = 663)
        self.textNo = Label(self.master, text="")
        self.textNo.place(y = 270,x = 663)
######################################################     ^
    

root = Tk()

root.geometry("800x620")

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  