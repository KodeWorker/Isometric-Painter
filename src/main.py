import os
import sys
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

from base import (BaseApplication, Desk)
from config.base import get_asset_dir
from system.file.base import read_pickle_file,  write_pickle_file

class IsometricPainter(BaseApplication):

    def __init__(self):
        super().__init__()

    def initUI(self):

        self.setWindowTitle('Isometric-Painter')
        self.setWindowIcon(QIcon(get_asset_dir('icon.png')))
        
        self.resize(self.windowWidth, self.windowHeight)
        center_point = QDesktopWidget().availableGeometry().center()
        self.frameGeometry().moveCenter(center_point)

        self.initMenu()
        self.initToolbar()

        self.desk = Desk(self)
        
        self.openPathDone = False
        self.newId = 0
        self.workRecord = {}
        self.newFile()
        
        self.initStatusbar()
                
        self.show()
    
    def workingDirCheck(self):
        if not self.openPathDone and sys.platform == 'win32':
            # win32 system system disk
            self.openPath = '/'
            self.openPathDone = True
        elif not self.openPathDone and sys.platform.startswith('linux'):
            # linux system system disk
            self.openPath = '/home'
            self.openPathDone = True
    
    def newFile(self):
        self.workingDirCheck()

        if self.newId == 0:
            #!
            file_name = 'New*'
        else:
            #!
            file_name = 'New-%d*' %self.newId
        grid_max, mesh, idx = self.desk.canvas.newPaintArea(file_name)
        #!
        self.workRecord[file_name] = {'path':None, 'index':idx, 'done':False}
        self.newId += 1
        
    def openFile(self):
        self.workingDirCheck()
        
        fname = QFileDialog.getOpenFileName(self, 'Open File', self.openPath,
                                            "Isometric File Extension (*.ifx)")
        if fname[0]:
            self.openPath = os.path.dirname(fname[0])
            file_name = os.path.basename(fname[0]).replace('.ifx', '')
            if file_name not in self.workRecord.keys():
                data_list = read_pickle_file(fname[0])
                grid_max, mesh = data_list
                idx = self.desk.canvas.openPaintArea(grid_max, mesh, file_name)
                self.workRecord[file_name] = \
                {'path':fname[0], 'index':idx, 'done':True}
            else:
                index = self.workRecord[file_name]['index']
                self.desk.canvas.tabs.setCurrentIndex(index)
        
    def saveFile(self):
        grid_max, mesh, file_name = self.desk.canvas.savePaintArea()
        data_list = [grid_max, mesh]
        if self.workRecord[file_name]['path'] == None:
            self.saveAsFile()
        else:
            write_pickle_file(self.workRecord[file_name]['path'], data_list)
            self.workRecord[file_name]['done'] = True
            
    def saveAsFile(self):
        self.workingDirCheck()
        fname = QFileDialog.getSaveFileName(self, 'Save File', self.openPath,
                                            "Isometric File Extension (*.ifx)")
        if fname[0]:
            #!
            index = self.desk.canvas.tabs.currentIndex()
            file_name = self.desk.canvas.tabs.tabText(index)
            self.workRecord.pop(file_name)
            
            self.openPath = os.path.dirname(fname[0])
            file_name = os.path.basename(fname[0]).replace('.ifx', '')
            grid_max, mesh, _ = self.desk.canvas.savePaintArea(file_name)            
            data_list = [grid_max, mesh]
            write_pickle_file(fname[0], data_list)
            self.workRecord[file_name] = \
            {'path':fname[0], 'index':self.desk.canvas.tabs.currentIndex(),
             'done':True}
            
    def closeFile(self, index=None):
        if index is False:
            # Exicute from menu
            index = self.desk.canvas.tabs.currentIndex()
        file_name = self.desk.canvas.tabs.tabText(index)
        if self.isWorkDone(file_name):     
            self.workRecord.pop(file_name)
            self.desk.canvas.tabs.removeTab(index)
        else:
            #!
            # Show warning to save
            msg = QMessageBox()
            msg.setWindowIcon(QIcon(get_asset_dir('icon.png')))
            msg.setIcon(QMessageBox.Question)
            msg.setText("%s has been modified.\n Do you want to save changes"
                        %file_name)
            msg.setWindowTitle("Closing Tab")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No
                                   | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.closeMessage)
            msg.exec_()
            
    def closeMessage(self, btn_clicked):
        if btn_clicked.text() == '&Yes':
            self.saveFile()
        elif btn_clicked.text() == '&No':
            #!
            print('No')
        elif btn_clicked.text() == 'Cancel':
            pass
    
    
    def isWorkDone(self, file_name):
        if self.workRecord[file_name]['done']:
            return True
        else:
            return False
    
    def isWorkAllDone(self):
        allDone = True
        for key in self.workRecord.keys():
            allDone = allDone and self.workRecord[key]['done']
        if allDone:
            return True
        else:
            return False
        
    def quitWin(self):
        #if condition:
        if self.isWorkAllDone():
            QCoreApplication.instance().quit()
        else:
            #!
            # Show warning to save
            print('save please?!')
            
    def closeEvent(self, event):
        #if condition:
        if self.isWorkAllDone():
            event.accept() # let the window close
        else:
            #!
            # Show warning to save
            print('save please?!')
            event.ignore()
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ip = IsometricPainter()
    sys.exit(app.exec_())
