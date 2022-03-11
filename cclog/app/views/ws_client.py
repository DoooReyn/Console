import time
from typing import Union

import websocket
from PyQt5.QtCore import QObject

from cclog.common import StoppableThread
from cclog.conf import Lang, signals, WsCommand


class WsObject(QObject):

    def __init__(self):
        super(WsObject, self).__init__()

        self.ws_threading: Union[None, StoppableThread] = None
        self.ws_client = None
        self.host = None

        def close():
            if self.ws_client is not None:
                self.ws_client.close(status=websocket.STATUS_GOING_AWAY, reason=b"request to close")
                self.host = None

        signals.ws_close.connect(close)

        def send(msg):
            if self.ws_client is not None:
                self.ws_client.send(msg)

        signals.ws_send_msg.connect(send)

        def check():
            while True:
                time.sleep(1)
                if self.ws_client is None and self.host is not None:
                    self.createWebSocketClient(self.host)

        self.ws_check_thread = StoppableThread(target=check)
        self.ws_check_thread.daemon = True
        self.ws_check_thread.start()

    def createWebSocketClient(self, host: str):
        if self.ws_client is not None:
            signals.ws_status.emit(WsCommand.console, Lang.Zh.WaitMinute)
            return

        def on_message(_, message):
            signals.ws_status.emit(WsCommand.receive, message)

        def on_error(_, error):
            signals.ws_status.emit(WsCommand.error, str(error))

        def on_close(_, __, ___):
            signals.ws_status.emit(WsCommand.closed, Lang.Zh.ConnectionClosed)
            self.ws_client = None
            if self.ws_threading is not None and self.ws_threading.is_alive():
                self.ws_threading.stop()
                msg = Lang.Zh.ThreadClosed.format(self.ws_threading.name, self.ws_threading.native_id)
                signals.ws_status.emit(WsCommand.console, msg)
                self.ws_threading = None

        def on_open(_):
            self.host = host
            signals.ws_status.emit(WsCommand.connected, Lang.Zh.ConnectionEstablished)

        websocket.enableTrace(False)
        self.ws_client = websocket.WebSocketApp(host,
                                                on_message=on_message,
                                                on_error=on_error,
                                                on_close=on_close,
                                                on_open=on_open)
        self.ws_threading = StoppableThread(target=self.ws_client.run_forever)
        self.ws_threading.daemon = True
        self.ws_threading.start()
