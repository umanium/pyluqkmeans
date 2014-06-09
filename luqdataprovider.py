# data provider for data

import sys, math, random
import matplotlib.pyplot as plt, matplotlib.image as mpimg

def provideRandomData(dataCount, dataLen, minVal, maxVal):
    random.seed()
    result = []
    for i in range(dataCount):
        temp_array = []
    for j in range(dataLen):
        init_num = random.random()
        final_num = minVal + (init_num * (maxVal-minVal))
        final_num = math.floor(final_num * 100)/100
        temp_array.append(final_num)
        result.append(temp_array)
    return result

def provideImageData(fileName):
  
    img = mpimg.imread(fileName)

    linearizedImg = linearizeImage(img)
    #normalizedImg = normalizeImage(linearizedImg)

    #plt.imshow(img)

    return linearizedImg

def provideTextData(fileName):
    result = []

    return result

def linearizeImage(imageData):
    result = []

    len1 = 0
    len2 = 0

    for i1 in imageData:
        for i2 in i1:
            len2 = len2 + 1
            result.append(i2)
        len1 = len1 + 1

    len2 = len2 / len1

    return [result, len1, len2]

def normalizeImage(linearizedImageData):
    result = []

    len1 = linearizedImageData[1]
    len2 = linearizedImageData[2]
    imgData = linearizedImageData[0]

    for i1 in range(len1):
        temp_res = []
        for i2 in range(len2):
            idx = (i1*len2)+i2
            temp_res.append(imgData[idx])
        result.append(temp_res)

    return result