import SimpleITK as sitk
import os
import cv2
import numpy as np


def expand(x, y, data):
    global shape
    if 0 <= x < shape[0] and 0 <= y < shape[1]:
        global seeddata
        global seedindex
        global flag
        global dataarray
        global mean
        global count
        if flag[x][y] == 0 and abs(data - dataarray[x][y]) < 400 and dataarray[x][y] > 100:
        # if abs(data - dataarray[x][y]) < 5 and dataarray[x][y] > 140:
        #if abs(data - dataarray[x][y]) < 7 and (abs(dataarray[x][y] - mean) < 180 and dataarray[x][y] > 140) and \
                #flag[x][y] == 0:
            # print(str(data))
            # print(str(dataarray[x][y]))
            seeddata.append(dataarray[x][y])
            seedindex.append([x, y])
            flag[x][y] = 1
            count = count + 1
            mean = (mean + dataarray[x][y]) / count
            # dataarray[x][y] = 0


# imgpath = input('图像路径：')
# outputpath = input('输出路径：')
dicompath = 'D:\\CTA\\18 LI_JIU_WEN_CT3-233510\\DUAL_ENERGY_YZXDE_BODYANGIO_BONEREM_(ADUL_20110902_140614_078000\\DE_BODYANGIO_1_0_B30F_A_140KV_0005'
# imgpath = 'D:\\bmp1\\DE_BODYANGIO_1_0_B30F_A_140KV_0005'
outputpath = 'D:\\bmp3'
# outputpath = outputpath + '\\' + os.path.basename(imgpath)
outputpath = outputpath + '\\' + os.path.basename(dicompath)
if not os.path.exists(outputpath):
    os.makedirs(outputpath)
index = 0
reader = sitk.ImageSeriesReader()
seriesIds = reader.GetGDCMSeriesIDs(dicompath)
dicomname = reader.GetGDCMSeriesFileNames(dicompath, seriesIds[0])
reader.SetFileNames(dicomname)
image = reader.Execute()
dataarrays = sitk.GetArrayFromImage(image)
dataarrays = dataarrays[(dataarrays.shape[0] - 619):]
for dataarray in dataarrays:
    shape = dataarray.shape
    dataarray = dataarray[0:(shape[0] - 100)][:]
    mindata = np.min(dataarray).tolist()
    maxdata = np.max(dataarray).tolist()
    shape = dataarray.shape
    flag = np.zeros((shape[0], shape[1]))
    mean = 0
    count = 0
    connectedcount = 0
    while maxdata > 1000:
        # print(str(maxdata))
        maxindex = list(np.where(dataarray == maxdata))
        # print(str(dataarray[maxindex[0][0]][maxindex[1][0]]))
        seeddata = []
        seedindex = []
        for i in range(len(maxindex[1])):
            seeddata.append(maxdata)
            seedindex.append([maxindex[0][i], maxindex[1][i]])
        while len(seeddata) > 0:
            center = seeddata[0]
            flag[seedindex[0][0]][seedindex[0][1]] = 1
            count = count + 1
            mean = (mean + center) / count
            # dataarray[seedindex[0][0]][seedindex[0][1]] = 0
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
        _, labels = cv2.connectedComponents(np.array(flag, np.uint8))
        temp = np.max(labels)
        if temp > connectedcount:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40))
            flag = cv2.morphologyEx(flag, cv2.MORPH_CLOSE, kernel)
            connectedcount = temp
        for i in range(shape[0]):
            for j in range(shape[1]):
                if flag[i][j] == 1:
                    dataarray[i][j] = mindata
        maxdata = np.max(dataarray).tolist()
    imagearray = dataarray.astype('float')
    imagearray = (dataarray - mindata)/(maxdata - mindata)
    imagearray = imagearray * 255.0
    # print(str(maxdata))
    imagearray = imagearray.astype('uint8')
    cv2.imwrite(outputpath + '\\' + os.path.basename(dicompath + '\\' + os.path.basename(dicomname[index])) + '.bmp', imagearray)
    index = index + 1
    print(str(index))
# for file in os.listdir(dicompath):
#     dicomarray=sitk.ReadImage(dicompath+'\\'+file)
#     imgarray=np.squeeze(sitk.GetArrayFromImage(dicomarray))
#     shape=imgarray.shape
#     # imgarray=np.reshape(imgarray,(shape[1],shape[2])).astype('float')
#     cv2.namedWindow("image")
#     cv2.imshow("image",imgarray)
#     cv2.waitKey(0)
# for file in os.listdir(imgpath):
#     dataarray = cv2.imread(imgpath + '\\' + file, cv2.IMREAD_GRAYSCALE)
#     dataarray = dataarray.astype('int16')
#     size = [np.size(dataarray, 0), np.size(dataarray, 1)]
#     maxdata = np.max(dataarray).tolist()
#     flag = np.zeros((size[0], size[1]))
#     mean = 0
#     count = 0
#     while maxdata > 175:
#         maxindex = list(np.where(dataarray == maxdata))
#         seeddata = []
#         seedindex = []
#         for i in range(len(maxindex[1])):
#             seeddata.append(maxdata)
#             seedindex.append([maxindex[0][i], maxindex[1][i]])
#         while len(seeddata) > 0:
#             center = seeddata[0]
#             flag[seedindex[0][0]][seedindex[0][1]] = 1
#             count = count + 1
#             mean = (mean + center) / count
#             # dataarray[seedindex[0][0]][seedindex[0][1]] = 0
#             expand(seedindex[0][0] - 1, seedindex[0][1] - 1, center)
#             expand(seedindex[0][0] - 1, seedindex[0][1], center)
#             expand(seedindex[0][0] - 1, seedindex[0][1] + 1, center)
#             expand(seedindex[0][0], seedindex[0][1] - 1, center)
#             expand(seedindex[0][0], seedindex[0][1] + 1, center)
#             expand(seedindex[0][0] + 1, seedindex[0][1] - 1, center)
#             expand(seedindex[0][0] + 1, seedindex[0][1], center)
#             expand(seedindex[0][0] + 1, seedindex[0][1] + 1, center)
#             seeddata.pop(0)
#             seedindex.pop(0)
#         for i in range(size[0]):
#             for j in range(size[1]):
#                 if flag[i][j] == 1:
#                     dataarray[i][j] = 0
#         maxdata = np.max(dataarray).tolist()
#         # print(str(maxdata))
#     dataarray = dataarray.astype('uint8')
#     cv2.imwrite(outputpath + '\\' + os.path.basename(imgpath + '\\' + file), dataarray)
#     index = index + 1
#     print(str(index))
