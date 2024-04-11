# coding:utf-8
from view.information import Ui_StopWatchInterface
from PyQt5.QtWidgets import QWidget

class finfmation_window(QWidget, Ui_StopWatchInterface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
