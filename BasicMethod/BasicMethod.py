#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,logging,yaml,base64,cv2
import numpy as np


# 遍历目录下图片
def BrowsePic(fpath):
    PicList = []
    if not os.path.exists(fpath):
        print("此目录不存在!!!")
        return PicList
    for root, dirs, files in os.walk(fpath):
        for x in files:
            if x.endswith('.jpg') or x.endswith('.JPG') or x.endswith('.bmp') or x.endswith(
                    '.BMP') or x.endswith('.png') or x.endswith(".PNG") or x.endswith(".gray"):
                PicList.append(root + os.path.sep + x)
        return PicList


# 遍历目录下所有图片，包括子目录
def BrowsePics(fpath):
    PicList = []
    if not os.path.exists(fpath):
        print("此目录不存在!!!")
        return PicList
    for root, dirs, files in os.walk(fpath):
        for x in files:
            # if x.find('.jpg') != -1 or x.find('.JPG') != -1 or x.find('.bmp') != -1 or x.find(
            #         '.BMP') != -1 or x.find('.png') != -1 or x.find("PNG") != -1:

            if x.endswith('.jpg') or x.endswith('.JPG') or x.endswith('.bmp') or x.endswith(
                    '.BMP') or x.endswith('.png') or x.endswith(".PNG"):
                PicList.append(root + os.path.sep + x)
    return PicList

# 遍历目录,只遍历一层目录
def BrowseDir(fpath,index = 1):
    DirList = []
    nCount = 0
    if not os.path.exists(fpath):
        print("此目录不存在!!!")
        return DirList
    for root, dirs, files in os.walk(fpath):
        nCount += 1
        if len(dirs) > 0:
            for dir in dirs:
                DirList.append(root + os.path.sep + dir)
        if nCount == index:
            break
    return DirList

# 创建目录
def CreateFolder(path, filename = ' '):
    try:
        TempPath = path + os.path.sep + filename
        if not os.path.exists(TempPath):
            # os.mkdir(pathTemp)
            os.makedirs(TempPath)
    except:
        logging.error('CreateFolder error')

# 遍历txt
def BrowseTxt(fpath):
    TxtList = []
    if not os.path.exists(fpath):
        print("此目录不存在!!!")
        return TxtList
    for x in os.listdir(fpath):
        if x.endswith('.txt'):
            if os.path.isfile(os.path.join(fpath, x)):
                TxtList.append(x)
    return TxtList


# 遍历Xml
def BrowseXml(fpath):
    XmlList = []
    if not os.path.exists(fpath):
        print("此目录不存在!!!")
        return XmlList
    for x in os.listdir(fpath):
        if x.endswith('.xml'):
            if os.path.isfile(os.path.join(fpath, x)):
                XmlList.append(x)
    return XmlList


# 遍历bin
def BrowseName(fpath,name = 'bin'):
    binlList = []
    if not os.path.exists(fpath):
        print("此目录不存在!!!")
        return binlList
    for x in os.listdir(fpath):
        if x.endswith('.'+name):
            if os.path.isfile(os.path.join(fpath, x)):
                binlList.append(x)
    return binlList

# 遍历目录下所有bin，包括子目录
def BrowseNames(fpath,name = 'bin'):
    binlList = []
    if not os.path.exists(fpath):
        print("此目录不存在!!!")
        return binlList
    for root, dirs, files in os.walk(fpath):
        for x in files:
            if x.endswith('.'+name):
                binlList.append(root + os.path.sep + x)
    return binlList

# 快速排序
def quick_sort(myList, indexArr, start, end):

    try:
        if start < end:
            i, j = start, end
            base = myList[i]
            while i < j:
                while (i < j) and (myList[j] >= base):
                    j = j - 1
                myList[i] = myList[j]
                _temp = indexArr[j]
                indexArr[j] = indexArr[i]
                indexArr[i] = _temp
                while (i < j) and (myList[i] <= base):
                    i = i + 1
                myList[j] = myList[i]
                _temp = indexArr[j]
                indexArr[j] = indexArr[i]
                indexArr[i] = _temp
            myList[i] = base
            quick_sort(myList, indexArr, start, i - 1)
            quick_sort(myList, indexArr, j + 1, end)

    except:
        print('quick_sortError!!!')


def PartitionSample(samefile,multiNum):
    '''
        :param samefile:输入样本列表文件
        :param multiNum:划分的样本分数
        :return:
    '''
    try:
        with open(samefile,'r') as file:
            AllData = file.readlines()
            out = []
            num = int(len(AllData)/multiNum)
            rem = int(len(AllData)%multiNum)
            for k in range(0,multiNum):
                outTemp = []
                for z in range(0,num):
                    outTemp.append(AllData[k*num + z].split('\n')[0].split('\r')[0])
                if(k==multiNum-1):
                    for x in range(0, rem):
                        outTemp.append(AllData[num * multiNum + x].split('\n')[0].split('\r')[0])
                out.append(outTemp)
            return out
    except:
        return None


def readConfFile(confpath = 'config/IputSetting.yaml'):
    '''
    # 读取配置文件(启动的线程或者进程数量)
    :param confpath:
    :return:
    '''
    try:
        with open(confpath,'r',encoding='utf-8') as cofile:
            conf = yaml.load(cofile)

        return conf
    except:
        return yaml.load(None)



def file2ImageBuffer(path):
    try:
        if os.path.exists(path):
            with open(path, 'rb') as file:
                data = file.read()
                return data
        else:
            return 0
    except:
        return None

def jpgToBase64(path):
    try:
        if os.path.exists(path):
            with open(path,'rb') as file:
                base64buffer = base64.b64encode(file.read())#读取文件内容，转换为base64编码
                # 解码转成字符串
                imgBufferString = base64buffer.decode('utf-8')
                return imgBufferString
        else:
            return None
    except:
        return None

def base64ToJpg(base64Str):
    try:
        images = base64.b64decode(base64Str)

        return images
    except:
        return None


# YUV通道转BGR图像，只有Y通道数据
def y2Image(binfilepath,width,height):
    try:
        fp = open(binfilepath, 'rb')
        imageY = np.zeros((height, width), np.uint8, 'C')
        for m in range(height):
            for n in range(width):
                imageY[m, n] = ord(fp.read(1))
        fp.close()
        return imageY
    except:
        return None


# YUV通道转BGR图像
def yuv2Image(binfilepath, width, height):
    try:
        fp = open(binfilepath, 'rb')
        uv_width = width / 2
        uv_height = height / 2
        imageY = np.zeros((height, width), np.uint8, 'C')
        imageU = np.zeros((uv_height, uv_width), np.uint8, 'C')
        imageV = np.zeros((uv_height, uv_width), np.uint8, 'C')

        for m in range(height):
            for n in range(width):
                imageY[m, n] = ord(fp.read(1))

        for m in range(uv_height):
            for n in range(uv_width):
                imageV[m, n] = ord(fp.read(1))
                imageU[m, n] = ord(fp.read(1))

        fp.close()
        return (imageY,imageU,imageV)
    except:
        return None

'''
# YUV图像转JPG（灰度图）
def bin2Jpg(filepath,width = 640,height = 360 ):
    try:
        binNamelist = BrowseBins(filepath)
        for binPath in binNamelist:
            name = binPath.split('\\')[-1].split('.')[0]
            savePath = u'' + binPath.split(name)[0] + name + '.jpg'
            print(savePath)
            image = y2Image(binPath,width,height)
            #python3.x 保存中文路径错误解决方法
            cv2.imencode('.jpg',image)[1].tofile(savePath)
            #python3.x 保存英文路径
            #cv2.imwrite(savePath,image)
            cv2.imshow('YUV_Y_Show', image)
            cv2.waitKey(1)
    except:
        return None
'''

# 二值化图像数据像素坐标分类,convert表示是否交换x和y坐标位置:
def thresholdClassify(picpath,convert = True):
    try:
        laneArea = []
        imageThreshold = cv2.imread(picpath)
        try:
            # 读取中文路径图像
            imageThreshold = cv2.imdecode(np.fromfile(picpath, dtype=np.uint8), -1)
        except:
            cv2.waitKey(1)
        imgArray = np.array(imageThreshold)
        for y in range(len(imgArray)):
            for x in range(len(imgArray[y])):
                if imgArray[y][x] == 255:
                    if convert==True:
                        laneArea.append([y, x])
                    elif convert == False:
                        laneArea.append([x, y])

        return laneArea
    except:
        return []

