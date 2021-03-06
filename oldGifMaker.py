from PIL import Image, ImageDraw
import numpy as np
import sys, cv2


def main():
    # These perameters let you tweak the gif
    tMin, tMax = -0.3, -0.1     # the range for the t variable
    gifLength = 15              # seconds
    pointDepth = 100000         # num of points that are drawn per frame
    pointOpacity = 50           # 0-255
    resolution = (1000, 1000)   # W, H (in pixels)
    center = (0.6, 0.5)         # ratio of W,  ratio of Y
    scale = 0.3                 # adjusts size of shape
    gifOrVid = "vid"            # output gif or video file (vid, gif, or g&v)
    fileName = "./output/test1"  # name for output file

    # Everything beyond here is best untouched
    stepSize = (tMax - tMin) / (24 * gifLength)
    frames = []
    t = tMin
    pFlip = True

    actualScale = scale*resolution[1]
    xCenter = resolution[0]*center[0]
    yCenter = resolution[1]*center[1]

    print("Rendering Frames...")
    while t < tMax:
        t += stepSize
        percentDone = int((t+abs(tMin))/(tMax+abs(tMin)) * 100)
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
                    y*actualScale + yCenter,
                ),
                fill=(255,255,255,pointOpacity)
            )

        frames.append(img)

    print(f"\n{len(frames)} frames generated.")
    outputFile(frames, gifOrVid, fileName, resolution)
    print("Done.")

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
    main()
