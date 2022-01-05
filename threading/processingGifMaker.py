from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import sys
from multiprocessing import Pool, set_start_method
import time

# set_start_method("fork") # potentially fixes a bug on macOS

# These parameters let you tweak the gif
tMin, tMax = 0.9, 1.0    # the range for the t variable
gifLength = 2              # seconds
pointDepth = 1000000        # num of points that are drawn per frame
pointOpacity = 40           # 0-255
resolution = (1920, 1080)   # W, H (in pixels)
center = (0.35, 0.7)         # ratio of W,  ratio of H
scale = 0.26                 # adjusts size of shape
gifOrVid = "v"            # output gif or video file (vid, gif, or g&v)
embedFuncs = True           # embed the functions in the top left of the video
numProcesses = 4

xFunc = "y**2 + t**2 - x - t"
yFunc = "-t**2 + x*t + y*t"


# Everything beyond here is best untouched
userInput = input(f"Name for {gifOrVid}: ")
fileName = f"./output/{userInput}"

# Calculating increment value for t to get the right gif length at 24 fps
stepSize = (tMax - tMin) / (24 * gifLength)
# Pre calculating x,y offsets
actualScale = scale*resolution[1]
xCenter = resolution[0]*center[0]
yCenter = resolution[1]*center[1]

tVal = tMin
tValues = []
while tVal < tMax:
    tValues.append(round(tVal,12))
    tVal += stepSize

chunkSize = len(tValues)//numProcesses

tSubRanges = []
for i in range(numProcesses):
    temp = []
    for j in range(chunkSize):
        temp.append(tValues.pop(0))
    tSubRanges.append(temp)
if len(tValues) > 0:
    if len(tValues) > 1:
        tSubRanges.append(tValues)



blankImage = Image.new("RGB", resolution, (10,10,12))
ImageDraw.Draw(blankImage)
if embedFuncs:
    ImageDraw.Draw(blankImage).multiline_text(
        (10,10), 
        text=f"{xFunc}\n{yFunc}",
        font=ImageFont.truetype(
            "Pillow/Tests/fonts/FreeMono.ttf", 
            32
        )
    )

def main():
    pool = Pool(numProcesses)
    print(f"There are {numProcesses} processes.")
    print(f"Each process is rendering ~{len(tSubRanges[0])} frames.")
    print(f"{pointDepth:,} points per frame.")
    startTime = time.time()
    workers = [
        pool.apply_async(
            renderSubRange, 
            args=(tSubRange,i)
        ) for i, tSubRange in enumerate(tSubRanges)
    ]
    results = [w.get() for w in workers]

    outputImages = []
    for list in results:
        for item in list:
            outputImages.append(item)

    timeToComplete = round(time.time()-startTime, 3)
    print(f"\n{len(outputImages)} frames generated in {timeToComplete} seconds.")
    outputFile(outputImages, gifOrVid, fileName, resolution)

def renderSubRange(TsubRange: list, processNum: int) -> list:
        processFrames = []

        x, y = TsubRange[0], TsubRange[0]
        for i, t in enumerate(TsubRange):
            if processNum == 0:
                pDone = ( i/len(TsubRange) )*100
                if pDone% 10 == 0:
                    sys.stdout.write(f"\n~{int(pDone):3}% done.")
                    sys.stdout.flush()
                else:
                    sys.stdout.write(".")
                    sys.stdout.flush()

            img = blankImage.copy()
            draw = ImageDraw.Draw(img, mode="RGBA")

            for p in range(pointDepth):
                if x > resolution[0] or y > resolution[1]:
                    continue

                try:
                    nx = y**2 + t**2 - x - t
                    ny = -t**2 + x*t + y*t
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

            processFrames.append(img)

        return processFrames


def outputFile(frames, gifOrVid, fileName, resolution):
    if "g" in gifOrVid:
        print(f"Saving '{fileName}.gif' ...")
        frames[0].save(
            f"{fileName}.gif",
            save_all = True, 
            append_images = frames[1:], 
            optimize = False, 
            duration = 1000/24, 
            loop = 0
        )
    if "v" in gifOrVid:
        print(f"Saving '{fileName}.mp4' ...")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(f"{fileName}.mp4", fourcc, 24, resolution)
        vidFrames = []
        for frame in frames:
            vidFrames.append(np.array(frame))
        for frame in vidFrames:
            video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        video.release()
    else:
        print(
        "gifOrVid value invalid. Should contain 'g' and/or 'v' characters."
        )
    
    print("Done.")

if __name__ == "__main__":
    main()
