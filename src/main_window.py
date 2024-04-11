# coding:utf-8

from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QPixmap,QPainter,QColor
from PyQt5.QtWidgets import QWidget

from view.mainWindow import Ui_mainwindow

class MainWindow(QWidget,Ui_mainwindow):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
