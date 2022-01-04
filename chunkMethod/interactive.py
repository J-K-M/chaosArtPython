from tkinter import *
from tkinter import simpledialog
from cg import ChaosGenerator

# Initialising and configuring root window
root = Tk()
root.title("Chaos Art Generator")
root.rowconfigure(0, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(3, weight=1)

# Initialising and placing image generator
cg = ChaosGenerator(root, width=2000, height=1500, scale=0.3, xOffset=0.6)
cg.f.grid(row=2,column=1, columnspan=5)

# Initialising and placing slider to change t value
scaleRes = 0.0001
s = Scale(
    root, 
    from_ = -0.4, 
    to = 0.1, 
    orient = HORIZONTAL, 
    resolution=scaleRes,
    sliderlength=80
)
s.grid(row=3, column=1, columnspan=5, sticky="NSEW")
# binding keyboard shortcuts for adjusting t value
root.bind("d", lambda e: s.set(s.get()-scaleRes*100))
root.bind("f", lambda e: s.set(s.get()+scaleRes*100))
root.bind("g", lambda e: s.set(s.get()-scaleRes*10))
root.bind("h", lambda e: s.set(s.get()+scaleRes*10))
root.bind("j", lambda e: s.set(s.get()-scaleRes))
root.bind("k", lambda e: s.set(s.get()+scaleRes))
sVal = s.get()

def saveImage():
    img = cg.baseImage
    fileName = simpledialog.askstring("Save Image", "file name: ")
    fileName = f"./images/{fileName}.png"
    print(f"file saved to {fileName}.png")
    print(fileName)
    img.save(fileName,"PNG")


Label(root,text=f"{cg.numPoints:,} points").grid(row=1, column=1)
Button(root, text="Save Image", command=saveImage).grid(row=1, column=5)

def main():
    root.after(1, checkChange)
    root.after(10, lambda: s.set(-0.17))
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