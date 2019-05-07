#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,logging
from postFaceServer import run


if len(sys.argv) <= 1:
    port = 8080
    imgpath = "./faceImage"

else:
    try:
        print('\t参数1：Server port)\n'
              '\t参数2：Sava image path\n')
        port = int(sys.argv[1])
        imgpath = sys.argv[2]

    except:
        logging.error('参数输入错误!!!')
        sys.exit()


if __name__ == '__main__':
    run(port,imgpath)

