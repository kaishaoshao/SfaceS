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
        self.BodyLabel.setScaledContents(True) #设置图片自适应大小
        self.PushButton.clicked.connect(self.open_sign_in)    #打开签到 （有问题）
        self.PushButton_2.clicked.connect(self.close_sign_in) #关闭签到  （有问题）


    #打开签到
    def open_sign_in(self):
        #启动摄像头
        self.cameraVideo = camera()
        #启动定时器，获取摄像头刷新
        self.timeshow = QTimer(self)
        self.timeshow.start(10)
        #每隔10ms刷新一次
        self.timeshow.timeout.connect(self.show_cameradata)


    #摄像头数据显示
    def show_cameradata(self):
        #获取摄像头数据
        pic = self.cameraVideo.camera_to_pic()
        #在Bodylabel中显示画面
        self.BodyLabel.setPixmap(pic)
        

    #关闭签到
    def close_sign_in(self):
        #关闭定时器
        self.timeshow.stop()  
        self.timeshow.timeout.disconnect(self.show_cameradata)
         #关闭摄像头
        self.cameraVideo.close_camera()
        #判断定时器是否关闭，则显示为自己设定的图像
        if self.timeshow.isActive() == False:
            self.label.setPixmap(QPixmap("./resource/images/logo.png"))
        else:
            QMessageBox.information(self, "提示", "关闭失败")