import os
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw,ImageFont
SIZE1 = 480
SIZE2 = 640


imSaveDir = "/home/zhouwenhui/AI/head_Detection/TensorBox/data/yuncong/part_B_resize/"

txtDir = "/home/zhouwenhui/AI/head_Detection/TensorBox/data/yuncong/TXT/"
imTrainSaveDir = "/home/zhouwenhui/AI/head_Detection/TensorBox/data/yuncong/split_part_B_resize/train/"
imTestSaveDir = "/home/zhouwenhui/AI/head_Detection/TensorBox/data/yuncong/split_part_B_resize/test/"
prePath = "/home/zhouwenhui/AI/head_Detection/TensorBox/data/yuncong/"
txtlist = os.listdir(txtDir)
for tx in range(0,len(txtlist)):
    txtPath = os.path.join(txtDir,txtlist[tx])
    txtfile = open(txtPath)
    jsonFileTrain = []
    jsonFileTest = []
    count = 0
    while True:
        lines = txtfile.readline().split()
        if not lines:
            break
        
        count +=1
        #deal with image resize
        imPath  = prePath +lines[0]
        imName = imPath.split("/")[-1]
        im = Image.open(imPath)
        wRatio = SIZE1/float(im.size[0])
        hRatio = SIZE2/float(im.size[1])
        resizeIm = im.resize((SIZE1,SIZE2))
        if count<300:
            saveTrainPath = os.path.join(imTrainSaveDir,imName)
            resizeIm.save(saveTrainPath)
        else:
            saveTestPath = os.path.join(imTestSaveDir,imName)
            resizeIm.save(saveTestPath)
        
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
        if count<300:
            jsonFileTrain.append({'image_path': saveTrainPath,"rects":rectList})
        else:
            jsonFileTest.append({'image_path': saveTestPath,"rects":rectList})

    with open(prePath+'Part_B_Train'+'.json', 'w+') as f1:
        json.dump(jsonFileTrain, f1)
        print('Traindone')
    with open(prePath+'Part_B_Test'+'.json', 'w+') as f2:
        json.dump(jsonFileTest, f2)
        print('Testdone')  
        
