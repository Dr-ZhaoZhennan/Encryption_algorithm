from ui.floating_avatar import FloatingAvatar
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtCore import Qt, QPoint, QTimer, QRect

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FloatingAvatar()
    window.show()
    sys.exit(app.exec_()) 