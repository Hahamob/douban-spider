# 工具模块
import datetime
import os
import random
import time

from random import randint


class Util(object):

    # 获取当前时间
    def getCurrentTime(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 获取时间戳+六位随机数，用于上传文件名
    def getCurrentTimeRandom(self):
        strTemp = ""
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            strTemp += ch
        return str(round(time.time() * 1000))+"_"+strTemp

    # 程序运行暂停一会
    def getRandomSleep(self):
        sleep = random.randint(5,10)
        print("**休息一会开始（"+str(sleep)+"秒）**")
        # 控制访问速度，秒
        time.sleep(sleep)
        print("**休息一会结束（" + str(sleep) + "秒）**")


