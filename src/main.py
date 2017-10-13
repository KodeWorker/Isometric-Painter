import sys
from PyQt5.QtWidgets import (QApplication, QDesktopWidget)
from base import (BaseApplication, Desk)

class IsometricPainter(BaseApplication):

    def __init__(self):
        super().__init__()

    def initUI(self):

        self.setWindowTitle('Isometric-Painter')

        self.resize(self.windowWidth, self.windowHeight)
        center_point = QDesktopWidget().availableGeometry().center()
        self.frameGeometry().moveCenter(center_point)

        self.initMenu()
        self.initToolbar()

        self.desk = Desk(self)

        self.initStatusbar()
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ip = IsometricPainter()
    sys.exit(app.exec_())
