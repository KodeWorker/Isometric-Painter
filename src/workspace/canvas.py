from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QPushButton)
from PyQt5.QtGui import (QColor, QPainter, QPen, QPolygonF)
from PyQt5.QtCore import Qt, QPointF
from matrix.vector import Vector2D, Vector3D
from matrix.transform import PerspectiveProjection
from system.storage import InitMesh

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
        self.axis_line_width = 2
        self.init_axis_length = self.axis_length = \
        Vector2D(self.geometry().width(), self.geometry().height()).norm()
        # Grid parameters
        self.grid_line_width = 1
        self.grid_max = {'x':2, 'y':1, 'z':2}
        self.grid_min = {'x':0, 'y':-1, 'z':0}
        self.init_grid_length = self.grid_length = 100
        self.init_grid_mode = self.grid_mode = 1

        #======================================================================
        # Pixel storage
        #======================================================================

        self.mesh = InitMesh(self.grid_min, self.grid_max)
        #======================================================================
        # 3D perspective projection
        #======================================================================
        self.offset = Vector2D(0, 0)
        self.origin = Vector2D(self.geometry().center().x(),
                          self.geometry().center().y()) + self.offset

        self.v0 = Vector3D(0, 0, 0)
        gamma, beta, alpha = 45, 0, 60
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
        self.mesh[0]['xy'][1,1] = (100,100,100,100)
        self.mesh[1]['yz'][1,0] = (100,100,100,255)

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
        self.qPainter.setPen(QPen(Qt.blue, self.axis_line_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + x.x, self.origin.y + x.y)
        self.qPainter.setPen(QPen(Qt.red, self.axis_line_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + y.x, self.origin.y + y.y)
        self.qPainter.setPen(QPen(Qt.green, self.axis_line_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + z.x, self.origin.y + z.y)


    def drawMesh(self):

        if self.grid_mode == 0:
            #==================================================================
            # Draw grid - mode 0
            #==================================================================
            self.qPainter.setPen(QPen(Qt.gray, self.grid_line_width, Qt.DotLine))
            self.drawInnerMesh()

        elif self.grid_mode == 1:
            #==================================================================
            # Draw grid - mode 1
            #==================================================================
            self.qPainter.setPen(QPen(Qt.gray, self.grid_line_width, Qt.DotLine))
            self.drawInnerMesh()
            self.qPainter.setPen(QPen(Qt.white, self.grid_line_width, Qt.DotLine))
            self.drawOuterMesh()

    def drawInnerMesh(self):
        inner_mode = 0
        lim_dict = self.grid_min

        for x in range(self.grid_min['x'], self.grid_max['x']+1):
            for y in range(self.grid_min['y'], self.grid_max['y']+1):
                p1 = Vector3D(x, y, self.grid_min['z'])

                if self.grid_min['x'] >= 0:
                    x_idx = x+self.grid_min['x']-1
                else:
                    x_idx = x+self.grid_min['x']
                if self.grid_min['y'] >= 0:
                    y_idx = y+self.grid_min['y']-1
                else:
                    y_idx = y+self.grid_min['y']
                pixel = self.mesh[inner_mode]['xy'][x_idx, y_idx]

                self.drawOneGrid(p1, lim_dict, pixel)
        # Draw Y-Z grid plane
        for y in range(self.grid_min['y'], self.grid_max['y']+1):
            for z in range(self.grid_min['z'], self.grid_max['z']+1):
                p1 = Vector3D(self.grid_min['x'], y, z)

                if self.grid_min['y'] >= 0:
                    y_idx = y+self.grid_min['y']-1
                else:
                    y_idx = y+self.grid_min['y']
                if self.grid_min['z'] >= 0:
                    z_idx = z+self.grid_min['z']-1
                else:
                    z_idx = z+self.grid_min['z']
                pixel = self.mesh[inner_mode]['yz'][y_idx, z_idx]

                self.drawOneGrid(p1, lim_dict, pixel)
        # Draw X-Z grid plane
        for x in range(self.grid_min['x'], self.grid_max['x']+1):
            for z in range(self.grid_min['z'], self.grid_max['z']+1):
                p1 = Vector3D(x, self.grid_min['y'], z)

                if self.grid_min['x'] >= 0:
                    x_idx = x+self.grid_min['x']-1
                else:
                    x_idx = x+self.grid_min['x']
                if self.grid_min['z'] >= 0:
                    z_idx = y+self.grid_min['z']-1
                else:
                    z_idx = y+self.grid_min['z']
                pixel = self.mesh[inner_mode]['xz'][x_idx, z_idx]

                self.drawOneGrid(p1, lim_dict, pixel)

    def drawOuterMesh(self):
        outer_mode = 1
        lim_dict = {'x':self.grid_min['x'],
                    'y':self.grid_min['y'],
                    'z':self.grid_max['z']}

        for x in range(self.grid_min['x'], self.grid_max['x']+1):
            for y in range(self.grid_min['y'], self.grid_max['y']+1):
                p1 = Vector3D(x, y, self.grid_max['z'])

                if self.grid_min['x'] >= 0:
                    x_idx = x+self.grid_min['x']-1
                else:
                    x_idx = x+self.grid_min['x']
                if self.grid_min['y'] >= 0:
                    y_idx = y+self.grid_min['y']-1
                else:
                    y_idx = y+self.grid_min['y']
                pixel = self.mesh[outer_mode]['xy'][x_idx, y_idx]

                self.drawOneGrid(p1, lim_dict, pixel)

        # Draw Y-Z grid plane
        lim_dict = {'x':self.grid_max['x'],
                    'y':self.grid_min['y'],
                    'z':self.grid_min['z']}

        for y in range(self.grid_min['y'], self.grid_max['y']+1):
            for z in range(self.grid_min['z'], self.grid_max['z']+1):
                p1 = Vector3D(self.grid_max['x'], y, z)

                if self.grid_min['y'] >= 0:
                    y_idx = y+self.grid_min['y']-1
                else:
                    y_idx = y+self.grid_min['y']
                if self.grid_min['z'] >= 0:
                    z_idx = z+self.grid_min['z']-1
                else:
                    z_idx = z+self.grid_min['z']
                pixel = self.mesh[outer_mode]['yz'][y_idx, z_idx]

                self.drawOneGrid(p1, lim_dict, pixel)

        # Draw X-Z grid plane
        lim_dict = {'x':self.grid_min['x'],
                    'y':self.grid_max['y'],
                    'z':self.grid_min['z']}

        for x in range(self.grid_min['x'], self.grid_max['x']+1):
            for z in range(self.grid_min['z'], self.grid_max['z']+1):
                p1 = Vector3D(x, self.grid_max['y'], z)

                if self.grid_min['x'] >= 0:
                    x_idx = x+self.grid_min['x']-1
                else:
                    x_idx = x+self.grid_min['x']
                if self.grid_min['z'] >= 0:
                    z_idx = y+self.grid_min['z']-1
                else:
                    z_idx = y+self.grid_min['z']
                pixel = self.mesh[outer_mode]['xz'][x_idx, z_idx]

                self.drawOneGrid(p1, lim_dict, pixel)

    def drawOneGrid(self, p, lim_dict, pixel):

        p1 = Vector3D(p.x,                              max(p.y-1, lim_dict['y']),         max(p.z-1, lim_dict['z']))
        p2 = Vector3D(max(p.x-1, lim_dict['x']),        p.y,                               max(p.z-1, lim_dict['z']))
        p3 = Vector3D(max(p.x-1, lim_dict['x']),        max(p.y-1, lim_dict['y']),         p.z)
        p4 = Vector3D(max(p.x-1, lim_dict['x']),        max(p.y-1, lim_dict['y']),         max(p.z-1, lim_dict['z']))

        P = p.project(self.R, self.v0)*self.grid_length
        P1 = p1.project(self.R, self.v0)*self.grid_length
        P2 = p2.project(self.R, self.v0)*self.grid_length
        P3 = p3.project(self.R, self.v0)*self.grid_length
        P4 = p4.project(self.R, self.v0)*self.grid_length

        # Diagonal grid
        if p.x != lim_dict['x']:
            self.qPainter.drawLine(self.origin.x + P.x, self.origin.y + P.y,
                        self.origin.x + P1.x, self.origin.y + P1.y)
        else:
            # Y-Z mesh
            polygon = QPolygonF()
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P.x, P.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P2.x, P2.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P4.x, P4.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P3.x, P3.y))

        if p.y != lim_dict['y']:
            self.qPainter.drawLine(self.origin.x + P.x, self.origin.y + P.y,
                        self.origin.x + P2.x, self.origin.y + P2.y)
        else:
            # X-Z mesh
            polygon = QPolygonF()
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P1.x, P1.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P.x, P.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P3.x, P3.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P4.x, P4.y))

        if p.z != lim_dict['z']:
            self.qPainter.drawLine(self.origin.x + P.x, self.origin.y + P.y,
                        self.origin.x + P3.x, self.origin.y + P3.y)
        else:
            # X-Y mesh
            polygon = QPolygonF()
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P1.x, P1.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P.x, P.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P2.x, P2.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P4.x, P4.y))

        # Paint the grid area
        color = QColor(pixel[0], pixel[1], pixel[2], pixel[3])
        #self.qPainter.setPen(color)
        self.qPainter.setBrush(color)
        self.qPainter.drawPolygon(polygon)

        # Horizontal and vertical grid
        self.qPainter.drawLine(self.origin.x + P4.x, self.origin.y + P4.y,
                        self.origin.x + P3.x, self.origin.y + P3.y)
        self.qPainter.drawLine(self.origin.x + P4.x, self.origin.y + P4.y,
                        self.origin.x + P2.x, self.origin.y + P2.y)
        self.qPainter.drawLine(self.origin.x + P4.x, self.origin.y + P4.y,
                        self.origin.x + P1.x, self.origin.y + P1.y)


    #==========================================================================
    # Button Events
    #==========================================================================

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

    #==========================================================================
    # Mouse Events
    #==========================================================================

    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            # Update draging position
            self.drag_start = Vector2D(event.pos().x(), event.pos().y())\
             - self.offset

    def mouseMoveEvent(self, event):
        # Drag canvas while holding right mouse button on Canvas
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
