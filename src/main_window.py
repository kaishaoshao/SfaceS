# coding:utf-8

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon,QColor, QCursor
from view.mainWindow import Ui_mainwindow

from src.finfmation_window import finfmation_window
from src.function_window import function_window
from src.msg_window import message_window
from src.login_window import login_window

from PyQt5.QtWidgets import  QWidget
from qfluentwidgets import (SplitFluentWindow,RoundMenu,NavigationItemPosition,NavigationAvatarWidget,
                            FluentIcon, Action, AvatarWidget, BodyLabel,HyperlinkButton, CaptionLabel, setFont, isDarkTheme)
# 调用view
class MainWindow(QWidget,Ui_mainwindow):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


# 主界面
class Main(SplitFluentWindow):

    def __init__(self):
        super().__init__()

        self.initMain()
        # 添加子界面
        self.mainWindow = function_window()
        self.megWidnow = message_window()
        self.finformation = finfmation_window()
        self.longWinow = login_window()

        self.initNavigation()

    def initMain(self):
        self.setWindowTitle("SfaceS")
        self.setWindowIcon(QIcon('./resource/images/logo.png'))
        self.setMinimumSize(700, 600)

    def initNavigation(self):

        #添加侧边栏Icon
        self.addSubInterface(self.mainWindow,FluentIcon.RINGER,"签到界面")
        self.addSubInterface(self.megWidnow,FluentIcon.CALENDAR,"信息管理")
        self.addSubInterface(self.finformation,FluentIcon.SEARCH,"信息查找")


        #添加其他导航项
        self.navigationInterface.addWidget(
            routeKey = 'avatar',
            widget = NavigationAvatarWidget('用户','./resource/images/logo.png'),
            # onClick = self.longWinow,
            position = NavigationItemPosition.BOTTOM,
        )


        self.navigationInterface.addItem(
            routeKey='github',
            icon = FluentIcon.GITHUB,
            onClick=self.showGithub,
            text = 'Github',
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.addItem(
            routeKey = 'setting',
            icon = FluentIcon.SETTING,
            text = '设置',
            position=NavigationItemPosition.BOTTOM,
        )

    def showGithub(self):
        menu = RoundMenu(parent=self)
        # add custom widget
        card = ProfileCard('./resource/images/logo.png',
                           'kaishaoshao', '2032751077@qq.com', menu)
        menu.addWidget(card, selectable=False)
        # menu.addWidget(card, selectable=True, onClick=lambda: print('666'))

        menu.addSeparator()
        menu.addActions([
            Action(FluentIcon.PEOPLE, '管理账户和设置'),
        ])
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.SETTING, '设置'))
        # 获取当前鼠标位置
        cursor_position = QCursor.pos()
        # 打印鼠标位置信息
        #print(cursor_position)

        # 使用当前鼠标位置显示菜单
        menu.exec_(cursor_position)

    def show_login(self):
        print("www")
        login_window()

class ProfileCard(QWidget):
    """ Profile card """
    def __init__(self, avatarPath: str, name: str, email: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name, self)
        self.emailLabel = CaptionLabel(email, self)
        self.logoutButton = HyperlinkButton(
            'https://github.com/kaishaoshao/SfaceS', 'github地址', self)

        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.emailLabel.setStyleSheet('QLabel{color: ' + color.name() + '}')

        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: ' + color.name() + '}')
        setFont(self.logoutButton, 13)

        self.setFixedSize(307, 82)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.emailLabel.move(64, 32)
        self.logoutButton.move(52, 48)