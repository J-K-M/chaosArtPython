from tkinter import *
from tkinter import ttk
from PIL import Image,ImageDraw,ImageTk

class ChaosGenerator:
    def __init__(self, parentWindow, width=1280, height=720) -> None:
        self.parentWindow = parentWindow
        self.width = width
        self.height = height
        self.backgroundColour = (10,10,12)

        self.numPoints = 1000000
        self.scale = width*0.2
        self.pixelSize = 1
        self.pixelColourFunc = lambda i, n: ( 
            int(128*(i/n)+128),     # R
            int(128*(i/n)+128),     # G
            int(220 - 128*(i/n)),   # B
            int(50)                 # A
        )
        self.xFunc = lambda x, y, t: -x**2 -t**2 + x*t - y*t - x
        self.yfunc = lambda x, y, t: -x**2 -t**2 + x*t - x - y

        self.baseImage = Image.new("RGB", (self.width, self.height), self.backgroundColour)
        self.draw = ImageDraw.Draw(self.baseImage, mode="RGBA")
        self.tkImage = ImageTk.PhotoImage(self.baseImage)

        self.f = ttk.Frame(parentWindow)
        self.l = ttk.Label(self.f, image=self.tkImage)
        self.l.grid(row=1, column=1)

        self.running = None


    def generateEquations(self, code):
        print(code)

    def generateCode(self):
        print(self.xFunc)
        print(self.yfunc)


    def updateImagePoints(self, t=0, x=0, y=0, count=0, pixelNum=1000):
        if count == 0:
            self.draw.rectangle((0,0,self.width,self.height), fill=self.backgroundColour)

        if count >= self.numPoints:
            self.running = None
            print("done")

        for i in range(pixelNum):
            if x < self.width and y < self.height:

                x1 = int(x*self.scale + self.width/2)  #- self.pixelSize/2
                y1 = int(y*self.scale + self.height/2) #- self.pixelSize/2
                x2 = x1 + self.pixelSize
                y2 = y1 + self.pixelSize
                self.draw.point(
                    ( x1, y1),
                    fill=( 
                        255,  # R
                        255,  # G
                        255,  # B
                        30    # A
                    )
                )   
                count += 1

                try:
                    nx = -x**2 -t**2 + x*t - y*t - x
                    ny = -x**2 -t**2 + x*t - x - y

                    x, y = nx, ny
                except OverflowError:
                    pass
        

        bottom = self.height * .8
        top = self.height * .2
        left = self.width * .965
        right = self.width * .975
        
        self.draw.rectangle((left, bottom, right, top), fill="white")
        self.draw.rectangle((left, bottom, right, bottom + (top-bottom) *(count/self.numPoints)), fill="grey")

        self.tkImage = ImageTk.PhotoImage(self.baseImage)
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