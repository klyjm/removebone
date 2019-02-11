import cv2
import os
import math
import numpy as np


imgpath=input('图像路径：')
outputpath=input('输出路径：')
if not os.path.exists(outputpath+'\\'+os.path.basename(imgpath)):
    os.makedirs(outputpath+'\\'+os.path.basename(imgpath))
for file in os.listdir(imgpath):
    dataarray=cv2.imread(imgpath+'\\'+file, cv2.IMREAD_GRAYSCALE)
    maxdata=np.max(dataarray)
    seed=[]
    seed.append(maxdata)
    while len(seed)>0:
        center=seed[0]
        centerx=math.floor(center/100)
