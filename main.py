import cv2
import os


imgpath=input('图像路径：')
outputpath=input('输出路径')
if not os.path.exists(outputpath+'\\'+os.path.basename(imgpath)):
    os.makedirs(outputpath+'\\'+os.path.basename(imgpath))
for file in os.listdir(imgpath):
    cv2.imread(file, cv2.IMREAD_GRAYSCALE)
