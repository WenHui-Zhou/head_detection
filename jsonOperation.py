import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--method',type = int,required = 'true')
parser.add_argument('--pathList',required = 'true')
args = parser.parse_args()
pathList = args.pathList
pathList = pathList.split(',')
print('input path:',pathList)


def create_All_data_json():
    '''
    将输入的pathList中的所有json文件组合成一个，名字为All_train.json.

    python jsonOperation.py --method 1 --pathList F:/yuncong/yuncong_data/Mall_train.json,
    F:/yuncong/yuncong_data/our_train.json,
    F:/yuncong/yuncong_data/Part_A_train.json,
    F:/yuncong/yuncong_data/Part_B_train.json
    '''
    print('create all data json')
    H = []
    for path in pathList:
        print(path)
        with open(path, 'r') as f:
            H1 = json.load(f)
            H += H1
    with open('All_data.json', 'w') as f:
        json.dump(H,f)
    print('done')

def split_evaluate_and_train():
    '''
    将数据分为train与evaluate部分，默认evaluate/train为 1/20
    python jsonOperation --method 2 --pathList F:/yuncong/yuncong_data/Mall_train.json,
    F:/yuncong/yuncong_data/our_train.json,
    F:/yuncong/yuncong_data/Part_A_train.json,
    F:/yuncong/yuncong_data/Part_B_train.json
    '''
    H_evaluate = []
    H_train = []
    for path in pathList:
        with open(path, 'r') as f:
            H1 = json.load(f)
            H_train += H1[:int(len(H1)*19/20)]
            H_evaluate += H1[int(len(H1)*19/20):]
    with open('All_train.json', 'w') as f:
        json.dump(H_train,f)
    with open('All_evaluate.json', 'w') as f:
        json.dump(H_evaluate,f)
    print(len(H_evaluate))
    print(len(H_train))
    print('done')

if args.method == 1:
    print('execute create_All_data_json')
    create_All_data_json()
elif args.method == 2:
    print('execute split_evaluate_and_train')
    split_evaluate_and_train()
