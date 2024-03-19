# coding:utf-8
'''
人脸显示设置
'''

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow
from cameraVideo import camera
from main_window import Ui_mainwindow

class function_window(Ui_mainwindow,QMainWindow):
    
    #初始化
    def __init__(self):
        super(function_window,self).__init__()
        self.setupUi(self)

    #打开签到
    def open_sign_in(self):
        #启动摄像头
        self.cameraVideo = camera()
        #启动定时器，


    #摄像头数据显示
    def show_cameradata(self):
        #获取摄像头数据
        pic = self.cameraVideo.camera_to_pic()
        #在Bodylabel中显示画面
        self.BodyLabel.setPixmap(pic)

    https://www.tenorshare.cn/file-repair/