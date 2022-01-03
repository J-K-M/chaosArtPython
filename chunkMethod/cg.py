from tkinter import *
from tkinter import ttk
from PIL import Image,ImageDraw,ImageTk

class ChaosGenerator:
    def __init__(self, parentWindow, width=1280, height=720) -> None:

        self.width = width
        self.height = height
        self.backgroundColour = (10,10,12)

        self.numPoints = 100000
        self.scale = width*0.2
        self.pixelSize = 0.5 # actual pixel size is double this value
        self.pixelColourFunc = lambda i, n: ( 
            int(128*(i/n)+128),     # R
            int(128*(i/n)+128),     # G
            int(220 - 128*(i/n))    # B
        )

        self.baseImage = Image.new("RGB", (self.width, self.height), self.backgroundColour)
        self.draw = ImageDraw.Draw(self.baseImage)
        self.tkImage = ImageTk.PhotoImage(self.baseImage)

        self.f = ttk.Frame(parentWindow)
        self.l = ttk.Label(self.f, image=self.tkImage)
        self.l.grid(row=1, column=1)

        self.running = None

        self.xFunc = lambda x, y, t: -x**2 -t**2 + x*t - y*t - x
        self.yfunc = lambda x, y, t: -x**2 -t**2 + x*t - x - y
        

    def generateEquations(self, code):
        print(code)

    def generateCode(self):
        print(self.xFunc)
        print(self.yfunc)


    def updateImage(self, t=0):
        self.draw.rectangle((0,0,self.width,self.height), fill=self.backgroundColour)
        x, y = t, t

        for i in range(self.numPoints):
            if x < self.width and y < self.height:
                self.draw.rectangle(
                    (
                        (x*self.scale + self.width/2) - 0.5,
                        (y*self.scale + self.height/2) - 0.5,
                        (x*self.scale + self.width/2) + 0.5,
                        (y*self.scale + self.height/2) + 0.5,
                    ),
                    fill=self.pixelColourFunc(i, self.numPoints)
                )

                try:
                    nx = self.xFunc(x,y,t)
                    ny = self.yfunc(x,y,t)

                    x, y = nx, ny
                except OverflowError:
                    pass
                
        
        self.tkImage = ImageTk.PhotoImage(self.baseImage)
        self.l.configure(image = self.tkImage)


    def updateImagePoints(self, t=0, x=0, y=0, count=0, pixelNum=1000):
        if self.f.winfo_exists():


            if count == 0:
                self.draw.rectangle((0,0,self.width,self.height), fill=self.backgroundColour)

            if count >= self.numPoints:
                self.running = None
                print("done")

            for i in range(pixelNum):
                if x < self.width and y < self.height:
                    self.draw.rectangle(
                        (
                            (x*self.scale + self.width/2) - 0.5,
                            (y*self.scale + self.height/2) - 0.5,
                            (x*self.scale + self.width/2) + 0.5,
                            (y*self.scale + self.height/2) + 0.5,
                        ),
                        fill=self.pixelColourFunc(count, self.numPoints)
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
                self.running = self.f.after_idle(
                    lambda: self.updateImagePoints(
                        t=t,
                        x=x,
                        y=y,
                        count=count
                    )
                )
