import json
import os
import argparse
import matplotlib.pyplot as plt
from PIL import Image
import cv2

def input_matchToModel(path):
    '''
    比赛数据格式 -> 模型接受的数据格式(Part_B_train.json)
    当前数据库图片的输入格式
    train/path/to/image/2001.jpg 50 1 41 232 52 54 1......
    需要转换成的输入格式：
    {   "image_path”:"brainwash_11_13_2014_images/0163.png",
        "rect" : [{"x1":329.0, "x2":344.0, "y1": 137.0, "y2": 152.0},
              {"x1":391.0, "x2":341.0, "y1": 127.0, "y2": 128.},
             {},{}...]
    },{...}
    :param path: 文件路径
    :return:
    '''
    filepath = os.path.splitext(path) #返回一个(path/to/a, .txt)
    with open(path) as f:
        lines = f.readlines()
        step = 2
        gap = 5
        jsonFile = []
        for line in lines:
            lineList = line.split(' ')
            count = int(lineList[1])
            rectList = []
            for i in range(count):
                x1 = int(lineList[step + i * gap + 1]) # x1,y1->左下
                y1 = int(lineList[step + i * gap + 2])
                w = int(lineList[step + i * gap + 3])
                h = int(lineList[step + i * gap + 4])
                x2 = x1 + w
                y2 = y1 + h                            # x2,y2->右上
                rectList.append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2})
            jsonFile.append({'image_path': lineList[0],"rects":rectList})

        with open(filepath[0]+'.json', 'w+') as f:
            json.dump(jsonFile, f)
#    with open('Part_B_train.json') as f:
#        a = json.load(f)
        #print(a[0]['rect'])
    print('done')


def output_ModelToMatch(path,conf_threshold):
    '''
    模型输出json格式：
    { "image_path”:"brainwash_11_13_2014_images/0163.png",
    "rect" : [
    {"score":0.507844,"x1":329.0, "x2":344.0, "y1": 137.0, "y2": 152.0},
    {"score":0.507844,"x1":391.0, "x2":341.0, "y1": 127.0, "y2": 128.},
    {},{}...]
    },{...}

    比赛要求提交数据的格式
    5  (人头个数)
    x y w h confidence
    x y w h confidence
    ...
    :param path: 文件路径
    :param conf_threshold: 置信度度阈值
    :return: 输出的json对应缩放前原始大小的矩形框
    '''
    with open(path) as f:
        file = json.load(f)
    filepath = os.path.splitext(path)  # 返回一个(path/to/a, .txt)
    for k in range(len(file)):
        imgName = os.path.splitext(file[k]['image_path'])[0]#[0]
        path_img = file[k]['image_path']
        img = cv2.imread(path_img)  # 调图片得到图片的原始大小
        width_rate = img.shape[0]/640
        height_rate = img.shape[1]/480
        count = len(file[k]['rects'])
        time = 0 # 矩形框个数
        strRect =''
        for i in range(count):
            if(file[k]['rects'][i]['score'] >= conf_threshold):# score->x1
                time += 1
                x1 = file[k]['rects'][i]['x1']*width_rate # x1,y1->左下
                y1 = file[k]['rects'][i]['y1']*height_rate
                x2 = file[k]['rects'][i]['x2']*width_rate # x2,y2->右上
                y2 = file[k]['rects'][i]['y2']*height_rate
                w = x2-x1
                h = y2 - y1
                #得到这些坐标之后需要通过一个resize，还原到他原始的位置上，即乘以rate
                strRect += str(x1)+ ' '+str(y1)+' '+str(w)+' '+str(h)+' '+str(file[k]['rects'][i]['score'])+'\n'
        strRect = imgName + '\n' + str(time) + '\n'+strRect
        with open(filepath[0]+'.txt','a') as f: #打开文件追加
            f.write(strRect)
    print('done')


def imgShow(path,flag,conf_threshold):
    # path to json,flag = 1 原始图片,flag = 0 model 输出的图片，size变了需要缩放
    with open(path) as f:
        file = json.load(f)
    for k in range(len(file)):
        path_img = file[k]['image_path']
        img = cv2.imread(path_img)  # 调图片得到图片的原始大小
        width_rate = img.shape[0]/640 #将输出的[640,480]缩小回去
        height_rate = img.shape[1]/480
        count = len(file[k]['rects'])
        strRect =''
        for i in range(count):
            if(flag == -1): #原始图片
                x1 = file[k]['rects'][i]['x1']   # x1,y1->左下
                y1 = file[k]['rects'][i]['y1']
                x2 = file[k]['rects'][i]['x2']   # x2,y2->右上
                y2 = file[k]['rects'][i]['y2']
                w = x2 - x1
                h = y2 - y1
                # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)
            else:           #需要缩放的图片
                if (file[k]['rects'][i]['score'] >= conf_threshold):# score->x1
                    x1 = file[k]['rects'][i]['x1']*width_rate # x1,y1->左下
                    y1 = file[k]['rects'][i]['y1']*height_rate
                    x2 = file[k]['rects'][i]['x2']*width_rate # x2,y2->右上
                    y2 = file[k]['rects'][i]['y2']*height_rate
                    w = x2-x1
                    h = y2 - y1
                    img = cv2.resize(img, (img.shape[0], img.shape[1]), interpolation=cv2.INTER_CUBIC)
                    # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)
            cv2.imwrite('denote_'+path_img, img)  #保存了一下
#            cv2.namedWindow('Image')  绘制窗口的代码
#            cv2.imshow('image', img)
#            cv2.waitKey(0)
#            cv2.destroyAllWindows()

    print('done')



#input_matchToModel('F:/yuncong/yuncong_data/Part_B_train.txt')
#output_ModelToMatch('C:/Users/ZHOU/Desktop/面试准备文件/TensorBox-develop/prediction/save.ckpt-999.val_boxes.json',0.2)

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True)
parser.add_argument('--method', required=True)
parser.add_argument('--conf_threshold',default=0.2)
args = parser.parse_args()
if args.method == '1':
    input_matchToModel(args.path)
elif args.method == '2':
    output_ModelToMatch(args.path,args.conf_threshold)
