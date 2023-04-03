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
import pathlib
import random
import sys
import time

import oschmod  # I'm having wierd file permmission issues
import PIL
from PIL import Image
import numpy as np

np.set_printoptions(threshold=sys.maxsize)


# Turn everything in given directory to a jpg (used to counter an issue with color depth)
# InPlace, changes the original images
# DeleteFailure deletes files that are perieved as corrupted (anything that throws an error)
def Convert2JPG(_Directory,InPlace=False,DeleteFailure=False):
    count = 1
    directory = pathlib.Path(_Directory)
    imgList = os.listdir(directory)
    savepath = f'{directory}\JPEG'

    # Make a new folder
    if not InPlace:
        if not os.path.exists(savepath):
            print(f'making folder at:\n {savepath}')
            os.mkdir(savepath)

        for i, pic in enumerate(imgList):
            # if listing is a directory, or anything else that isnt a file, skip
            if not os.path.isfile(str(directory/pic)):
                print(f'{pic} is not a file')
                continue

            #if '.png' in pic or '.jpg':  # ATM focused on png and JPEG, could make this general, but idk
            try:
                print(f'converting {pic}')
                p = Image.open(f'{directory}\{pic}','r')
                RGBp = p.convert('RGB')
                # 100% a safe path
                saveLoc = savepath
                saveLoc = saveLoc + f'\{i}.jpg'
                RGBp.save(saveLoc)
                count += 1

            except PIL.UnidentifiedImageError:
                print(f'File data Corrupted. Skipping {pic}')
                if DeleteFailure:
                    print(f'Deleting {pic}')
                    os.remove(pathlib.Path.joinpath(directory / pic))
                continue
    else:   # Use current folder
        for i, pic in enumerate(imgList):
            # if listing is a directory, or anything else that isnt a file, skip
            if not os.path.isfile(str(directory / pic)):
                print(f'{pic} is not a file')
                continue
            try:
                print(f'converting {pic}')
                p = Image.open(f'{directory}\{pic}', 'r')
                RGBp = p.convert('RGB')
                # 100% a safe path
                RGBp.save(pathlib.Path.joinpath(directory/pic))
                count += 1

            except PIL.UnidentifiedImageError:
                print(f'File data Corrupted. Skipping {pic}')
                if DeleteFailure:
                    p.close()
                    print(f'Deleting {pic}')
                    os.remove(pathlib.Path.joinpath(directory / pic))
                continue

# set everything to Given Width and height in a directory
def ResizePics(_Directory, width, height ,DeleteFailure=False):
    directory = pathlib.Path(_Directory)
    imglist = os.listdir(directory)

    for pic in imglist:
        if not os.path.isfile(str(directory/pic)):
            print(f'{pic} is not a file')
            continue

        print(f'{directory}\\{pic}')
        try:
            with Image.open(f'{directory}\\{pic}') as img:
                resized = img.resize((width, height))
                resized = resized.convert(mode='RGB')
                resized.save(f'{directory}\\{pic}')
                print(f'resized {pic}')

        except PIL.UnidentifiedImageError:
            print(f'File data Corrupted. Skipping {pic}')
            if DeleteFailure:
                print(f'Deleting {pic}')
                os.remove(pathlib.Path.joinpath(directory/pic))
            continue


# Resizes in place
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
def PrintDimensions(_Directory):
    directory = _Directory
    lol = os.listdir(directory)
    for pic in lol:
        img = Image.open(f'{directory}\\{pic}')
        print(f'{pic}: {img.size}')


# add shit randomly to each pic in directory
def Shit(_Directory,InPlace=False,DeleteFailure=False):
    count = 1
    directory = pathlib.Path(_Directory)
    print(f'Reading from: {directory}')
    random.seed(datetime.datetime.now().second)
    imglist = os.listdir(directory)

    # make dir to store new images
    if not os.path.exists(f'{directory}\\shitpics') and not InPlace:
        print(f'Making shitty folder at:\n {directory}\\shitpics')
        os.mkdir(f'{directory}\\shitpics')

    for i, pic in enumerate(imglist):
        if not os.path.isfile(str(directory/pic)):  # skip folders
            print(f'{pic} is not a file')
            continue

        print(f'/______________________________________/{pic}/______________________________________/')
        # load the images
        print(f'Loading image: {directory}\\{pic}')

        try:
            NFTimg = Image.open(f'{directory}\\{pic}')
        except:
            print(f'File data Corrupted or invalid. Skipping {pic}')
            if DeleteFailure:
                os.remove(pathlib.Path.joinpath(directory/NFTimg))
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
        if not InPlace:
            NFTimg.save(f'{directory}\\shitpics\\{count}.png')  # save in new folder
        else:
            NFTimg.save(pathlib.Path.joinpath(directory/NFTimg))
        count += 1

    print('FINISHED SHITTING')


# add shits many times
def RepeatShit(_Dir,loops,InPlace=False,DeleteFailure=False):
    count = 0
    directory = pathlib.Path(_Dir)
    print(f'Reading from: {directory}')
    random.seed(datetime.datetime.now().second)
    imglist = os.listdir(directory)

    # make dir to store new images

    if not os.path.exists(f'{directory}\\shitpics') and not InPlace:
        print(f'Making shitty folder at:\n {directory}\\shitpics')
        os.mkdir(f'{directory}\\shitpics')

    for i, pic in enumerate(imglist):
        if not os.path.isfile(str(directory/pic)):  # skip folders
            print(f'{pic} is not a file')
            continue

        print(f'/______________________________________/{pic}/______________________________________/')
        # load the images
        print(f'Loading image: {directory}\\{pic}')

        try:
            NFTimg = Image.open(f'{directory}\\{pic}')
        except:
            print(f'File data Corrupted or invalid. Skipping {pic}')
            if DeleteFailure:
                os.remove(pathlib.Path.joinpath(directory / pic))
            continue

        for i in range(1,loops):
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
    #print('Wrong main')
    Shit(r'Images')
    #Convert2JPG(r'Images',InPlace=True,DeleteFailure=True)
    #ResizePics('Images',500,500)
    #PrintDimensions('Images')
