"GUI"

import os
import sys 
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import *
from matplotlib.figure import Figure

# modules
import Adviser
import Files

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setCentralWidget(UI(self))
        # Change for dark mode
        self.setStyleSheet("QWidget { background-color: white }")

        'Menubar'
        # actions not working 
        # combine to one loop
        mainMenu = self.menuBar()

        # File Menu
        fileMenu = mainMenu.addMenu('File')
        fileMenuList = ["Save","Open","Drop","Quit"]
        for x in fileMenuList:
            Name = x
            x = x.replace(" ","_")
            x = QAction(Name,self)
            x.triggered.connect(self.x)
            fileMenu.addAction(x)

        # Settings menu
        SettingsMenu = mainMenu.addMenu('Settings')
        SettingsMenuList = ["Compound Settings","Text Size Up","Text Size Down","Light/Dark"]
        for x in SettingsMenuList:
            Name = x
            x = x.replace(" ","_")
            x = QAction(Name,self)
            x.triggered.connect(self.x)
            SettingsMenu.addAction(x)

        # Help menu
        HelpMenu = mainMenu.addMenu('Help')
        Search = QAction("Search",self)
        Search.triggered.connect(self.Search)
        HelpMenu.addAction(Search)

    def Save(self):
        print("Saving")

    def Open(self):
        print("Opening")

    def Drop(self):
        print("Open file drop")

    def Quit(self):
        exit()
    
    def Search(self):
        print("helping")

class UI(QWidget):
    def __init__(self, parent=None): 
        super().__init__(parent)

        Layout = QHBoxLayout()
        self.setWindowTitle('GUI')
        self.setWindowIcon(QIcon('pythonlogo.png'))
        self.setAutoFillBackground(True)
        self.showMaximized()
        # Change for dark mode
        self.setStyleSheet("QWidget { background-color: white }")
        
        'Layouts'
        # MainLayout
        Layout = QHBoxLayout()
        self.setLayout(Layout)
        # Sublayouts
        SliderLayout = QVBoxLayout()
        Layout.addLayout(SliderLayout)
        GraphLayout  = QVBoxLayout()
        Layout.addLayout(GraphLayout)
        
        "Add Slider"
        # make modular
        global CompostSlider
        CompostSlider = QSlider(Qt.Vertical)
        # Int resrictions
        # use %%
        CompostSlider.setMaximum(500)
        CompostSlider.setValue(0)
        CompostSlider.setMinimum(0)
        CompostSlider.valueChanged.connect(self._update_canvas)
        CompostSlider.setTickPosition(QSlider.TicksBelow)
        # CompostSlider.setTickInterval(1)
        SliderLayout.addWidget(CompostSlider)

        SliderLayout.addWidget(QLabel("Compost"))
    
        "Graph"
        canvas = FigureCanvas(Figure(figsize=(5, 3)))
        GraphLayout.addWidget(canvas)

        # optional
        toolbar = NavigationToolbar2QT(canvas, self)
        GraphLayout.addWidget(toolbar)

        self.ax = canvas.figure.subplots()
 
    def _update_canvas(self):
        self.ax.clear()
        # add dragdrop
        # get files from user
        CompostLink = r"ExcelFiles\Compost 15mm 2018.xlsx"
        SoilLink = r"ExcelFiles\Soil N.Cole Dam.xlsx"
        # run module
        CompostValues, CompostNames = Files.run(CompostLink)
        SoilValues, SoilNames = Files.run(SoilLink)
        # arbitrary
        n = np.arange(len(CompostValues))

        # set_xticklabels not working
        # fix graphing scale
        self.ax.set_xticklabels(CompostNames)
        self.ax.bar(n, SoilValues)
        self.ax.bar(n, CompostValues*CompostSlider.value()/(10*4), bottom = SoilValues, color = "grey")
        print(CompostSlider.value()/(10*4))

        self.ax.figure.canvas.draw()

if __name__=='__main__':

    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())