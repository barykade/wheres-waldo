import numpy
import matplotlib.pyplot as pyplot
from PIL import Image
import time
from functools import reduce
from collections import Counter

def createExamples():
    numberArrayExamples = open('numArEx.txt','a')
    numbersWeHave = range(0,10)
    versionsWeHave = range(1,10)

    for eachNum in numbersWeHave:
        for eachVersion in versionsWeHave:
            imageFilePath = 'images/numbers/' + str(eachNum) + '.' + str(eachVersion) + '.png'
            i = Image.open(imageFilePath)
            imageArray = numpy.asarray(i)
            imageArray1 = str(imageArray.tolist())

            lineToWrite = str(eachNum) + '::' + imageArray1 + '\n'
            numberArrayExamples.write(lineToWrite)
    

def threshold(imageArray):
    balanceArray = []
    newArray = imageArray
    newArray.flags.writeable = True

    for eachRow in imageArray:
        for eachPixel in eachRow:
            avgNum = reduce(lambda x, y: x+y, eachPixel[:3])/len(eachPixel[:3])
            balanceArray.append(avgNum)

    balance = reduce(lambda x, y: x+y, balanceArray)/len(balanceArray)
    for eachRow in newArray:
        for eachPixel in eachRow:
            if reduce(lambda x, y: x+y, eachPixel[:3])/len(eachPixel[:3]) > balance:
                eachPixel[0] = 255
                eachPixel[1] = 255
                eachPixel[2] = 255
                eachPixel[3] = 255
            else:
                eachPixel[0] = 0
                eachPixel[1] = 0
                eachPixel[2] = 0
                eachPixel[3] = 255

    return newArray

def whatNumIsThis(filePath):
    matchedArray = []
    loadExamples = open('numArEx.txt','r').read()
    loadExamples = loadExamples.split('\n')

    i = Image.open(filePath)
    imageArray = numpy.asarray(i)
    imageArray1 = imageArray.tolist()

    inQuestion = str(imageArray1)

    for eachExample in loadExamples:
        if len(eachExample) > 3:
            splitExample = eachExample.split('::')
            currentNum = splitExample[0]
            currentArray = splitExample[1]

            eachPixelExample = currentArray.split('],')
            eachPixelInQuestion = inQuestion.split('],')

            x = 0

            while x < len(eachPixelExample):
                if eachPixelExample[x] == eachPixelInQuestion[x]:
                    matchedArray.append(int(currentNum))

                x += 1

    x = Counter(matchedArray)
    print(x)

''' 
i1 = Image.open('images/numbers/0.1.png')
imageArray1 = numpy.asarray(i1)

i2 = Image.open('images/numbers/y0.3.png')
imageArray2 = numpy.asarray(i2)

i3 = Image.open('images/numbers/y0.4.png')
imageArray3 = numpy.asarray(i3)

i4 = Image.open('images/numbers/y0.5.png')
imageArray4 = numpy.asarray(i4)
'''
'''
threshold(imageArray2)
threshold(imageArray3)
threshold(imageArray4)

fig = pyplot.figure()
ax1 = pyplot.subplot2grid((8,6), (0,0), rowspan=4, colspan=3)
ax2 = pyplot.subplot2grid((8,6), (4,0), rowspan=4, colspan=3)
ax3 = pyplot.subplot2grid((8,6), (0,3), rowspan=4, colspan=3)
ax4 = pyplot.subplot2grid((8,6), (4,3), rowspan=4, colspan=3)

ax1.imshow(imageArray1)
ax2.imshow(imageArray2)
ax3.imshow(imageArray3)
ax4.imshow(imageArray4)

pyplot.show()
'''
#pyplot.imshow(imageArray)
#pyplot.show()
