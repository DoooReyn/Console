from PyQt5.QtWidgets import QMainWindow, QApplication

from cclog.app.views.log_ui import LogUI
from cclog.conf import AppConfig


class View(QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.resize(AppConfig.OriginWidth, AppConfig.OriginHeight)
        rect = QApplication.desktop().availableGeometry(0)
        x = (rect.width() - AppConfig.OriginWidth) // 2 + AppConfig.OriginOffsetX
        y = (rect.height() - AppConfig.OriginHeight) // 2 + AppConfig.OriginOffsetY
        self.setMinimumSize(AppConfig.MinWidth, AppConfig.MinHeight)
        self.move(x, y)
        self.setCentralWidget(LogUI())
