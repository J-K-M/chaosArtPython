from PIL import Image, ImageDraw
import numpy as np
import sys, cv2
import cProfile
import threading

# These parameters let you tweak the gif
tMin, tMax = -0.19, -0.14    # the range for the t variable
gifLength = 15              # seconds
pointDepth = 100000        # num of points that are drawn per frame
pointOpacity = 50           # 0-255
resolution = (1200, 1000)   # W, H (in pixels)
center = (0.6, 0.5)         # ratio of W,  ratio of Y
scale = 0.3                 # adjusts size of shape
gifOrVid = "vid"            # output gif or video file (vid, gif, or g&v)
userInput = input("Name for output file: ")
fileName = f"./output/{userInput}"  # name for output file
numOfThreads = 10           # for parallelisation


# Everything beyond here is best untouched
stepSize = (tMax - tMin) / (24 * gifLength)
pFlip = True
actualScale = scale*resolution[1]
xCenter = resolution[0]*center[0]
yCenter = resolution[1]*center[1]

tVal = tMin
tValues = []
while tVal < tMax:
    tValues.append(tVal)
    tVal += stepSize
valsPerRange = len(tValues) // numOfThreads
tSubRanges = []
for i in range(numOfThreads):
    temp = []
    for j in range(valsPerRange):
        temp.append(round(tValues.pop(0), 4))
    tSubRanges.append(temp)
if len(tValues) > 0:
    tSubRanges.append(tValues)


def main():
    print("Rendering Frames...")
    frames = [None for i in range(numOfThreads)]

    threads = []
    for i in range(numOfThreads):
        threads.append(threading.Thread(target=renderSubRange,
            args=(
                tSubRanges[i], 
                i,
                frames
            )
        ))
        threads[-1].start()
    for thread in threads:
        print(thread)

    while threading.active_count() > 1:
        pass
    print("all threads done")

    outputImages = []
    for list in frames:
        for item in list:
            outputImages.append(item)

    print(f"\n{len(outputImages)} frames generated.")
    outputFile(outputImages, gifOrVid, fileName, resolution)

def renderSubRange(TsubRange: list, threadNum: int, frames: list) -> list:
    global pFlip
    threadFrames = []
    for t in TsubRange:
        if threadNum == 0:
            percentDone = int(
                ( (t-TsubRange[0]) 
                / (TsubRange[-1]-TsubRange[0])
                ) * 100)
            pFlip = p10print(percentDone, pFlip)

        img = Image.new("RGB", resolution, (10,10,12))
        draw = ImageDraw.Draw(img, mode="RGBA")

        x, y = t, t
        for p in range(pointDepth):
            if x > resolution[0] or y > resolution[1]:
                continue

            try:
                nx = -x**2 -t**2 + x*t - y*t - x
                ny = -x**2 -t**2 + x*t - x - y
            except OverflowError:
                pass

            x, y = nx, ny
            draw.point(
                (
                    x*actualScale + xCenter,
                    y*actualScale + yCenter
                ),
                fill=(255,255,255,pointOpacity)
            )

        threadFrames.append(img)

    print(f"Thread: {threadNum} done.")
    frames[threadNum] = threadFrames

def p10print(p, f):
    if p % 10 == 0:
        if f:
            sys.stdout.write(f"\n{p:3}% ")
            sys.stdout.flush()
            return False
        else:
            return True
    sys.stdout.write(".")
    sys.stdout.flush()

def outputFile(frames, gifOrVid, fileName, resolution):
    if gifOrVid == "gif" or gifOrVid == "g&v":
        print("Saving gif...")
        frames[0].save(
            f"{fileName}.gif",
            save_all = True, 
            append_images = frames[1:], 
            optimize = False, 
            duration = 1000/24, 
            loop = 0
        )
    elif gifOrVid == "vid" or gifOrVid == "g&v":
        print("Saving video...")
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        video = cv2.VideoWriter(f"{fileName}.avi", fourcc, 24, resolution)
        vidFrames = []
        for frame in frames:
            vidFrames.append(np.array(frame))
        for frame in vidFrames:
            video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        video.release()
    else:
        print("gifOrVid value invalid")

if __name__ == "__main__":
    cProfile.run("main()")
    # main()