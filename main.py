# coding:utf-8

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QWidget

from qfluentwidgets import SplitFluentWindow,FluentIcon,NavigationItemPosition,NavigationAvatarWidget
from main_window import MainWindow
class Main(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SfaceS")
        self.setWindowIcon(QIcon('./resource/images/logo.png'))
        self.setMinimumSize(630,510)
        #添加子界面
        self.mainWindow = MainWindow()
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


if __name__ == '__main__':
    #enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Main()
    w.show()
    app.exec_()