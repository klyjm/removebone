import math
import os
import cv2
import numpy as np


def expand(x, y, center):
    global size
    if 0 <= x < size[0] and 0 <= y < size[1]:
        global seeddata
        global seedindex
        global flag
        global dataarray
        if flag[x][y] == 0 and abs(center - dataarray[x][y]) < 10:
            seeddata.append(dataarray[x][y])
            seedindex.append([x, y])
            flag[x][y] = 1


imgpath = input('图像路径：')
outputpath = input('输出路径：')
outputpath = outputpath + '\\' + os.path.basename(imgpath)
if not os.path.exists(outputpath):
    os.makedirs(outputpath)
for file in os.listdir(imgpath):
    dataarray = cv2.imread(imgpath + '\\' + file, cv2.IMREAD_GRAYSCALE)
    dataarray = dataarray.astype('int16')
    size = [np.size(dataarray, 0), np.size(dataarray, 1)]
    maxdata = np.max(dataarray).tolist()
    flag = np.zeros((size[0], size[1]))
    # while maxdata > 235:
    maxindex = list(np.where(dataarray == maxdata))
    seeddata = []
    seedindex = []
    for i in range(len(maxindex[1])):
        seeddata.append(maxdata)
        seedindex.append([maxindex[0][i], maxindex[1][i]])
    while len(seeddata) > 0:
        center = seeddata[0]
        flag[seedindex[0][0]][seedindex[0][1]] = 1
        expand(seedindex[0][0] - 1, seedindex[0][1] - 1, center)
        expand(seedindex[0][0] - 1, seedindex[0][1], center)
        expand(seedindex[0][0] - 1, seedindex[0][1] + 1, center)
        expand(seedindex[0][0], seedindex[0][1] - 1, center)
        expand(seedindex[0][0], seedindex[0][1] + 1, center)
        expand(seedindex[0][0] + 1, seedindex[0][1] - 1, center)
        expand(seedindex[0][0] + 1, seedindex[0][1], center)
        expand(seedindex[0][0] + 1, seedindex[0][1] + 1, center)
        seeddata.pop(0)
        seedindex.pop(0)
    for i in range(size[0]):
        for j in range(size[1]):
            if flag[i][j] == 1:
                dataarray[i][j] = 0
    maxdata = np.max(dataarray).tolist()
    dataarray = dataarray.astype('uint8')
    cv2.imwrite(outputpath + '\\' + os.path.basename(imgpath + '\\' + file), dataarray)
