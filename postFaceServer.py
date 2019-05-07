#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json,logging,threading,queue,os,socket,time,datetime
from wsgiref.simple_server import make_server
import cv2
import numpy as np

# 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
from BasicMethod.BasicMethod import base64ToJpg


def getHostIp():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip

def application(environ, start_response):
    # 定义文件请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)

    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'].strip() == '/readsense/face':

        decodeStr = request_body.decode('utf-8')
        postData = json.loads(decodeStr)
        faceQueueListDZ.put(postData)
        #print(postData)
        dic = {'status': 'ok'}
        return [json.dumps(dic).encode('utf-8')]
    #软通动力版本
    elif environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'].strip() == '/readsense/ruantong':

        decodeStr = request_body.decode('utf-8')
        postData = json.loads(decodeStr)
        faceQueueListRT.put(postData)
        dic = {'status': 'ok'}
        return [json.dumps(dic).encode('utf-8')]
    elif environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'].strip() == '/readsense/heartbeat':
        decodeStr = request_body.decode('utf-8')

        print(json.loads(decodeStr))
        if 'macAddress' in json.loads(decodeStr).keys():
            print(datetime.datetime.now(), "[设备在线][" + json.loads(decodeStr)['macAddress']+']' + '[liveId = '+json.loads(decodeStr)['liveId']+']')
        dic = {'status': 'ok'}
        return [json.dumps(dic).encode('utf-8')]
    else:
        dic = {'status': 'error'}
        return [json.dumps(dic).encode('utf-8')]

def startSever(port = 8080):
    try:

        httpd = make_server("0.0.0.0", port, application)

        serverIp = 'http://'+getHostIp() + ":" + str(port)
        print('serving http on port : ' + serverIp)
        print('稻知版本：' + serverIp + '/readsense/face')
        print('软通动力版本：' + serverIp + '/readsense/ruantong')
        print('心跳：' + serverIp + '/readsense/heartbeat')
        #print("serving http on port {0}...".format(str(port)))

        httpd.serve_forever()
    except:
        logging.error("startSever  error!!!")

def processDaoZhi(imgpath = "./faceImage"):
    try:
        if not os.path.exists(imgpath):
            os.makedirs(imgpath)
        nSize = 0
        while True:
            if faceQueueListDZ.empty():
                time.sleep(1)
                continue
            try:
                faceData = faceQueueListDZ.get()
                nSize += 1
                print(datetime.datetime.now(), "Face OK = [%04d]" % nSize)

                # print(faceData)
                imagByteBuf = base64ToJpg(faceData['img'])
                image = np.asarray(bytearray(imagByteBuf), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                timelocal = time.localtime(float(faceData['time'] / 1000))
                dt = time.strftime("%Y-%m-%d_%H-%M-%S", timelocal)
                if faceData['faceQuality'] >= 5:
                    strTemp = imgpath + "/" + dt.split('_')[0] + "/人脸质量大于5"
                else:
                    strTemp = imgpath + "/" + dt.split('_')[0] + "/人脸质量小于5"
                if not os.path.exists(strTemp):
                    os.makedirs(strTemp)

                facepath = strTemp + "/" + dt + '_quality=[' + str(faceData['faceQuality']) + '].jpg'
                # python3.x 保存中文路径错误解决方法
                cv2.imencode('.jpg', image)[1].tofile(facepath)
                # python3.x 保存英文路径
                # cv2.imwrite(facepath, image)
                # cv2.imshow('RS', image)
                # cv2.waitKey(1)

            except:
                logging.error("imdecode error!!!")
    except:
        logging.error("processDaoZhi error!!!")


def processRuanTong(imgpath = "./faceImage"):
    try:
        if not os.path.exists(imgpath):
            os.makedirs(imgpath)
        nSize = 0
        while True:
            if faceQueueListRT.empty():
                time.sleep(1)
                continue
            try:
                faceData = faceQueueListRT.get()

                nSize += 1
                print(datetime.datetime.now(), "Face OK = [%04d]" % nSize)
                print(faceData)

                imagByteBuf = base64ToJpg(faceData['faceImage'])
                image = np.asarray(bytearray(imagByteBuf), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                timelocal = time.localtime(float(faceData['faceTime'] / 1000))
                dt = time.strftime("%Y-%m-%d_%H-%M-%S", timelocal)

                strTemp = imgpath + "/" + dt.split('_')[0] + "/" + str(faceData['macAddress']).replace(':', '_')

                if not os.path.exists(strTemp):
                    os.makedirs(strTemp)

                facepath = strTemp + "/" + dt + '_sex=[' + str(faceData['sex']) + ']' + '_age=[' + str(
                    faceData['age']) + ']' + '_attention=[' + str(faceData['attention']) + '].jpg'
                # python3.x 保存中文路径错误解决方法
                cv2.imencode('.jpg', image)[1].tofile(facepath)

            except:
                logging.error("imdecode error!!!")
    except:
        logging.error("processRuanTong error!!!")


def run(port = 8080,imgpath = "./faceImage"):
    try:

        global faceQueueListDZ,faceQueueListRT
        #faceQueueList = queue.LifoQueue(maxsize=1000)
        faceQueueListDZ = queue.Queue(maxsize=1000)
        faceQueueListRT = queue.Queue(maxsize=1000)
        server  = threading.Thread(target=startSever,args=(port,))
        acceptDZ = threading.Thread(target=processDaoZhi, args=(imgpath,))
        acceptRT = threading.Thread(target=processRuanTong, args=(imgpath,))

        server.start()
        acceptDZ.start()
        acceptRT.start()

        server.join()
        acceptDZ.join()
        acceptRT.join()

    except:
        logging.error("start server error!!!")