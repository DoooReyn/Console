from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextBrowser, QLabel, QVBoxLayout, QPushButton


class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        pass

    def setup_signals(self):
        pass

    @property
    def default_font(self):
        font = QFont()
        font.setPointSize(10)
        return font

    @property
    def default_height(self):
        return 28

    @property
    def default_layout_spacing(self):
        return 10

    @property
    def default_button_size(self):
        return QSize(84, 28)

    @property
    def default_minimum_width(self):
        return 400

    def add_vertical_layout(self, child: QWidget):
        self.layout().addWidget(child)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(self.default_layout_spacing)
        child.setLayout(layout)

    def add_label(self, text: str, parent: QWidget):
        child = QLabel(text)
        child.setAlignment(Qt.AlignCenter)
        child.setFixedHeight(self.default_height)
        parent.layout().addWidget(child)
        return child

    def add_line_edit(self, placeholder: str, parent: QWidget):
        child = QLineEdit()
        child.setMinimumWidth(self.default_minimum_width)
        child.setFont(self.default_font)
        child.setFixedHeight(self.default_height)
        child.setPlaceholderText(placeholder)
        parent.layout().addWidget(child)
        return child

    def add_push_button(self, text, parent: QWidget):
        child = QPushButton(text)
        child.setFixedSize(self.default_button_size)
        parent.layout().addWidget(child)
        return child

    def add_check_button(self, text: str, parent: QWidget, checked: bool = True):
        child = QPushButton(text)
        child.setFixedSize(self.default_button_size)
        child.setCheckable(True)
        child.setChecked(checked)
        parent.layout().addWidget(child)
        return child

    def add_text_browser(self, parent: QWidget):
        child = QTextBrowser()
        child.setFont(self.default_font)
        child.setReadOnly(True)
        child.setAcceptRichText(True)
        child.setMinimumHeight(self.default_minimum_width)
        parent.layout().addWidget(child)
        return child
