from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QAction, QMenu,
                             QToolBar, QFrame, QSplitter, QHBoxLayout, QWidget,
                             QTextEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class BaseApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windowWidth, self.windowHeight = 800, 600
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle('demo name')
        
        self.resize(self.windowWidth, self.windowHeight)
        center_point = QDesktopWidget().availableGeometry().center()
        self.frameGeometry().moveCenter(center_point)        
        
        self.initMenu()
        self.initToolbar()
        
        self.workspace = Workspace(self)
        self.setCentralWidget(self.workspace)
        
        self.initStatusbar()      
        self.show()

    def initMenu(self):
        menubar = self.menuBar()
        
        # File menu
        fileMenu = menubar.addMenu('File')
        self.initFileMenu(fileMenu)
        
        helpMenu = menubar.addMenu('Help')
        self.initHelpMenu(helpMenu)

    def initFileMenu(self, fileMenu):
        
        # New
        newAct = QAction('New', self)
        newAct.setShortcut('Ctrl+N')
        
        # Open
        openAct = QAction('Open', self)
        openAct.setShortcut('Ctrl+O')
        
        # Open recent
        #======================================================================
        openRecentMenu = QMenu('Open recent', self)
        openRecentAct = QAction('Clear list', self)
        
        recentList = ['demo-1','demo-2']
        for item in recentList:            
            openRecentMenu.addAction(QAction('%s' %item, self))
            
        openRecentMenu.addSeparator()        
        openRecentMenu.addAction(openRecentAct)
        #======================================================================
        
        # Save
        saveAct = QAction('Save', self)
        saveAct.setShortcut('Ctrl+S')
        
        # Save
        closeAct = QAction('Close', self)
        
        # Quit
        quitAct = QAction('Quit', self)
        quitAct.setShortcut('Ctrl+Q')        
        
        #######################################################################
        
        # Menu Item Structure
        fileMenu.addAction(newAct)
        fileMenu.addSeparator()
        fileMenu.addAction(openAct)
        fileMenu.addMenu(openRecentMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(saveAct)
        fileMenu.addSeparator()
        fileMenu.addAction(closeAct)
        fileMenu.addSeparator()
        fileMenu.addAction(quitAct)
        
        #######################################################################

    def initHelpMenu(self, helpMenu):
        
        # Report issue
        reportAct= QAction('Report issue', self)
        
        # About Isometric Painter
        aboutAct = QAction('About Isometric Painter', self)
        
        #######################################################################
        
        # Menu Item Structure
        helpMenu.addAction(reportAct)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAct)
        
        #######################################################################
    
    def initToolbar(self):
        
        cursorTool = QAction(QIcon('cursor.png'), 'cursor', self)
        penTool = QAction(QIcon('pen.png'), 'Pen', self)
        eraserTool = QAction(QIcon('eraser.png'), 'Eraser', self)
        lineTool = QAction(QIcon('line.png'), 'Line', self)
        paintBucketTool = QAction(QIcon('paint_bucket.png'), 'Paint Bucket', self)
        
        toolbar = QToolBar('Paint Tool')
        self.addToolBar(Qt.BottomToolBarArea , toolbar)
                      
        #######################################################################
        
        # Toolbar Item Structure
        toolbar.addAction(cursorTool)
        toolbar.addAction(penTool)
        toolbar.addAction(eraserTool)
        toolbar.addSeparator()
        toolbar.addAction(lineTool)
        toolbar.addSeparator()
        toolbar.addAction(paintBucketTool)
        
        #######################################################################
    
    def initStatusbar(self):
        
        self.statusbar = self.statusBar()
        
class Workspace(QFrame):
    
    def __init__(self, parent=None):
        super().__init__(parent)        
        self.initWorkspace()
    
    def initWorkspace(self):
        hbox = QHBoxLayout(self)

        # Canvas
        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
                        
        # Toolset
        rightTop = QFrame(self)
        rightTop.setFrameShape(QFrame.StyledPanel)
                
        # Viewer
        rightBottom = QFrame(self)
        rightBottom.setFrameShape(QFrame.StyledPanel)
        
        #######################################################################
        
        # Workspace Item Structure
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(rightTop)
        splitter1.addWidget(rightBottom)
        # set splitter ratio
        splitter1.setSizes([self.parentWidget().windowHeight, self.parentWidget().windowHeight])
        
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(left)
        splitter2.addWidget(splitter1)
        # set splitter ratio
        splitter2.setSizes([self.parentWidget().windowHeight, self.parentWidget().windowWidth - self.parentWidget().windowHeight])
        
        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        #######################################################################
        
        self.canvas = Canvas(left)
        self.toolset = Toolset(rightTop)
        self.viewr = Viewer(rightBottom)
        
class Canvas(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initCanvas()
    
    def initCanvas(self):
        pass
        
class Toolset(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initToolset()
    
    def initToolset(self):
        pass

class Viewer(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initViewer()
    
    def initViewer(self):
        pass
