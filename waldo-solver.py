import numpy
import matplotlib.pyplot as pyplot
from PIL import Image
import time
from functools import reduce
from collections import Counter

def convertImageToArray(filename):
    imageFilePath = 'images/' + filename + '.png'
    i = Image.open(imageFilePath)
    imageArray = numpy.asarray(i)
    return imageArray

def writeArrayToFile(imageFilename):
    writeFile = open('images/' + imageFilename + '.txt','a')
    writeFile.write(str(convertImageToArray(imageFilename).tolist()))
