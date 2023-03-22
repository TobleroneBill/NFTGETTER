# Applies a piece of shit to the image at a random location and scale
# Has functions to:
#   convert the images to jpegs
#   them into clean 250x250 pics
#   List dimensions of stuff
#   Within a directory:
#       Add a picture of a shit to all found images
#       Add a your own image to all found images

import datetime
import os
import random
import sys
import time

import PIL
from PIL import Image
import numpy as np

np.set_printoptions(threshold=sys.maxsize)


# Turn everything in given directory to a jpg (used to counter an issue with color depth)
def Convert2JPG(_Directory):
    count = 1
    directory = _Directory
    imgList = os.listdir(directory)

    if not os.path.exists(f'{directory}\\JPEG'):
        print(f'making folder at:\n {directory}\\JPEG')
        os.mkdir(f'{directory}\\JPEG')

    for i, pic in enumerate(imgList):
        if '.png' in pic:  # only effects pngs
            try:
                with Image.open(f'{directory}\\{pic}') as p:
                    print(f'Converting: {pic}')
                    p = p.convert('RGB')
                    p.save(f'{directory}\\JPEG\\{count}.jpg')
                    count += 1
            except PIL.UnidentifiedImageError:
                print(f'File data Corrupted. Skipping {pic}')
                continue


# set everything to Given Width and height
def ResizePics(_Directory, width, height):
    directory = _Directory
    imglist = os.listdir(directory)
    for pic in imglist:
        if '.png' in pic:  # only effects pngs
            print(f'{directory}\\{pic}')
            try:
                with Image.open(f'{directory}\\{pic}') as img:
                    resized = img.resize((width, height))
                    resized.save(f'{directory}\\{pic}')
                    print(f'resized {pic}')
            except PIL.UnidentifiedImageError:
                print(f'File data Corrupted. Skipping {pic}')
                continue


def Resize(_imgPath, width, height):
    pic = _imgPath
    try:
        with Image.open(pic) as img:
            resized = img.resize((width, height))
            resized.save(pic)
            print(f'resized {pic}')
    except:
        print(f'File data courrupted or invalid. Cannot Resize {pic}')


# mass check jpg collection dimensions
def PrintDetails(_Directory):
    directory = _Directory
    lol = os.listdir(directory)
    for pic in lol:
        img = Image.open(f'{directory}\\{pic}')
        print(img.size)


# add shit randomly to each pic in location
def Shit(_Directory):
    count = 1
    directory = _Directory
    print(f'Reading from: {directory}')
    random.seed(datetime.datetime.now().second)
    imglist = os.listdir(directory)

    # make dir to store new images
    if not os.path.exists(f'{directory}\\shitpics'):
        print(f'Making shitty folder at:\n {directory}\\shitpics')
        os.mkdir(f'{directory}\\shitpics')

    for i, pic in enumerate(imglist):
        if os.path.isdir(pic) or pic.__contains__('.py'):  # only effects pngs
            continue
        else:
            print(f'/______________________________________/{pic}/______________________________________/')
            # load the images
            print(f'Loading image: {directory}\\{pic}')

            try:
                NFTimg = Image.open(f'{directory}\\{pic}')
            except:
                print(f'File data Corrupted or invalid. Skipping {pic}')
                continue

            print(f'Loading poop image')
            shtimg = Image.open('Shit.png')  # should be saved where this .py file is
            # apply rotations and scaling
            print(f'transforming poop image')
            shtimg = shtimg.rotate(random.randint(0, 359))
            shtimg = shtimg.resize((random.randint(50, 100), random.randint(50, 100)))
            print(shtimg.size)
            xpos = random.randint(10, (NFTimg.size[0])-shtimg.size[0])
            ypos = random.randint(10, (NFTimg.size[1])-shtimg.size[1])
            # paste the shit on at a random location. uses itself as a mask to keep transparency
            NFTimg.paste(shtimg, (xpos,ypos), shtimg)
            # folder for these shitty fucking images
            print(f'Saving Result')
            NFTimg.save(f'{directory}\\shitpics\\{count}.png')
            count += 1


# can imagine this being used for a watermark I guess
def ApplyImageToDir(_Directory, image, xPos, yPos, Rotation=None, transparency=True, delay=0.1):
    count = 1
    directory = _Directory
    imglist = os.listdir(_Directory)
    random.seed(datetime.datetime.now().second)

    # make dir to store new images
    if not os.path.exists(f'{directory}\\Updated'):
        os.mkdir(f'{directory}\\Updated')

    for i, pic in enumerate(imglist):
        # For somereason imglist contains the actual directory in the list (WIERD)
        if '.' not in pic:
            continue
        print(f'/______________________________________/{pic}/______________________________________/')
        print('Loading Images')
        # Load the paste image
        try:
            PasteImg = Image.open(image)  # image needs to be a string of the location
        except:
            print(f'Paste image data corrupted or invalid. Skipping {image}')
            print('Get a proper data file and use that :/')
            break

        # load the directory image
        try:
            dirImg = Image.open(f'{directory}\\{pic}')
        except:
            print(f'image data corrupted or invalid. Skipping {pic}')
            continue

        # apply rotations if given
        if Rotation is not None:
            if Rotation.lower() == 'random':
                PasteImg = PasteImg.rotate(random.randint(0, 359))
            else:
                print('Applying Rotation')
                # apply rotations if given
                PasteImg = PasteImg.rotate(Rotation)

        print('Pasting')
        # paste the given image with transparancey
        if transparency is True:
            dirImg.paste(PasteImg, (xPos, yPos), PasteImg)
        else:
            dirImg.paste(PasteImg, (xPos, yPos))
        print('Saving')
        # folder for these shitty fucking images
        dirImg = dirImg.convert('RGB')
        dirImg.save(f'{directory}\\Updated\\{count}.jpg')
        time.sleep(delay)  # Delay can be changed, because this runs so fast that sometimes it crashes lol
        count += 1


# What most people will use lol
def ShitAllOver(NFTDir, resizeW, resizeH):
    print('######################################## Formatting Images ########################################')
    Convert2JPG(NFTDir)
    print('######################################## Resizing ########################################')
    ResizePics(NFTDir, resizeW, resizeH)
    print('######################################## SHITTING ########################################')
    Shit(NFTDir)


if __name__ == '__main__':
    # Make pngs good 1ST
    Shit(r'C:\Users\JOE\Desktop\Projects\PythonSuicide\NFTs\2001_Sotschi')
