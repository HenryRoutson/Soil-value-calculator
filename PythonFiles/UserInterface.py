"GUI"

import os
import sys 
import re 
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

global color
color = "white"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setCentralWidget(UI(self))
        # Change for dark mode
        
        self.setStyleSheet("QWidget { background-color: "+color+" }")

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

        DragDrop = QAction("Drag&Drop",self)
        DragDrop.triggered.connect(self.DragDrop)
        FileMenu.addAction(DragDrop)
        
        Quit = QAction("Quit",self)
        Quit.triggered.connect(self.Quit)
        FileMenu.addAction(Quit)

        # Settings menu
        SettingsMenu = MainMenu.addMenu('Settings')

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
        # To pick up again
        # what to open 
        # slider values 

    def Open(self):
        Path = QFileDialog.getOpenFileName(self,'Open File')[0]
        Type = Path.split("*").upper()
        if Type == "IDEAL":
            print("ideal")

        elif Type == "SOIL":
            print("soil")
            SoilLink = Path
        else:
            print(Type)
            # Add slider with type name
            # avoid overlapp

    def DragDrop(self):
        print("DragDrop")
        # open window
        
    def Quit(self):
        exit()

    def Text_Size_Up(self):
        print()

    def Text_Size_Down(self):
        print()
        # matplotlib.rcParams.update({'font.size': 22})

    def Light_Dark(self):
        # global
        global color
        if color == "white":
            color = "darkGrey"
        else:
            color = "white"
        # refer to self
        self.setStyleSheet("QWidget { background-color: "+color+" }")
        # update canvas
        # markerfacecolor='blue'

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
        
        global COMPOST_SLIDER
        COMPOST_SLIDER = QSlider(Qt.Vertical)
        # Int resrictions
        # use %%
        COMPOST_SLIDER.setMaximum(50)
        COMPOST_SLIDER.setValue(0)
        COMPOST_SLIDER.setMinimum(0)
        COMPOST_SLIDER.valueChanged.connect(self._update_canvas)
        COMPOST_SLIDER.setTickPosition(QSlider.TicksBelow)
        SliderLayout.addWidget(COMPOST_SLIDER)

        SliderLayout.addWidget(QLabel("Compost"))
    
        "Graph"
        global fig
        fig = Figure(figsize=(5, 3))
        canvas = FigureCanvas(fig)
        GraphLayout.addWidget(canvas)

        # optional
        toolbar = NavigationToolbar2QT(canvas, self)
        GraphLayout.addWidget(toolbar)

        self.ax = canvas.figure.subplots()
        global CompostLink
        CompostLink = r"ExcelFiles\Compost 15mm 2018.xlsx"
        global SoilLink
        SoilLink = r"ExcelFiles\Soil N.Cole Dam.xlsx"
 
    def _update_canvas(self):

        self.ax.clear()
        # add dragdrop
        # make borders smaller
        # get files from user
        
        # run module
        CompostValues, CompostNames = Files.run(CompostLink)
        SoilValues, SoilNames = Files.run(SoilLink)
        # arbitrary
        Natural = np.arange(len(CompostValues))

        # set_xticklabels not working
        # fix graphing scale
        self.ax.set_xticklabels(CompostNames)
        self.ax.bar(Natural, SoilValues)
        # for x in compound
        self.ax.bar(Natural, CompostValues*COMPOST_SLIDER.value()/(10*4), bottom = SoilValues, color = "grey")
        # use sci notation
        fig.tight_layout()

        self.ax.figure.canvas.draw()

class DragDrop(QLineEdit):
    def __init__(self):
        super(DragDrop, self).__init__()
        
        self.setDragEnabled(True)
        self.setWindowTitle("drop xlsx files")
        self.hide()

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if True:
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        dragEnterEvent(self, event)

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'xlsx':
            filepath = str(urls[0].path())[1:]
            # any file type here
            if filepath[-5:].upper() == ".xlsx":
                self.setText(filepath)
            else:
                print("Wrong file type")

if __name__=='__main__':

    App = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(App.exec_())