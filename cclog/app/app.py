import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from cclog.conf import AppConfig
from .view import View


class App(object):
    """App 基类"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(AppConfig.AppName)
        self.app.setWindowIcon(QIcon(AppConfig.AppIcon))
        self.view = View()
        self.view.show()

    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())
