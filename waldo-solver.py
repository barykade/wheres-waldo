import numpy
import matplotlib.pyplot as pyplot
from PIL import Image
import time
from functools import reduce
from collections import Counter
import sys
import os

def convertImageToArray(filename):
    imageFilePath = 'images/' + filename
    i = Image.open(imageFilePath)
    imageArray = numpy.asarray(i)
    return imageArray

def writeArrayToFile(imageFilename):
    imageFilenameNoExt = os.path.splitext(imageFilename)[0]
    writeFile = open('images/' + imageFilenameNoExt + '.txt','a')
    writeFile.write(str(convertImageToArray(imageFilename).tolist()))

def compareTwoFilesOfSameSize(file1, file2):
    imageArray1 = convertImageToArray(file1)
    imageArray2 = convertImageToArray(file2)

    if ((len(imageArray1) != len(imageArray2)) or (len(imageArray1[0]) != len(imageArray2[0]))):
        print("error: images not same size")
        return

    counter = 0
    for row in range(len(imageArray1)):
        for column in range(len(imageArray1[row])):
            pixel1 = imageArray1[row][column]
            pixel2 = imageArray2[row][column]
            if (pixel1[3] != 255 or pixel2[3] != 255):
                continue
            rCloseness = abs(int(pixel1[0]) - int(pixel2[0])) / 255
            gCloseness = abs(int(pixel1[1]) - int(pixel2[1])) / 255
            bCloseness = abs(int(pixel1[2]) - int(pixel2[2])) / 255
            counter += 1 / (rCloseness + gCloseness + bCloseness)

    print(counter)

def main():
    imageFilename = sys.argv[1]
    imageFilename2 = sys.argv[2]
    compareTwoFilesOfSameSize(imageFilename, imageFilename2)

if __name__ == '__main__':
        main()