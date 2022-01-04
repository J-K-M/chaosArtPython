from tkinter import *
from tkinter import ttk
from PIL import Image,ImageDraw,ImageTk
from random import randint

class ChaosGenerator:
    def __init__(self, parentWindow, width=1280, height=720, 
                scale=0.2, xOffset=0.5, yOffset=0.5, previewScale=2) -> None:

        self.parentWindow = parentWindow
        self.width = width
        self.height = height
        self.backgroundColour = (10,10,12)

        self.numPoints = 1000000
        self.xScale = width * scale
        self.yScale = height * scale

        self.previewScale = previewScale

        self.baseImage = Image.new(
            "RGB", (self.width, self.height), 
            self.backgroundColour
        )
        self.draw = ImageDraw.Draw(self.baseImage, mode="RGBA")
        self.tkImage = ImageTk.PhotoImage(
            self.baseImage.resize(
                (self.width//previewScale, 
                self.height//previewScale)
        ))

        self.f = ttk.Frame(parentWindow)
        self.l = ttk.Label(self.f, image=self.tkImage)
        self.l.grid(row=1, column=1)

        self.running = None

        self.bottom = self.height * .8
        self.top = self.height * .2
        self.left = self.width * .965
        self.right = self.width * .975

        self.xCenter = width * xOffset
        self.yCenter = height * yOffset

    def updateImagePoints(self, t=0, x=0, y=0, count=0, pixelNum=20000):
        if count == 0:
            opacity = 60 # Higher opacity on first pass for clearer preview
            self.draw.rectangle(
                (0,0,self.width,self.height), 
                fill=self.backgroundColour)      # Clears points
        else:
            opacity = 20

        for i in range(pixelNum):
            if x < self.width and y < self.height:

                xpos = int(x*self.xScale + self.xCenter)
                ypos = int(y*self.yScale + self.yCenter)
                try:
                    self.draw.point(
                        ( xpos, ypos),
                        fill=(
                            int(128 + 64*count/self.numPoints), 
                            int(128 + 128*count/self.numPoints), 
                            int(255 - 128*count/self.numPoints), 
                            opacity
                        )
                    )   
                    count += 1

                    nx = -x**2 -t**2 + x*t - y*t - x
                    ny = -x**2 -t**2 + x*t - x - y

                    x, y = nx, ny
                except:
                    pass
        
        self.draw.rectangle(
            (self.left, self.bottom, self.right, self.top), 
            fill="white"
        )
        self.draw.rectangle(
            (self.left, self.bottom, self.right, 
            self.bottom + (self.top-self.bottom) *(count/self.numPoints)), 
            fill="grey"
        )

        self.tkImage = ImageTk.PhotoImage(
            self.baseImage.resize(
                (self.width//self.previewScale, 
                self.height//self.previewScale)
        ))
        self.l.configure(image = self.tkImage)

        if count < self.numPoints:
            self.running = self.parentWindow.after_idle(
                lambda: self.updateImagePoints(
                    t=t,
                    x=x,
                    y=y,
                    count=count
                )
            )