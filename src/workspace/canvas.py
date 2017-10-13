from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QPushButton)
from PyQt5.QtGui import (QColor, QPainter, QPen)
from PyQt5.QtCore import Qt
from matrix.vector import Vector2D, Vector3D, PerspectiveProjection
from math import pi

class Canvas(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initCanvas()

    def initCanvas(self):
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        tab1 = PaintArea()
        tab2 = PaintArea()
        self.tabs.addTab(tab1, 'tab1')
        self.tabs.addTab(tab2, 'tab2')

        vbox.addWidget(self.tabs)
        self.setLayout(vbox)

        self.tabs.tabCloseRequested.connect(self.removeTab)

    def removeTab(self, index):
        self.tabs.removeTab(index)

class PaintArea(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initCanvas()

    def initCanvas(self):
        # Axis parameters
        self.axis_width = 2
        self.init_axis_length = self.axis_length = \
        Vector2D(self.geometry().width(), self.geometry().height()).norm()
        # Grid parameters
        self.grid_width = 1
        self.grid_max = {'x':10, 'y':10, 'z':10}
        self.grid_min = {'x':0, 'y':0, 'z':0}
        self.init_grid_length = self.grid_length = 100
        self.init_grid_mode = self.grid_mode = 1

        #======================================================================
        # 3D perspective projection
        #======================================================================
        self.offset = Vector2D(0, 0)
        self.origin = Vector2D(self.geometry().center().x(),
                          self.geometry().center().y()) + self.offset

        self.v0 = Vector3D(0, 0, 0)
        gamma, beta, alpha = -pi*45/180, 0, -pi*60/180
        self.R = PerspectiveProjection(gamma, beta, alpha)

        #======================================================================
        # Buttons
        #======================================================================
        reset_btn = QPushButton("reset", self)
        reset_btn.clicked[bool].connect(self.resetGridPos)

        self.mode_btn = QPushButton('%d' %self.grid_mode, self)
        self.mode_btn.setCheckable(True)
        self.mode_btn.clicked[bool].connect(self.setGridMode)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.mode_btn)
        hbox.addWidget(reset_btn)
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def paintEvent(self, event):
        self.qPainter = QPainter()
        self.qPainter.begin(self)

        #======================================================================
        # Draw background
        #======================================================================

        # Black background
        self.qPainter.setPen(QColor(0, 0, 0))
        self.qPainter.setBrush(QColor(0, 0, 0))
        self.qPainter.drawRect(self.geometry())

        #======================================================================
        # Draw 3D object
        #======================================================================

        # Update origin
        self.origin = Vector2D(self.geometry().center().x(),
                          self.geometry().center().y()) + self.offset

        self.drawAxis()
        self.drawMesh()

        self.qPainter.end()

    def drawAxis(self):
        #======================================================================
        # Draw axis
        #======================================================================

        x_unit = Vector3D(1, 0, 0)
        y_unit = Vector3D(0, 1, 0)
        z_unit = Vector3D(0, 0, 1)

        x = x_unit.project(self.R, self.v0)*self.axis_length
        y = y_unit.project(self.R, self.v0)*self.axis_length
        z = z_unit.project(self.R, self.v0)*self.axis_length

        # Draw axis
        self.qPainter.setPen(QPen(Qt.blue, self.axis_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + x.x, self.origin.y + x.y)
        self.qPainter.setPen(QPen(Qt.red, self.axis_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + y.x, self.origin.y + y.y)
        self.qPainter.setPen(QPen(Qt.green, self.axis_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + z.x, self.origin.y + z.y)

    def drawMesh(self):

        if self.grid_mode == 0:
            #==================================================================
            # Draw grid - mode 0
            #==================================================================

            self.qPainter.setPen(QPen(Qt.gray, self.grid_width, Qt.DotLine))
            # Draw X-Y grid plane
            lim_dict = self.grid_min

            for x in range(1, self.grid_max['x']+1):
                for y in range(1, self.grid_max['y']+1):
                    p1 = Vector3D(x, y, self.grid_min['z'])
                    self.drawGrid(p1, lim_dict)
            # Draw Y-Z grid plane
            for y in range(1, self.grid_max['y']+1):
                for z in range(1, self.grid_max['z']+1):
                    p1 = Vector3D(self.grid_min['x'], y, z)
                    self.drawGrid(p1, lim_dict)
            # Draw X-Z grid plane
            for x in range(1, self.grid_max['x']+1):
                for z in range(1, self.grid_max['z']+1):
                    p1 = Vector3D(x, self.grid_min['y'], z)
                    self.drawGrid(p1, lim_dict)

        elif self.grid_mode == 1:
            #==================================================================
            # Draw grid - mode 1
            #==================================================================

            self.qPainter.setPen(QPen(Qt.white, self.grid_width, Qt.DotLine))
            # Draw X-Y grid plane
            lim_dict = {'x':self.grid_min['x'],
                        'y':self.grid_min['y'],
                        'z':self.grid_max['z']}

            for x in range(1, self.grid_max['x']+1):
                for y in range(1, self.grid_max['y']+1):
                    p1 = Vector3D(x, y, self.grid_max['z'])
                    self.drawGrid(p1, lim_dict)

            # Draw Y-Z grid plane
            lim_dict = {'x':self.grid_max['x'],
                        'y':self.grid_min['y'],
                        'z':self.grid_min['z']}

            for y in range(1, self.grid_max['y']+1):
                for z in range(1, self.grid_max['z']+1):
                    p1 = Vector3D(self.grid_max['x'], y, z)
                    self.drawGrid(p1, lim_dict)

            # Draw X-Z grid plane
            lim_dict = {'x':self.grid_min['x'],
                        'y':self.grid_max['y'],
                        'z':self.grid_min['z']}

            for x in range(1, self.grid_max['x']+1):
                for z in range(1, self.grid_max['z']+1):
                    p1 = Vector3D(x, self.grid_max['y'], z)
                    self.drawGrid(p1, lim_dict)

        #======================================================================
        # Paint grid
        #======================================================================

    def drawGrid(self, p, lim_dict):

        p1 = Vector3D(p.x,                              max(p.y-1, lim_dict['y']),         max(p.z-1, lim_dict['z']))
        p2 = Vector3D(max(p.x-1, lim_dict['x']),        p.y,                               max(p.z-1, lim_dict['z']))
        p3 = Vector3D(max(p.x-1, lim_dict['x']),        max(p.y-1, lim_dict['y']),         p.z)
        p4 = Vector3D(max(p.x-1, lim_dict['x']),        max(p.y-1, lim_dict['y']),         max(p.z-1, lim_dict['z']))

        P = p.project(self.R, self.v0)*self.grid_length
        P1 = p1.project(self.R, self.v0)*self.grid_length
        P2 = p2.project(self.R, self.v0)*self.grid_length
        P3 = p3.project(self.R, self.v0)*self.grid_length
        P4 = p4.project(self.R, self.v0)*self.grid_length

        if p.x != lim_dict['x']:
            self.qPainter.drawLine(self.origin.x + P.x, self.origin.y + P.y,
                        self.origin.x + P1.x, self.origin.y + P1.y)
        if p.y != lim_dict['y']:
            self.qPainter.drawLine(self.origin.x + P.x, self.origin.y + P.y,
                        self.origin.x + P2.x, self.origin.y + P2.y)
        if p.z != lim_dict['z']:
            self.qPainter.drawLine(self.origin.x + P.x, self.origin.y + P.y,
                        self.origin.x + P3.x, self.origin.y + P3.y)

        self.qPainter.drawLine(self.origin.x + P4.x, self.origin.y + P4.y,
                        self.origin.x + P3.x, self.origin.y + P3.y)
        self.qPainter.drawLine(self.origin.x + P4.x, self.origin.y + P4.y,
                        self.origin.x + P2.x, self.origin.y + P2.y)
        self.qPainter.drawLine(self.origin.x + P4.x, self.origin.y + P4.y,
                        self.origin.x + P1.x, self.origin.y + P1.y)

    def setGridMode(self, pressed):
        self.grid_mode += 1
        self.grid_mode %= 2
        self.mode_btn.setText('%d' %self.grid_mode)
        self.update()

    def resetGridPos(self, pressed):
        # Reset configuration
        self.grid_length = self.init_grid_length
        self.grid_mode = self.init_grid_mode
        self.offset = Vector2D(0, 0)
        # Reset "mode" button
        self.mode_btn.setChecked(False)
        self.mode_btn.setText('%d' %self.grid_mode)
        self.update()

    #===========================================================================
    # Mouse Events
    #===========================================================================

    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            # Update draging position
            self.drag_start = Vector2D(event.pos().x(), event.pos().y())\
             - self.offset

    def mouseReleaseEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        # Drag canvas
        if event.buttons() == Qt.RightButton:
            drag = Vector2D(event.pos().x(), event.pos().y()) - self.drag_start
            # Update axis length
            self.axis_length = self.init_axis_length + (self.offset+drag).norm()
            # Update mesh offset
            self.offset = drag
            self.update()

    def wheelEvent(self, event):
        #======================================================================
        # Zoom in/out when scroll upd/down
        #======================================================================
        if event.angleDelta().y() > 0:
            self.grid_length *= 2
        else:
            self.grid_length /= 2
        self.update()
