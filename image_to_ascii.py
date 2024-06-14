from PIL import Image, ImageDraw,ImageFont
import imageio.v2 as imageio
import numpy as np
import os
from math import ceil



resolution = (1920, 1080)
greyScale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
font = ImageFont.truetype("fonts/Input.ttf", size=30)



def deleteFiles():
    try:
        lis = os.listdir("textfiles")
        for entry in lis:
            os.remove(f"textfiles/{entry}")
        lis = os.listdir("images")
        for entry in lis:
            os.remove(f"images/{entry}")
    except Exception as e:
        print(f"An error has occured in deleteFiles : {e}")
        exit(0)
    except KeyboardInterrupt:
        print("Program terminated by user!")
        exit(0)



def getParams(lines):
    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = 20

    tallest_line = max(lines, key=lambda line: font.getbbox(line)[3])
    max_line_height = font_points_to_pixels(font.getbbox(tallest_line)[3])
    realistic_line_height = max_line_height * 0.8
    image_height = int(ceil(realistic_line_height * len(lines) + 2 * margin_pixels))

    widest_line = max(lines, key=lambda s: font.getbbox(s)[2])
    max_line_width = font_points_to_pixels(font.getbbox(widest_line)[2])
    image_width = int(ceil(max_line_width + (2.0 * margin_pixels) - 500))

    return (image_width, image_height, realistic_line_height)



def turnImageToGIF(frames):
    try:
        with open(f"textfiles/0.txt", "r") as text:
            lines = tuple(line.rstrip() for line in text.readlines())
            ass = getParams(lines)
        for k in range(frames):
            with open(f"textfiles/{k}.txt", "r") as text:
                lines = text.readlines()
                img = Image.new('L',(ass[0], ass[1]), 0)
                d = ImageDraw.Draw(img)
                for w, line in enumerate(lines):
                    d.text((20, 20 + (w*ass[2])), line, fill=255, font = font)
                img = img.resize(resolution)
                img.save(f"images/{k}.png")
                print("Turned text to image")
        gifarray=[]
        for k in range(frames):
            gifarray.append(imageio.imread(f"images/{k}.png"))
        imageio.mimsave('gifs/out.gif', gifarray)
        deleteFiles()
        print("done")
    except Exception as e:
        print(f"An error has occured in turnImageToGIF : {e}")
        deleteFiles()
        exit(0)
    except KeyboardInterrupt:
        print("Program terminated by user!")
        deleteFiles()
        exit(0)



def turnGIFToImage(frames):
    try:
        with Image.open("gifs/input.gif") as roger:
            if roger.n_frames <= frames:
                print("Too many frames!")
                exit(0)
            else:
                for k in range(frames):
                    roger.seek(roger.n_frames // frames*k)
                    roger.save(f"images/{k}.png")
        print("Turned to Images")
    except Exception as e:
        print(f"An error has occured in turnGIFToImage : {e}")
        deleteFiles()
        exit(0)
    except KeyboardInterrupt:
        print("Program terminated by user!")
        deleteFiles()
        exit(0)



def asciiTheImage(columns=125, scale=1, frames=15):
    finalArray=[]
    try:
        for k in range(frames):
            with Image.open(f"images/{k}.png").convert("L") as roger:
                width, height = roger.size[0], roger.size[1]
                tileWidth = width/columns
                tileHeight = tileWidth/scale
                rows = int(height/tileHeight)

                if columns > width or rows > height:
                    print("Image too small for specified cols!")
                    exit(0)
                    
                asciiImage = []
                for j in range(rows):
                    y1 = int(j*tileHeight)
                    y2 = int((j+1)*tileHeight)
                    if j == rows-1:
                        y2 = height
                    asciiImage.append("")
                    for i in range(columns):
                        x1 = int(i*tileWidth)
                        x2 = int((i+1)*tileHeight)
                        if i == columns-1:
                            x2 = width
                        croppedImage = roger.crop((x1,y1,x2,y2))
                        avgBrightness = int(computeBrightnessAverage(croppedImage))
                        greyScaleValue = greyScale1[int((avgBrightness*69)/255)]
                        asciiImage[j] += greyScaleValue
            finalArray.append(asciiImage)
        return finalArray
    except Exception as e:
        print(f"An error has occured in asciiTheImage : {e}")
        deleteFiles()
        exit(0)
    except KeyboardInterrupt:
        print("Program terminated by user!")
        deleteFiles()
        exit(0)



def computeBrightnessAverage(image):
    try:
        imageArray = np.array(image)
        w,h = imageArray.shape
        return np.average(imageArray.reshape(w*h))
    except Exception as e:
        print(f"An error has occured in computeBrightnessAverage : {e}")
        deleteFiles()
        exit(0)
    except KeyboardInterrupt:
        print("Program terminated by user!")
        deleteFiles()
        exit(0)



def writingFile(finalImages, frames):
    try:
        for k in range(frames):
            with open(f'textfiles/{k}.txt', 'w') as f:
                for row in finalImages[k]:
                    f.write(row + '\n')
            print("done writing the file")
    except Exception as e:
        print(f"An error has occured in writingFile : {e}")
        deleteFiles()
        exit(0)
    except KeyboardInterrupt:
        print("Program terminated by user!")
        deleteFiles()
        exit(0)



if __name__ == "__main__":
    try:
        columns = int(input("Enter the columns : "))
        scale = float(input("Enter the scale : "))
        frames = int(input("Enter the frames : "))
        turnGIFToImage(frames)
        endImages = asciiTheImage(columns, scale, frames)
        writingFile(endImages,frames)
        turnImageToGIF(frames)
    except Exception as e:
        print(f"An error has occured in the main code : {e}")
        deleteFiles()
        exit(0)
    except KeyboardInterrupt:
        print("Program terminated by user!")
        deleteFiles()
        exit(0)
