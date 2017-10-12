from PyQt5.QtWidgets import (QTextEdit, QWidget, QVBoxLayout)

class Viewer(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initViewer()
        
    def initViewer(self):
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        canvasLog = QTextEdit('Viewer!')
        vbox.addWidget(canvasLog)
        self.setLayout(vbox)