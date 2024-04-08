# coding:utf-8
'''
open函数完成摄像头的配置打开
'''

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

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
        print("test")

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
        # 将图像pic从BGR颜色空间转换为RGB颜色空间，并赋值给self.currentframe
        self.currentframe = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        
        # 获取当前帧的高度和宽度
        height, width = self.currentframe.shape[:2]

        # 创建一个名为qimg的QImage对象，用于存储当前帧的图像数据
        qimg = QImage(self.currentframe, width, height, QImage.Format_RGB888)
        # 根据qimg创建一个名为qpix的QPixmap对象，用于在界面上显示图像
        qpix = QPixmap.fromImage(qimg)

        return qpix


    #关闭摄像头
    def colse_camera(self):
        #释放摄像头资源
        self.capture.release()
        return None

        