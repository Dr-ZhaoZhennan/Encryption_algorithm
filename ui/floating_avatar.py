import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMenu, QAction, QVBoxLayout, QComboBox, QTextEdit, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect, QLabel
from PyQt5.QtGui import QPainter, QPixmap, QRegion, QCursor, QColor, QFont, QGuiApplication
from PyQt5.QtCore import Qt, QPoint, QTimer, QRect
import os
import json
from crypto import unicode_shift, base64_codec

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(data):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception:
        pass

class PopupPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 顶层或子控件自适应：无父时作为顶层窗口，有父时作为子控件
        if parent is None:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Window)
            self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_InputMethodEnabled, True)
        self.setFixedSize(320, 260)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0,0,0,120))
        shadow.setOffset(0, 6)
        self.setGraphicsEffect(shadow)
        self.algorithms = [
            ('Unicode码位移（支持中文）', '每个字符的Unicode码+3，解密时每个字符的Unicode码-3。\n可用Python、在线Unicode工具还原。\n示例：明文“abc”→密文“def”，明文“你好”→密文“呜咍”'),
            ('Base64（支持中文）', '将文本用Base64编码，解密时用任意Base64解码工具还原。\n如 https://base64.us/\n示例：明文“abc”→密文“YWJj”，明文“你好”→密文“5L2g5aW9”')
        ]
        self.combo = QComboBox(self)
        for name, _ in self.algorithms:
            self.combo.addItem(name)
        self.decrypt_hint = QLabel(self)
        self.decrypt_hint.setStyleSheet('color:#bbb;font-size:12px;')
        self.update_decrypt_hint()
        self.combo.currentIndexChanged.connect(self.update_decrypt_hint)
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText('请输入或粘贴文本...')
        self.text_edit.setFont(QFont('微软雅黑', 11))
        self.btn_encrypt = QPushButton('加密', self)
        self.btn_decrypt = QPushButton('解密', self)
        self.btn_copy = QPushButton('复制', self)
        self.btn_clear = QPushButton('清空', self)
        self.decrypt_detail = QLabel(self)
        self.decrypt_detail.setStyleSheet('color:#888;font-size:12px;')
        self.decrypt_detail.setWordWrap(True)
        self.decrypt_detail.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.update_decrypt_detail()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(8)
        vbox.addWidget(self.combo)
        vbox.addWidget(self.decrypt_hint)
        vbox.addWidget(self.text_edit)
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_encrypt)
        hbox.addWidget(self.btn_decrypt)
        hbox.addWidget(self.btn_copy)
        hbox.addWidget(self.btn_clear)
        vbox.addLayout(hbox)
        vbox.addWidget(self.decrypt_detail)
        self.setLayout(vbox)
        self.radius = 18
        self.text_edit.installEventFilter(self)
        self.btn_encrypt.clicked.connect(self.encrypt_text)
        self.btn_decrypt.clicked.connect(self.decrypt_text)
        self.btn_copy.clicked.connect(self.copy_text)
        self.btn_clear.clicked.connect(self.clear_text)
        self.combo.currentIndexChanged.connect(self.update_decrypt_detail)
        self.text_edit.textChanged.connect(self.update_decrypt_detail)

    def ensure_input_focus(self):
        try:
            self.raise_()
            # 子控件/顶层均尝试聚焦到文本框
            self.text_edit.setFocus(Qt.OtherFocusReason)
            im = QGuiApplication.inputMethod()
            if im:
                im.show()
        except Exception:
            pass

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self.ensure_input_focus)

    def update_decrypt_hint(self):
        self.decrypt_hint.setText('解密算法：' + self.combo.currentText())

    def update_decrypt_detail(self):
        idx = self.combo.currentIndex()
        _, detail = self.algorithms[idx]
        self.decrypt_detail.setText('解密原理：\n' + detail)

    def eventFilter(self, obj, event):
        if obj == self.text_edit and event.type() == event.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.encrypt_text()
                return True
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(30, 30, 30, 230))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)

    def encrypt_text(self):
        text = self.text_edit.toPlainText()
        idx = self.combo.currentIndex()
        try:
            if idx == 0:
                result = unicode_shift.encrypt(text)
            elif idx == 1:
                result = base64_codec.encrypt(text)
            else:
                result = text
            self.text_edit.setPlainText(result)
        except Exception as e:
            self.text_edit.setPlainText(f'加密出错：{e}')

    def decrypt_text(self):
        text = self.text_edit.toPlainText()
        idx = self.combo.currentIndex()
        try:
            if idx == 0:
                result = unicode_shift.decrypt(text)
            elif idx == 1:
                result = base64_codec.decrypt(text)
            else:
                result = text
            self.text_edit.setPlainText(result)
        except Exception as e:
            self.text_edit.setPlainText(f'解密出错：{e}')

    def copy_text(self):
        text = self.text_edit.toPlainText()
        QApplication.clipboard().setText(text)

    def clear_text(self):
        self.text_edit.clear()

class AvatarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.avatar_size = 64
        self.setFixedSize(self.avatar_size, self.avatar_size)
        avatar_path = os.path.join(os.path.dirname(__file__), 'resources', 'photo.png')
        if os.path.exists(avatar_path):
            self.avatar = QPixmap(avatar_path).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            self.avatar = QPixmap(self.size())
            self.avatar.fill(QColor(120, 120, 120))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        region = QRegion(self.rect(), QRegion.Ellipse)
        self.setMask(region)
        painter.drawPixmap(0, 0, self.avatar)


class MainController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.panel = PopupPanel(self)
        self.avatar = AvatarWidget(self)
        self.panel.hide()

        self.drag_offset = QPoint()
        self.mouse_press_pos = None
        self.click_threshold = 6

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.restore_or_center()

    def restore_or_center(self):
        config = load_config()
        pos = config.get('window_pos')
        screen_rect = QApplication.primaryScreen().geometry()
        if pos and isinstance(pos, list) and len(pos) == 2:
            self.move(QPoint(pos[0], pos[1]))
        else:
            x = screen_rect.width() - self.avatar.width() - 80
            y = screen_rect.height() - self.avatar.height() - 80
            self.move(x, y)
        self.resize(self.avatar.size())

    def update_layout(self):
        if self.panel.isVisible():
            panel_x = 0
            panel_y = 0
            avatar_x = (self.panel.width() - self.avatar.width()) // 2
            avatar_y = self.panel.height() + 10
            self.panel.move(panel_x, panel_y)
            self.avatar.move(avatar_x, avatar_y)

            new_width = self.panel.width()
            new_height = self.avatar.y() + self.avatar.height()
            self.resize(new_width, new_height)
        else:
            self.avatar.move(0, 0)
            self.resize(self.avatar.size())

    def mousePressEvent(self, event):
        if self.avatar.geometry().contains(event.pos()):
            if event.button() == Qt.LeftButton:
                self.drag_offset = event.globalPos() - self.pos()
                self.mouse_press_pos = event.globalPos()
                event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mouse_press_pos:
            self.move(event.globalPos() - self.drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.mouse_press_pos:
            moved_distance = (event.globalPos() - self.mouse_press_pos).manhattanLength()
            if moved_distance <= self.click_threshold:
                self.toggle_panel()
            self.mouse_press_pos = None
            event.accept()

    def toggle_panel(self):
        # 统一保持头像的全局位置不变
        avatar_global_before = self.mapToGlobal(self.avatar.pos())
        if self.panel.isVisible():
            self.panel.hide()
        else:
            self.panel.show()
        self.update_layout()
        avatar_global_after = self.mapToGlobal(self.avatar.pos())
        self.move(self.pos() + (avatar_global_before - avatar_global_after))
        if self.panel.isVisible():
            self.panel.text_edit.setFocus()

    def show_context_menu(self, pos):
        if self.avatar.geometry().contains(pos):
            menu = QMenu(self)
            quit_action = QAction('退出', self)
            quit_action.triggered.connect(QApplication.instance().quit)
            menu.addAction(quit_action)
            menu.exec_(self.mapToGlobal(pos))

    def closeEvent(self, event):
        pos = self.pos()
        config = load_config()
        config['window_pos'] = [pos.x(), pos.y()]
        save_config(config)
        super().closeEvent(event)