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

def convertArrayToImage(array):
	img = Image.fromarray(array, 'RGB')
	return img

def writeArrayToFile(imageFilename):
	imageFilenameNoExt = os.path.splitext(imageFilename)[0]
	writeFile = open('images/' + imageFilenameNoExt + '.txt','a')
	writeFile.write(str(convertImageToArray(imageFilename).tolist()))

def compareTwoFilesOfSameSize(file1, file2):
	imageArray1 = convertImageToArray(file1)
	imageArray2 = convertImageToArray(file2)
	return compareTwoImageArrays(imageArray1, imageArray2)

def getAveragePixelOfImageArray(imageArray):
	averageR = 0
	averageG = 0
	averageB = 0
	for row in range(len(imageArray)):
		for column in range(len(imageArray[row])):
			pixel = imageArray[row][column]
			averageR += pixel[0]
			averageG += pixel[1]
			averageB += pixel[2]

	averageR /= ((row+1) * (column+1))
	averageG /= ((row+1) * (column+1))
	averageB /= ((row+1) * (column+1))

	return [int(averageR), int(averageG), int(averageB)]

def resizeImageArray(imageArray, increment):
	
	newImageArray = numpy.empty([int(len(imageArray) / increment), int(len(imageArray[0]) / increment), 3])
	newImageArray.setflags(write=1)

	for row in range(0, len(imageArray), increment):
		for column in range(0, len(imageArray[row]), increment):
			averagePixel = getAveragePixelOfImageArray(getImageChunkFromImageArray(imageArray, row, column, increment))
			newImageArray[int(row / increment), int(column / increment)] = averagePixel

	return newImageArray

def compareTwoImageArrays(imageArray1, imageArray2):
	if ((len(imageArray1) != len(imageArray2)) or (len(imageArray1[0]) != len(imageArray2[0]))):
		print("error: images not same size")
		return

	totalLikeness = 0
	totalPixels = 0
	numPixelsAlike = 0

	for row in range(len(imageArray1)):
		for column in range(len(imageArray1[row])):
			pixel1 = imageArray1[row][column]
			pixel2 = imageArray2[row][column]
			if ((len(pixel1) == 4 and pixel1[3] != 255) or (len(pixel2) == 4 and pixel2[3] != 255)):
				continue

			totalPixels += 1

			rDifference = math.pow((int(pixel1[0]) - int(pixel2[0])) / 255, 2)
			gDifference = math.pow((int(pixel1[1]) - int(pixel2[1])) / 255, 2)
			bDifference = math.pow((int(pixel1[2]) - int(pixel2[2])) / 255, 2)
			distance = math.sqrt(rDifference + gDifference + bDifference)

			if (distance < 0.3):
				numPixelsAlike += 1
				totalLikeness += distance

	#print(totalLikeness)
	return numPixelsAlike / totalPixels

def getImageChunkFromImageArray(imageArray, startX, startY, size):
	return imageArray[startX:startX+size, startY:startY+size]

def compareImageToPuzzle(imageFilename, puzzleFilename):
	compareImageArrayToPuzzleArray(convertImageToArray(imageFilename), convertImageToArray(puzzleFilename))

def getAllPossibleContendersForComparison(imageArray, puzzleArray, threshold):
	imageSize = len(imageArray)

	possibleCandidates = []
	counter = 0
	
	for row in range(0, len(puzzleArray), 1):
		if (row + imageSize >= len(puzzleArray)):
			break
		
		for column in range(0, len(puzzleArray[row]), 1):
			if (column + imageSize >= len(puzzleArray[row])):
				continue
			
			puzzleChunk = getImageChunkFromImageArray(puzzleArray, row, column, imageSize)
			likeness = compareTwoImageArrays(imageArray, puzzleChunk)
			if (likeness > threshold):
				possibleCandidates.append([row, column])

	return possibleCandidates

def getLikliestCandidateForComparisonWithContenders(imageArray, puzzleArray, increment, contenders):
	imageSize = len(imageArray)
	highestLikeness = 0
	lowestRow = 0
	lowestColumn = 0

	for contender in contenders:
		contenderRow = contender[0]
		contenderColumn = contender[1]

		for row in range(contenderRow * increment, (contenderRow + 1) * increment):
			for column in range(contenderColumn * increment, (contenderColumn + 1) * increment):

				puzzleChunk = getImageChunkFromImageArray(puzzleArray, row, column, imageSize)
				likeness = compareTwoImageArrays(imageArray, puzzleChunk)
				if (likeness > highestLikeness):
					highestLikeness = likeness
					lowestRow = row
					lowestColumn = column

	print('(' + str(lowestRow) + ', ' + str(lowestColumn) + ')' + str(highestLikeness))

def addBorderAroundWaldo(puzzleArray, rowStart, columnStart, size):

	puzzleArray.setflags(write=1)

	# Add green border around box
	green3D = [0, 255, 0]
	green4D = [0, 255, 0, 255]

	for x in range(size):
		#top
		if len(puzzleArray[rowStart, columnStart + x]) == 3:
			puzzleArray[rowStart, columnStart + x] = green3D
		else:
			puzzleArray[rowStart, columnStart + x] = green4D

		#left
		if len(puzzleArray[rowStart + x, columnStart]) == 3:
			puzzleArray[rowStart + x, columnStart] = green3D
		else:
			puzzleArray[rowStart + x, columnStart] = green4D

		#bottom
		if len(puzzleArray[rowStart + size, columnStart + x]) == 3:
			puzzleArray[rowStart + size, columnStart + x] = green3D
		else:
			puzzleArray[rowStart + size, columnStart + x] = green4D

		#right
		if len(puzzleArray[rowStart + x, columnStart + size]) == 3:
			puzzleArray[rowStart + x, columnStart + size] = green3D
		else:
			puzzleArray[rowStart + x, columnStart + size] = green4D

	img = convertArrayToImage(puzzleArray)
	img.show()

def main():
	#print(compareTwoFilesOfSameSize(sys.argv[1], sys.argv[2]))
	#compareImageToPuzzle(sys.argv[1], sys.argv[2])
	imageArrayFull = convertImageToArray(sys.argv[1])
	puzzleArrayFull = convertImageToArray(sys.argv[2])

	imageArrayTmp = resizeImageArray(imageArrayFull, 5).astype(int)
	puzzleArrayTmp = resizeImageArray(puzzleArrayFull, 5).astype(int)
	contenders = getAllPossibleContendersForComparison(imageArrayTmp, puzzleArrayTmp, 0.3)

	getLikliestCandidateForComparisonWithContenders(imageArrayFull, puzzleArrayFull, 5, contenders)

	#pyplot.imshow(convertImageToArray(sys.argv[2]))
	#pyplot.show()

	#img = convertArrayToImage(puzzleArray)
	#img.show()

if __name__ == '__main__':
		main()
