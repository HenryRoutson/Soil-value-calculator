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
        # Shorten with loop over list of names

        MainMenu = self.menuBar()
        # File Menu
        FileMenu = MainMenu.addMenu('File')

        Save = QAction("Save",self)
        Save.triggered.connect(self.Save)
        FileMenu.addAction(Save)

        Open = QAction("Open",self)
        Open.triggered.connect(self.Open)
        FileMenu.addAction(Open)

        Drop = QAction("Drop",self)
        Drop.triggered.connect(self.Drop)
        FileMenu.addAction(Drop)
        
        Quit = QAction("Quit",self)
        Drop.triggered.connect(self.Quit)
        FileMenu.addAction(Quit)

        # Settings menu
        SettingsMenu = MainMenu.addMenu('Settings')

        Compound_Settings = QAction("Compound Settings",self)
        Compound_Settings.triggered.connect(self.Compound_Settings)
        SettingsMenu.addAction(Compound_Settings)

        Text_Size_Up = QAction("Text Size Up",self)
        Text_Size_Up.triggered.connect(self.Text_Size_Up)
        SettingsMenu.addAction(Text_Size_Up)

        Text_Size_Down = QAction("Text Size Down",self)
        Text_Size_Up.triggered.connect(self.Text_Size_Down)
        SettingsMenu.addAction(Text_Size_Down)

        Light_Dark = QAction("Light/Dark",self)
        Light_Dark.triggered.connect(self.Light_Dark)
        SettingsMenu.addAction(Light_Dark)

        # Help menu
        HelpMenu = MainMenu.addMenu('Help')

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

    def Compound_Settings(self):
        print("Compound_Settings")

    def Text_Size_Up(self):
        print()

    def Text_Size_Down(self):
        print()
        # matplotlib.rcParams.update({'font.size': 22})

    def Light_Dark(self):
        print("")
    
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

        self.Ax = canvas.figure.subplots()
 
    def _update_canvas(self):

        self.Ax.clear()
        # add dragdrop
        # make borders smaller
        # get files from user
        CompostLink = r"ExcelFiles\Compost 15mm 2018.xlsx"
        SoilLink = r"ExcelFiles\Soil N.Cole Dam.xlsx"
        # run module
        CompostValues, CompostNames = Files.run(CompostLink)
        SoilValues, SoilNames = Files.run(SoilLink)
        # arbitrary
        Natural = np.arange(len(CompostValues))

        # set_xticklabels not working
        # fix graphing scale
        self.Ax.set_xticklabels(CompostNames)
        self.Ax.bar(Natural, SoilValues)
        self.Ax.bar(Natural, CompostValues*CompostSlider.value()/(10*4), bottom = SoilValues, color = "grey")

        self.Ax.figure.canvas.draw()

if __name__=='__main__':

    App = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(App.exec_())