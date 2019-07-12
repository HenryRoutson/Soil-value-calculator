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

        # globals
        self.color = "black"
        self.text_size = 14

        # param
        self.UI = UI(self)
        self.setCentralWidget(self.UI)
        self.showMaximized()
        self.Light_Dark()
        self.setWindowTitle('GUI')
        self.setWindowIcon(QIcon('pythonlogo.png'))

        'Menubar'

        MainMenu = self.menuBar()
        # File Menu
        FileMenu = MainMenu.addMenu('File')

        Open = QAction("Open",self)
        Open.triggered.connect(self.Open)
        FileMenu.addAction(Open)

        DragAndDrop = QAction("Drag&Drop Open",self)
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

        Documentation = QAction("Open documentation",self)
        Documentation.triggered.connect(lambda: os.system('start Documentation'))
        HelpMenu.addAction(Documentation)

    def Open(self, full_paths):
        if full_paths == False:
            full_paths = QFileDialog.getOpenFileNames(self,'Open File')[0]
        for full_path in full_paths:
            name =  os.path.basename(full_path)
            print(name)
            if re.search("IDEAL", name.upper()):
                print("ideal")
                self.UI.ideal_link = full_path
            elif re.search("SOIL", name.upper()):
                print("soil")
                self.UI.soil_link = full_path
            else:
                print("other")
                self.UI.sliders.append(full_path)
        self.UI._update_graph()

    def DragAndDrop(self):
        self.DragDrop = DragDrop()
        self.DragDrop.show()

    def update_text_size(self):
        pass
    # for x in self.UI.sliders:
    #     settextsize(self.text_size)
    # self.UI.fig.rcParams.update({'font.size': self.text_size})

    # not working
    # shorten with signals
    def Text_Size_Up(self):
        self.text_size += 1
        self.update_text_size()

    def Text_Size_Down(self):
        self.text_size += -1
        self.update_text_size()

    def Light_Dark(self):
        if self.color == "white":
            self.color = "#3D3D3D"
        else:
            self.color = "white"
        try:
            self.DragDrop.setStyleSheet("QWidget { background-color: "+self.color+" }")
        except:
            pass
        self.setStyleSheet("QWidget { background-color: "+self.color+" }")
        self.UI.setStyleSheet("QWidget { background-color: "+self.color+" }")
        self.UI.ax.set_facecolor(self.color)
        self.UI.fig.set_facecolor(self.color)
        self.UI._update_graph()

class UI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # inherit

        'Layouts'
        # MainLayout
        Layout = QHBoxLayout()
        self.setLayout(Layout)
        # Sublayouts

        "Add Slider"

        self.sliders = []

        # not working dynamically
        # remove exec
        # use as subclass
        def slider(self,name,color):
            SliderLayout = QVBoxLayout()
            Layout.addLayout(SliderLayout)
            exec("self."+name+" = QSlider(Qt.Vertical)")
            # set color
            # max/10**6
            exec("self."+name+".setMaximum(50000)")
            exec("self."+name+".setValue(0)")
            exec("self."+name+".setMinimum(0)")
            exec("self."+name+".valueChanged.connect(self._update_graph)")
            exec("self."+name+".setTickPosition(QSlider.TicksBelow)")
            exec("SliderLayout.addWidget(self."+name+")")
            SliderLayout.addWidget(QLabel(name))
            self.valueWidget = QLabel("0")
            SliderLayout.addWidget(self.valueWidget)
            # update graph

        slider(self,"Compost","lightBlue")

        GraphLayout  = QVBoxLayout()
        Layout.addLayout(GraphLayout)

        "Graph"
        self.fig = Figure()
        canvas = FigureCanvas(self.fig)
        GraphLayout.addWidget(canvas)

        # optional
        toolbar = NavigationToolbar2QT(canvas, self)
        GraphLayout.addWidget(toolbar)

        self.ax = canvas.figure.subplots()
        # avoid default
        self.soil_link = r"ExcelFiles\Soil N.Cole Little.xlsx"
        self.ideal_link = r"C:\Users\henryro\OneDrive - Ballarat Grammar School\2019 Software\Sat\ExcelFiles\Ideal.xlsx"
        self._update_graph()

    def _update_graph(self):
        self.ax.clear()

        # solid
        SoilValues, names = Files.run(self.soil_link)
        IdealValues, names = Files.run(self.ideal_link)
        Natural = np.arange(len(names))
        self.ax.bar(Natural, SoilValues, color = "grey")

        # for x in range
        # color = bar and slider
        # tonnes per hactare
        
        full_path = r"ExcelFiles\Compost Geelong Sample.xlsx"
        values, names = Files.run(full_path)
        # T/Ha
        self.valueWidget.setText(str(round(1330*self.Compost.value()/10**6,1)))
        self.ax.bar(Natural, values*self.Compost.value()/10**6, bottom = SoilValues)

        # outline
        
        self.ax.bar(Natural, IdealValues*4, facecolor="None", edgecolor='red', linewidth=0.5)
        self.ax.bar(Natural, IdealValues, facecolor="None", edgecolor='green', linewidth=0.5)

        self.ax.set_xticks(Natural)
        self.ax.set_xticklabels(names)
        self.fig.tight_layout()
        self.ax.figure.canvas.draw()

class DragDrop(QLineEdit):
    def __init__(self):
        # inherit
        super(DragDrop, self).__init__()
        self.setGeometry(200,200,200,200)
        self.setStyleSheet("QWidget { background-color: "+MainWindow.color+" }")
        self.setText("Drag and drop here")
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            full_paths = []
            for x in range(len(urls)):
                if filepath[-5:].upper() == ".XLSX":
                    full_paths.append(str(urls[x].path())[1:])
                else:
                    print("This is not a .xlsx file")
            MainWindow.Open(full_paths)

if __name__=='__main__':
    # close all windows after main
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())