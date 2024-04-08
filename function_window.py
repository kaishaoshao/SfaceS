# coding:utf-8
'''
人脸显示设置
'''

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget,QMessageBox
from cameraVideo import camera
from main_window import Ui_mainwindow
from PyQt5.QtGui import QIcon,QPixmap

from view.mainWindow import Ui_mainwindow

from qfluentwidgets import SplitFluentWindow,FluentIcon,NavigationItemPosition,NavigationAvatarWidget
from main_window import MainWindow
class Main(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SfaceS")
        self.setWindowIcon(QIcon('./resource/images/logo.png'))
        self.setMinimumSize(630,510)
        #添加子界面
        self.mainWindow = function_window()
        #添加侧边栏Icon
        self.addSubInterface(self.mainWindow,FluentIcon.RINGER,"签到界面")


        #添加其他导航项
        self.navigationInterface.addWidget(
            routeKey = 'avatar',
            widget = NavigationAvatarWidget('用户','./resource/images/logo.png'),
            position=NavigationItemPosition.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey = 'setting',
            icon = FluentIcon.SETTING,
            text = '设置',
            position=NavigationItemPosition.BOTTOM
        )



class function_window(QWidget,Ui_mainwindow):
    
    #初始化
    def __init__(self):
        super(function_window,self).__init__()
        self.setupUi(self)

        self.sign_pressed = False

        self.lab_cap.setScaledContents(True)                #设置图片自适应大小
        self.btn_sign.clicked.connect(self.open_sign_in)
        self.btn_close.clicked.connect(self.close_sign_in)


    #打开签到
    def open_sign_in(self):
        self.sign_pressed = True
        #启动摄像头
        self.cameraVideo = camera()
        #启动定时器，获取摄像头刷新
        self.timeshow = QTimer(self)
        self.timeshow.start(10)
        #每隔10ms刷新一次
        self.timeshow.timeout.connect(self.show_cameradata)


    # #摄像头数据显示
    def show_cameradata(self):
        #获取摄像头数据
        pic = self.cameraVideo.camera_to_pic()
        #在Bodylabel中显示画面
        self.lab_cap.setPixmap(pic)


    # #关闭签到
    def close_sign_in(self):
        if self.sign_pressed == False :
            QMessageBox.warning(self,"警告","没有签到")
            return self.sign_pressed
        else:
            #关闭定时器
            self.timeshow.stop()
            self.timeshow.timeout.disconnect(self.show_cameradata)
            #关闭摄像头
            self.cameraVideo.colse_camera()
            #判断定时器是否关闭，则显示为自己设定的图像
            if self.timeshow.isActive() == False:
                self.lab_cap.setPixmap(QPixmap("./resource/images/logo.png"))
            else:
                QMessageBox.information(self, "提示", "关闭失败")