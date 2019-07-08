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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # global
        self.color = "white"
        self.text_size = 14

        # param
        self.UI = UI(self)
        self.setCentralWidget(self.UI)

        'Menubar'
        
        MainMenu = self.menuBar()
        # File Menu
        FileMenu = MainMenu.addMenu('File')

        Save = QAction("Save",self)
        Save.triggered.connect(self.Save)
        FileMenu.addAction(Save)

        Open = QAction("Open",self)
        Open.triggered.connect(self.Open)
        FileMenu.addAction(Open)

        DragAndDrop = QAction("Drag&Drop",self)
        DragAndDrop.triggered.connect(self.DragAndDrop)
        FileMenu.addAction(DragAndDrop)
        
        Quit = QAction("Quit",self)
        Quit.triggered.connect(lambda: exit())
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

    def Open(self, full_path):
        if full_path == False:
            full_path = QFileDialog.getOpenFileName(self,'Open File')[0]
        name =  os.path.basename(full_path)
        print(name)
        if re.search("IDEAL", name.upper()):
            print("ideal")
            ideal_link = full_path
        elif re.search("SOIL", name.upper()):
            print("soil")
            global soil_link
            soil_link = full_path
        else:
            print("other")
            # Create slider and bar
        # update graphs
                
    def DragAndDrop(self):
        self.DragDropWindow = DragDrop()
        self.DragDropWindow.show()
    
    def update_text_size(self):
        print(self.text_size)
        matplotlib.rcParams.update({'font.size': self.text_size})

    def Text_Size_Up(self):
        self.text_size += 1   
        update_text_size(self)     
        
    def Text_Size_Down(self):
        self.text_size += -1
        update_text_size(self)

    def Light_Dark(self):
        if self.color == "white":
            self.color = "darkGrey"
        else:
            self.color = "white"

        self.setStyleSheet("QWidget { background-color: "+self.color+" }")
        # not working 
        self.UI.setStyleSheet("QWidget { background-color: "+self.color+" }")
        self.UI.ax.set_facecolor(self.color)

    def Search(self):
        print("Search")

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
        COMPOST_SLIDER.valueChanged.connect(self._update_graph)
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
        global compost_link
        compost_link = r"ExcelFiles\Compost 15mm 2018.xlsx"
        global soil_link
        soil_link = r"ExcelFiles\Soil N.Cole Dam.xlsx"
        self._update_graph()

    def _update_graph(self):
        self.ax.clear()
        # add dragdrop
        SoilValues, SoilNames = Files.run(soil_link)
        Natural = np.arange(len(SoilValues))
        # set_xticklabels not working
        self.ax.set_xticklabels(SoilValues)
        self.ax.bar(Natural, SoilValues)
        # for x in compound
        CompostValues, CompostNames = Files.run(compost_link)
        self.ax.bar(Natural, CompostValues*COMPOST_SLIDER.value()/(10*4), bottom = SoilValues, color = "grey")
        # use sci notation
        fig.tight_layout()
        self.ax.figure.canvas.draw()

class DragDrop(QLineEdit):
    def __init__(self):
        super(DragDrop, self).__init__()
        self.setGeometry(200,200,200,200)
        self.setText("Drag and drop here")
        self.setDragEnabled(True)

    # simplify functions
    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        # add support for multiple drops 
        print()
        print(event)
        data = event.mimeData()
        print(data)
        urls = data.urls()
        print(urls)
        if urls and urls[0].scheme() == 'file':
            filepath = str(urls[0].path())[1:]
            if filepath[-5:].upper() == ".XLSX":
                MainWindow.Open(filepath)
            else:
                print("This is not a .xlsx file")
                
if __name__=='__main__':

    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())