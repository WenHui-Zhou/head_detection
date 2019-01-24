
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw,ImageFont
SIZE1 = 640
SIZE2 = 480

txtDir = "/home/zhouwenhui/AI/head_Detection/TensorBox/data/yuncong/TXT/"
imSaveDir = "/home/zhouwenhui/AI/head_Detection/TensorBox/data/yuncong/part_B_resize/"
prePath = "/home/zhouwenhui/AI/head_Detection/TensorBox/data/yuncong/"
txtlist = os.listdir(txtDir)
for tx in range(0,len(txtlist)):
    txtPath = os.path.join(txtDir,txtlist[tx])
    txtfile = open(txtPath)
    jsonFile = []
    while True:
        lines = txtfile.readline().split()
        if not lines:
            break
        #deal with image resize
        imPath  = prePath +lines[0]
        imName = imPath.split("/")[-1]
        im = Image.open(imPath)
        wRatio = SIZE1/float(im.size[0])
        hRatio = SIZE2/float(im.size[1])
        resizeIm = im.resize((SIZE1,SIZE2))
        savePath = os.path.join(imSaveDir,imName)
        resizeIm.save(savePath)
        
        #deal with image bbox
        bboxLine = lines[3:]
        rectList = []
        i = 0
        while i< len(bboxLine)-3:
            x1 = int(bboxLine[i])*(wRatio)
            y1 = int(bboxLine[i+1])*hRatio
            w = int(bboxLine[i+2])*wRatio
            h = int(bboxLine[i+3])*hRatio
            x2 = x1+w
            y2 = y1+h
            rectList.append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2})
            i += 5
        jsonFile.append({'image_path': savePath,"rects":rectList})
    
    with open(prePath+txtlist[tx].split('.')[0]+'.json', 'w+') as f:
        json.dump(jsonFile, f)
        print('done')


