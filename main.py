# coding:utf-8

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from src.main_window import Main

if __name__ == '__main__':
    #enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Main()
    w.show()
    app.exec_()