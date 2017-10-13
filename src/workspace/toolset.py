from PyQt5.QtWidgets import (QTextEdit, QWidget, QVBoxLayout)

class Toolset(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initToolset()
        
    def initToolset(self):
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        canvasLog = QTextEdit('Toolset!')
        vbox.addWidget(canvasLog)
        self.setLayout(vbox)