from PyQt5.QtCore import pyqtSignal, QObject


class AppSignals(QObject):
    ws_status = pyqtSignal(str, str)
    ws_close = pyqtSignal()
    ws_receive_msg = pyqtSignal(str)
    ws_send_msg = pyqtSignal(str)


signals = AppSignals()
