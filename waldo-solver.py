import numpy
import matplotlib.pyplot as pyplot
from PIL import Image
import time
from functools import reduce
from collections import Counter
import math
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
    return compareTwoImageArrays(imageArray1, imageArray2)

def compareTwoImageArrays(imageArray1, imageArray2):
    if ((len(imageArray1) != len(imageArray2)) or (len(imageArray1[0]) != len(imageArray2[0]))):
        print("error: images not same size")
        return

    totalDifferences = 0
    numPixelsAlike = 0

    for row in range(len(imageArray1)):
        for column in range(len(imageArray1[row])):
            pixel1 = imageArray1[row][column]
            pixel2 = imageArray2[row][column]
            if ((len(pixel1) == 4 and pixel1[3] != 255) or (len(pixel2) == 4 and pixel2[3] != 255)):
                continue
            rDifference = math.pow((int(pixel1[0]) - int(pixel2[0])) / 255, 2)
            gDifference = math.pow((int(pixel1[1]) - int(pixel2[1])) / 255, 2)
            bDifference = math.pow((int(pixel1[2]) - int(pixel2[2])) / 255, 2)
            distance = math.sqrt(rDifference + gDifference + bDifference)
            totalDifferences += distance

            if (distance < 0.1):
            	numPixelsAlike += 1

    #print(counter)
    return numPixelsAlike

def getImageChunkFromImageArray(imageArray, startX, startY, size):
    return imageArray[startX:startX+size, startY:startY+size]

def compareImageToPuzzle(imageFilename, puzzleFilename):
    imageArray = convertImageToArray(imageFilename)
    imageSize = len(imageArray)

    highestLikeness = 0
    lowestRow = 0
    lowestColumn = 0
    
    puzzleArray = convertImageToArray(puzzleFilename)
    for row in range(len(puzzleArray)):
        print(row)
        if (row + imageSize >= len(puzzleArray)):
            break
        
        for column in range(len(puzzleArray[row])):
            if (column + imageSize >= len(puzzleArray[row])):
                continue
            
            puzzleChunk = getImageChunkFromImageArray(puzzleArray, row, column, imageSize)
            likeness = compareTwoImageArrays(imageArray, puzzleChunk)
            if (likeness > highestLikeness):
                highestLikeness = likeness
                lowestRow = row
                lowestColumn = column

    print('(' + str(lowestRow) + ', ' + str(lowestColumn) + ') ' + str(highestLikeness))

def main():
    #print(compareTwoFilesOfSameSize(sys.argv[1], sys.argv[2]))
    compareImageToPuzzle(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
        main()
