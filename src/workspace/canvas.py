from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QPushButton)
from PyQt5.QtGui import (QColor, QPainter, QPen, QPolygonF, QPalette, QIcon)
from PyQt5.QtCore import (Qt, QPointF)
from system.matrix.vector import (Vector2D, Vector3D)
from system.matrix.transform import PerspectiveProjection
from system.storage import InitMesh

from config.base import get_asset_dir
from config.canvas import (get_axis_line_width, get_grid_line_width,
                           get_grid_length, get_grid_mode)

class Canvas(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initCanvas()

    def initCanvas(self):
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        
        self.newPaintArea()

        vbox.addWidget(self.tabs)
        self.setLayout(vbox)
        
        self.tabs.tabCloseRequested.connect(self.removeTab)

    def removeTab(self, index):
        self.tabs.removeTab(index)
    
    def newPaintArea(self, file_name=None):
        if file_name == None:
            file_name = 'temp'
        paintArea = PaintArea()
        self.tabs.addTab(paintArea, file_name)

class PaintArea(QWidget):

    def __init__(self, x=8, y=8, z=8, parent=None):
        super().__init__(parent)
        self.initPaintArea(x, y, z)

    def initPaintArea(self, x, y, z):

        # Axis parameters
        self.axis_line_width = get_axis_line_width()
        self.init_axis_length = self.axis_length = \
        Vector2D(self.geometry().width(), self.geometry().height()).norm()
        # Grid parameters
        self.grid_line_width = get_grid_line_width()
        self.grid_max = {'x':x, 'y':y, 'z':z}
        self.grid_min = {'x':0, 'y':0, 'z':0}
        self.init_grid_length = self.grid_length = get_grid_length()
        self.init_grid_mode = self.grid_mode = get_grid_mode()

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
        
        x_unit = Vector3D(1, 0, 0)
        y_unit = Vector3D(0, 1, 0)
        z_unit = Vector3D(0, 0, 1)

        self.x_u = x_unit.project(self.R, self.v0)
        self.y_u = y_unit.project(self.R, self.v0)
        self.z_u = z_unit.project(self.R, self.v0)
        
        #======================================================================
        # Buttons
        #======================================================================
        
        reset_btn = QPushButton(QIcon(get_asset_dir('reset.png')), '', self)
        reset_btn.clicked[bool].connect(self.resetBtn)

        self.mode_btn = QPushButton(QIcon(get_asset_dir('mode%d.png' %self.grid_mode)), '', self)
        self.mode_btn.setCheckable(True)
        self.mode_btn.clicked[bool].connect(self.modeBtn)
        
        self.grid_btn = QPushButton(QIcon(get_asset_dir('grid_on.png')), '', self)
        self.showGrid = True
        self.grid_btn.clicked[bool].connect(self.gridBtn)
        
        self.axis_btn = QPushButton(QIcon(get_asset_dir('axis_on.png')), '', self)
        self.showAxis = True
        self.axis_btn.clicked[bool].connect(self.axisBtn)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.axis_btn)
        hbox.addWidget(self.grid_btn)
        hbox.addStretch()        
        hbox.addWidget(self.mode_btn)
        hbox.addWidget(reset_btn)
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
        #======================================================================
        # Draw background
        #======================================================================
        
        qPalette = QPalette()
        qPalette.setColor(QPalette.Background, Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(qPalette)
        
        #======================================================================
        # Draw test cells
        #======================================================================
        self.mesh[0]['xy'][0,0] = (100,100,100,100)
        self.mesh[0]['yz'][0,0] = (100,100,100,100)
        self.mesh[0]['xz'][0,0] = (100,100,100,100)
        
        self.mesh[1]['xy'][0,0] = (255,000,000,100)
        self.mesh[1]['yz'][0,0] = (000,255,000,100)
        self.mesh[1]['xz'][0,0] = (000,000,255,100)
        
    def paintEvent(self, event):
        self.qPainter = QPainter()
        self.qPainter.begin(self)

        # Update origin and axis length
        self.origin = Vector2D(self.geometry().center().x(),
                          self.geometry().center().y()) + self.offset
        if self.showAxis:
            self.axis_length = \
            Vector2D(self.geometry().width(), self.geometry().height()).norm()
            self.drawAxis()            
        self.drawMesh()
        
        self.qPainter.end()

    def drawAxis(self):
        #======================================================================
        # Draw axis
        #======================================================================
        self.qPainter.setPen(QPen(Qt.blue, self.axis_line_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + self.x_u.x*self.axis_length,
                    self.origin.y + self.x_u.y*self.axis_length)
        self.qPainter.setPen(QPen(Qt.red, self.axis_line_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + self.y_u.x*self.axis_length,
                    self.origin.y + self.y_u.y*self.axis_length)
        self.qPainter.setPen(QPen(Qt.green, self.axis_line_width, Qt.DashLine))
        self.qPainter.drawLine(self.origin.x, self.origin.y,
                    self.origin.x + self.z_u.x*self.axis_length,
                    self.origin.y + self.z_u.y*self.axis_length)

    def drawMesh(self):
        if not self.showGrid:
            self.qPainter.setPen(QPen(QColor(0, 0, 0, 0), self.grid_line_width, Qt.DotLine))
        if self.grid_mode == 0:
            #==================================================================
            # Draw grid - mode 0
            #==================================================================
            if self.showGrid:
                self.qPainter.setPen(QPen(Qt.gray, self.grid_line_width, Qt.DotLine))
            self.drawInnerMesh()

        elif self.grid_mode == 1:
            #==================================================================
            # Draw grid - mode 1
            #==================================================================
            if self.showGrid:
                self.qPainter.setPen(QPen(Qt.gray, self.grid_line_width, Qt.DotLine))
            self.drawInnerMesh()
            if self.showGrid:
                self.qPainter.setPen(QPen(Qt.white, self.grid_line_width, Qt.DotLine))
            self.drawOuterMesh()

    def drawInnerMesh(self):
        inner_mode = 0
        
        # Draw X-Y grid plane
        for x in range(self.grid_min['x'], self.grid_max['x']):
            for y in range(self.grid_min['y'], self.grid_max['y']):
                p = Vector3D(x, y, self.grid_min['z'])
                color = self.mesh[inner_mode]['xy'][x-self.grid_min['x'], y-self.grid_min['y']]
                self.drawOneGrid(p+Vector3D(1, 1, 0), self.grid_min, color)
                
        # Draw Y-Z grid plane
        for y in range(self.grid_min['y'], self.grid_max['y']):
            for z in range(self.grid_min['z'], self.grid_max['z']):
                p = Vector3D(self.grid_min['x'], y, z)
                color = self.mesh[inner_mode]['yz'][y-self.grid_min['y'], z-self.grid_min['z']]
                self.drawOneGrid(p+Vector3D(0, 1, 1), self.grid_min, color)
                
        # Draw X-Z grid plane
        for x in range(self.grid_min['x'], self.grid_max['x']):
            for z in range(self.grid_min['z'], self.grid_max['z']):
                p = Vector3D(x, self.grid_min['y'], z)
                color = self.mesh[inner_mode]['xz'][x-self.grid_min['x'], z-self.grid_min['z']]
                self.drawOneGrid(p+Vector3D(1, 0, 1), self.grid_min, color)

    def drawOuterMesh(self):
        outer_mode = 1
        
        lim_dict = {'x':self.grid_min['x'],
                    'y':self.grid_min['y'],
                    'z':self.grid_max['z']}

        for x in range(self.grid_min['x'], self.grid_max['x']):
            for y in range(self.grid_min['y'], self.grid_max['y']):
                p = Vector3D(x, y, self.grid_max['z'])
                color = self.mesh[outer_mode]['xy'][x-self.grid_min['x'], y-self.grid_min['y']]
                self.drawOneGrid(p+Vector3D(1, 1, 0), lim_dict, color)
                
        # Draw Y-Z grid plane
        lim_dict = {'x':self.grid_max['x'],
                    'y':self.grid_min['y'],
                    'z':self.grid_min['z']}

        for y in range(self.grid_min['y'], self.grid_max['y']):
            for z in range(self.grid_min['z'], self.grid_max['z']):
                p = Vector3D(self.grid_max['x'], y, z)
                color = self.mesh[outer_mode]['yz'][y-self.grid_min['y'], z-self.grid_min['z']]
                self.drawOneGrid(p+Vector3D(0, 1, 1), lim_dict, color)
                
        # Draw X-Z grid plane
        lim_dict = {'x':self.grid_min['x'],
                    'y':self.grid_max['y'],
                    'z':self.grid_min['z']}

        for x in range(self.grid_min['x'], self.grid_max['x']):
            for z in range(self.grid_min['z'], self.grid_max['z']):
                p = Vector3D(x, self.grid_max['y'], z)
                color = self.mesh[outer_mode]['xz'][x-self.grid_min['x'], z-self.grid_min['z']]
                self.drawOneGrid(p+Vector3D(1, 0, 1), lim_dict, color)
        
    def drawOneGrid(self, p, lim_dict, color):

        p1 = Vector3D(p.x,                              max(p.y-1, lim_dict['y']),         max(p.z-1, lim_dict['z']))
        p2 = Vector3D(max(p.x-1, lim_dict['x']),        p.y,                               max(p.z-1, lim_dict['z']))
        p3 = Vector3D(max(p.x-1, lim_dict['x']),        max(p.y-1, lim_dict['y']),         p.z)
        p4 = Vector3D(max(p.x-1, lim_dict['x']),        max(p.y-1, lim_dict['y']),         max(p.z-1, lim_dict['z']))
        
        P = self.x_u*p.x*self.grid_length + self.y_u*p.y*self.grid_length + self.z_u*p.z*self.grid_length
        P1 = self.x_u*p1.x*self.grid_length + self.y_u*p1.y*self.grid_length + self.z_u*p1.z*self.grid_length
        P2 = self.x_u*p2.x*self.grid_length + self.y_u*p2.y*self.grid_length + self.z_u*p2.z*self.grid_length
        P3 = self.x_u*p3.x*self.grid_length + self.y_u*p3.y*self.grid_length + self.z_u*p3.z*self.grid_length
        P4 = self.x_u*p4.x*self.grid_length + self.y_u*p4.y*self.grid_length + self.z_u*p4.z*self.grid_length

        if p.x == lim_dict['x']:
            # Y-Z mesh
            polygon = QPolygonF()
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P.x, P.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P2.x, P2.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P4.x, P4.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P3.x, P3.y))

        elif p.y == lim_dict['y']:
            # X-Z mesh
            polygon = QPolygonF()
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P1.x, P1.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P.x, P.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P3.x, P3.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P4.x, P4.y))

        elif p.z == lim_dict['z']:
            # X-Y mesh
            polygon = QPolygonF()
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P1.x, P1.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P.x, P.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P2.x, P2.y))
            polygon.append(QPointF(self.origin.x, self.origin.y) + QPointF(P4.x, P4.y))

        # Paint the grid area
        qColor = QColor(color[0], color[1], color[2], color[3])
        self.qPainter.setBrush(qColor)
        self.qPainter.drawPolygon(polygon)

    #==========================================================================
    # Button Events
    #==========================================================================

    def modeBtn(self, pressed):
        self.grid_mode += 1
        self.grid_mode %= 2
        self.mode_btn.setIcon(QIcon(get_asset_dir('mode%d.png' %self.grid_mode)))
        self.update()

    def resetBtn(self, pressed):
        # Reset configuration
        self.grid_length = self.init_grid_length
        self.grid_mode = self.init_grid_mode
        self.offset = Vector2D(0, 0)
        # Reset "mode" button
        self.mode_btn.setChecked(False)
        self.mode_btn.setIcon(QIcon(get_asset_dir('mode%d.png' %self.grid_mode)))
        self.update()
        
    def gridBtn(self, pressed):
        self.showGrid = not self.showGrid
        if self.showGrid:
            self.grid_btn.setIcon(QIcon(get_asset_dir('grid_on.png')))
        else:
            self.grid_btn.setIcon(QIcon(get_asset_dir('grid_off.png')))
        self.update()
    
    def axisBtn(self, pressed):
        self.showAxis = not self.showAxis
        if self.showAxis:
            self.axis_btn.setIcon(QIcon(get_asset_dir('axis_on.png')))
        else:
            self.axis_btn.setIcon(QIcon(get_asset_dir('axis_off.png')))
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
        #======================================================================
        # Drag canvas while holding right mouse button on Canvas
        #======================================================================
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
