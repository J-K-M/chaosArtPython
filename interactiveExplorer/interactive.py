from tkinter import *
from tkinter import simpledialog
from cg import ChaosGenerator


xFunc = lambda x,y,t: -y**2 - x*t + y
yFunc = lambda x,y,t: x**2 - x*y + t

sFrom, sTo = -0.45, -0.35
scaleRes = 0.0001
shapeScale = 0.7

# Initialising and configuring root window
root = Tk()
root.title("Chaos Art Generator")
root.rowconfigure(0, weight=1)
root.rowconfigure(10, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(10, weight=1)

# Initialising and placing image generator
cg = ChaosGenerator(root, 
    width=2000, height=1800, 
    scale=shapeScale, 
    xOffset=0.75, yOffset=0.5,
    xFunc=xFunc, yFunc=yFunc
)
cg.f.grid(row=2,column=1, columnspan=5, sticky="NSEW")

# Initialising and placing slider to change t value
s = Scale(
    root, 
    from_ = sFrom, 
    to = sTo, 
    orient = HORIZONTAL, 
    resolution=scaleRes,
    sliderlength=80)
sVal = None
s.set(sTo + (sFrom - sTo)/2)
s.grid(row=3, column=1, columnspan=5, sticky="NSEW")

# binding keyboard shortcuts for adjusting t value
root.bind("d", lambda e: s.set(s.get()-scaleRes*100))
root.bind("f", lambda e: s.set(s.get()+scaleRes*100))
root.bind("g", lambda e: s.set(s.get()-scaleRes*10))
root.bind("h", lambda e: s.set(s.get()+scaleRes*10))
root.bind("j", lambda e: s.set(s.get()-scaleRes))
root.bind("k", lambda e: s.set(s.get()+scaleRes))

def saveImage():
    img = cg.baseImage
    fileName = simpledialog.askstring("Save Image", "file name: ")
    fileName = f"./output/{fileName}.png"
    print(f"file saved to {fileName}.png")
    print(fileName)
    img.save(fileName,"PNG")

# Info along top, and button to save image
xFuncText = inspect.getsource(xFunc).split(":")[1].rstrip("\n")
yFuncText = inspect.getsource(yFunc).split(":")[1].rstrip("\n")
Label(root,text=f"{cg.numPoints:,} points"
    ).grid(row=1, column=1, sticky="W")
Label(root,text=f"x' = {xFuncText}"
    ).grid(row=1, column=2)
Label(root,text=f"y' = {yFuncText}"
    ).grid(row=1, column=3)
Button(root, text="Save Image", command=saveImage
    ).grid(row=1, column=5, sticky="E")

def main():
    root.after(10, checkChange)
    root.mainloop()

def checkChange():
    root.after(1, checkChange)
    global sVal
    if sVal != s.get():
        if cg.running != None:
            root.after_cancel(cg.running)
        sVal = s.get()
        cg.updateImagePoints(t=sVal)

if __name__ == "__main__":
    main()
