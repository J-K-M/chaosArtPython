from tkinter import *
from cg import ChaosGenerator
import cProfile

root = Tk()
root.title("Chaos Art Generator")
root.rowconfigure(0, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(2, weight=1)

cg = ChaosGenerator(root)
cg.f.grid(row=1,column=1)

scaleRes = 0.0001
s = Scale(
    root, 
    from_ = -0.4, 
    to = 0.1 , 
    orient = HORIZONTAL, 
    resolution=scaleRes, 
    sliderlength=100
)
s.grid(row=2, column=1, sticky="EW")
s.set(-0.17)
root.bind("j", lambda e: s.set(s.get()-scaleRes))
root.bind("k", lambda e: s.set(s.get()+scaleRes))
root.bind("g", lambda e: s.set(s.get()-scaleRes*10))
root.bind("h", lambda e: s.set(s.get()+scaleRes*10))
root.bind("d", lambda e: s.set(s.get()-scaleRes*100))
root.bind("f", lambda e: s.set(s.get()+scaleRes*100))
root.bind("<Escape>", lambda e: root.destroy())
sVal = s.get()

def main():
    root.after(1, checkChange)
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
    # cProfile.run("main()")
    main()