import json
from typing import Union

from PyQt5.QtWidgets import QTextBrowser, QHBoxLayout, QLineEdit, QPushButton, QWidget

from cclog.app.ui import UI
from cclog.app.views.ws_client import WsObject
from cclog.conf import AppConfig, Lang, signals, WsCommand, LogStyles, Levels, StyleSheet


class LogUI(UI):

    def __init__(self):
        self.edit_server_addr: Union[None, QLineEdit] = None
        self.edit_send_msg: Union[None, QLineEdit] = None
        self.btn_connect: Union[None, QPushButton] = None
        self.browser_log: Union[None, QTextBrowser] = None
        self.btn_clear: Union[None, QPushButton] = None
        self.btn_trace: Union[None, QPushButton] = None
        self.btn_debug: Union[None, QPushButton] = None
        self.btn_info: Union[None, QPushButton] = None
        self.btn_warn: Union[None, QPushButton] = None
        self.btn_error: Union[None, QPushButton] = None
        self.btn_fatal: Union[None, QPushButton] = None
        self.btn_send: Union[None, QPushButton] = None

        self.signals = {
            Lang.Zh.BtnConnect: "on_signal_connect",
            Lang.Zh.BtnDisconnect: "on_signal_disconnect",
            Lang.Zh.BtnSend: "on_signal_send_msg",
            Lang.Zh.BtnClear: "on_signal_clear",
        }
        self.ws_object = WsObject()

        super(LogUI, self).__init__()

    def setup_ui(self):
        self.setLayout(QHBoxLayout())

        # col1
        widget_col1 = QWidget()
        self.add_vertical_layout(widget_col1)
        self.add_label(Lang.Zh.ServerAddr, widget_col1)
        self.add_label(Lang.Zh.SendMessage, widget_col1)
        self.add_label(Lang.Zh.LogContent, widget_col1)

        # col2
        widget_col2 = QWidget()
        self.add_vertical_layout(widget_col2)
        self.edit_server_addr = self.add_line_edit(AppConfig.DefaultServerAddr, widget_col2)
        self.edit_send_msg = self.add_line_edit(Lang.Zh.InputMessagePlease, widget_col2)
        self.browser_log = self.add_text_browser(widget_col2)

        # col3
        widget_col3 = QWidget()
        self.add_vertical_layout(widget_col3)
        self.btn_connect = self.add_push_button(Lang.Zh.BtnConnect, widget_col3)
        self.btn_send = self.add_push_button(Lang.Zh.BtnSend, widget_col3)
        self.btn_clear = self.add_push_button(Lang.Zh.BtnClear, widget_col3)
        self.add_label('——————', widget_col3)
        self.btn_trace = self.add_check_button("Trace", widget_col3)
        self.btn_debug = self.add_check_button("Debug", widget_col3)
        self.btn_info = self.add_check_button("Info", widget_col3)
        self.btn_warn = self.add_check_button("Warn", widget_col3)
        self.btn_error = self.add_check_button("Error", widget_col3)
        self.btn_fatal = self.add_check_button("Fatal", widget_col3)

        self.edit_server_addr.setText(AppConfig.DefaultServerAddr)
        self.browser_log.setStyleSheet(StyleSheet.TextBrowser)

    def setup_signals(self):
        self.btn_connect.clicked.connect(self.on_btn_clicked)
        self.btn_clear.clicked.connect(self.on_btn_clicked)
        self.btn_send.clicked.connect(self.on_btn_clicked)
        self.edit_server_addr.returnPressed.connect(self.on_signal_connect)
        self.edit_send_msg.returnPressed.connect(self.on_signal_send_msg)

        signals.ws_status.connect(self.on_ws_status)

    def is_mode_opened(self, mode: str):
        btn = getattr(self, 'btn_' + mode)
        if btn is not None:
            return btn.isChecked()

    @staticmethod
    def format_msg(mode, msg):
        return LogStyles.get(mode).format(msg).replace("\n", "<br>")

    def add_rich_log(self, mode, msg):
        if not mode or not msg:
            return

        if type(mode) == Levels:
            mode = mode.name

        if not self.is_mode_opened(mode):
            return

        self.browser_log.append(self.format_msg(mode, msg))

    def on_ws_status(self, cmd, msg):
        print(cmd, msg)
        if cmd == WsCommand.console or cmd == WsCommand.connected:
            self.add_rich_log(Levels.trace, msg)
        elif cmd == WsCommand.connected:
            self.btn_connect.setText(Lang.Zh.BtnDisconnect)
            self.btn_connect.setEnabled(True)
            self.edit_server_addr.setEnabled(False)
            self.add_rich_log(Levels.info, Lang.Zh.ConnectionEstablished)
        elif cmd == WsCommand.closed:
            self.btn_connect.setText(Lang.Zh.BtnConnect)
            self.btn_connect.setEnabled(True)
            self.edit_server_addr.setEnabled(True)
            self.add_rich_log(Levels.debug, Lang.Zh.ConnectionClosed)
        elif cmd == WsCommand.error:
            self.add_rich_log(Levels.error, msg)
        elif cmd == WsCommand.receive:
            try:
                data = json.loads(msg)
                self.add_rich_log(data.get("mode"), data.get('msg'))
            except Exception as e:
                self.add_rich_log(Levels.fatal, str(e))

    def on_btn_clicked(self):
        key = self.sender().text()
        signal = self.signals.get(key)
        if signal and getattr(self, signal) is not None:
            getattr(self, signal)()

    def on_signal_connect(self):
        ipaddress = self.edit_server_addr.text()
        if ipaddress.startswith("ws://"):
            self.btn_connect.setEnabled(False)
            self.edit_server_addr.setEnabled(False)
            self.ws_object.createWebSocketClient(ipaddress)
        else:
            self.add_rich_log(Levels.error, Lang.Zh.IllegalServerAddr + ipaddress)

    def on_signal_send_msg(self):
        msg = self.edit_send_msg.text()
        if len(msg) <= 0:
            self.add_rich_log(Levels.warn, Lang.Zh.InputMessagePlease)
            return
        signals.ws_send_msg.emit(msg)
        self.edit_send_msg.clear()

    def on_signal_clear(self):
        self.browser_log.clear()

    def on_signal_disconnect(self):
        signals.ws_close.emit()
