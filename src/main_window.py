# coding:utf-8

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from view.mainWindow import Ui_mainwindow
from qfluentwidgets import SplitFluentWindow,FluentIcon,NavigationItemPosition,NavigationAvatarWidget
from src.function_window import function_window

# 调用view
class MainWindow(QWidget,Ui_mainwindow):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

# 主界面
class Main(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SfaceS")
        self.setWindowIcon(QIcon('../resource/images/logo.png'))
        self.setMinimumSize(700,600)
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

