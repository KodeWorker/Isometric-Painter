from workspace.canvas import Canvas
from workspace.toolset import Toolset
from workspace.viewer import Viewer
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

class Desk():
    
    def __init__(self, parent=None):
        self.initDesk(parent)
    
    def initDesk(self, parent):        
        self.canvas = Canvas()
        self.toolset = Toolset()
        self.viewer = Viewer()
        
        self.canvasDock = DeskDock('Canvas', parent)
        parent.addDockWidget(Qt.LeftDockWidgetArea, self.canvasDock)
        self.canvasDock.setWidget(self.canvas)
        
        self.toolsetDock = DeskDock('Toolset', parent)
        parent.addDockWidget(Qt.RightDockWidgetArea, self.toolsetDock)
        self.toolsetDock.setWidget(self.toolset)
        
        self.viewerDock = DeskDock('Viewer', parent)
        parent.addDockWidget(Qt.RightDockWidgetArea, self.viewerDock)
        self.viewerDock.setWidget(self.viewer)
        
class DeskDock(QDockWidget):
    
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.initDeskDock()
    
    def initDeskDock(self):
        self.setWindowTitle(self.name)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)