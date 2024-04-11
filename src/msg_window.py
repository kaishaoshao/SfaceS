# coding:utf-8
from view.message import Ui_FocusInterface
from PyQt5.QtWidgets import QWidget

class message_window(QWidget, Ui_FocusInterface):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
