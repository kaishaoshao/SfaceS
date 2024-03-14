# coding:utf-8
'''
open函数完成摄像头的配置打开
'''

import cv2
import numpy as np

class camera():
    #初始化
    def __init__(self):
        self.open_camera()

    #通过opencv打开电脑默认摄像头
    def open_camera(self):
        #0表示内置默认摄像头，self.capture为全局变量
        self.capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        if self.capture.isOpened():
            print("摄像头打开成功")
        #定义一个多维数组，用来存储获取的画面数据
        self.curerentframe = np.array([])

    #获取摄像头数据
    def read_cameraData(self):
        ret,data = self.capture.read()
        if not ret:
            print("获取摄像头数据失败")
            return None
        return data

    #摄像头图像格式转换
    def camera_to_pic(self):
        pic = self.read_cameraData()
        #摄像头是BGR转换为RGB
        self.curerentframe = cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)