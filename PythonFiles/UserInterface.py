"GUI"

import os
import sys
import re
import numpy as np
from pylab import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import *
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

# modules
import Adviser
import Files

# pep8, 

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # globals
        self.color = "black" # opposite
        self.font = QFont()
        self.text_size = 10

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

        text_size_Up = QAction("Text Size Up",self)
        text_size_Up.triggered.connect(self.change_text_size)
        SettingsMenu.addAction(text_size_Up)

        text_size_Down = QAction("Text Size Down",self)
        text_size_Down.triggered.connect(self.change_text_size)
        SettingsMenu.addAction(text_size_Down)

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
            if re.search("IDEAL", name.upper()):
                self.UI.ideal_link = full_path
            elif re.search("SOIL", name.upper()):
                self.UI.soil_link = full_path
            else:
                self.UI.create_slider(full_path)
        self.UI.update_graph()

    def DragAndDrop(self):
        self.DragDrop = DragDrop()

    def change_text_size(self):
        change = 1
        if self.sender().text() == "Text Size Up":
            self.text_size += change
        else:
            if self.text_size>change:
                self.text_size += -change
        self.UI.setStyleSheet("font: "+str(self.text_size)+"pt")
        # matplotlib

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
        self.UI.update_graph()

class UI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Layout = QHBoxLayout()
        self.setLayout(self.Layout)

        self.slider_init()
        self.graph_init()
        self.context_menu_init()

    def slider_init(self):
        self.slider_layout = QVBoxLayout()
        self.Layout.addLayout(self.slider_layout)

        self.sliders = QHBoxLayout()
        self.buttons = QHBoxLayout()
        self.values = QHBoxLayout()

        self.slider_layout.addLayout(self.sliders)
        self.slider_layout.addLayout(self.buttons)
        self.slider_layout.addLayout(self.values)

        self.sliderLinks = []
        self.color_options = []
        self.colors = []
        self.color_pos = 0
    
        # viridis for color blind
        cmap = cm.get_cmap('viridis', 8)
        for i in range(cmap.N):
            rgb = cmap(i)[:3]
            self.color_options.append(matplotlib.colors.rgb2hex(rgb))

    def create_slider(self,path):

        for x in self.sliderLinks:
            if path == x:
                return None
            
        self.sliderLinks.append(path)
        # QProxyStyle QJumpSlider
        slider = QSlider(Qt.Vertical)

        hex_color = self.color_options[self.color_pos]
        if self.color_pos == len(self.color_options):
            self.color_pos = 0
        self.color_pos += 1
        self.colors.append(hex_color)
        slider.setStyleSheet("QSlider::handle:vertical {background-color: "+hex_color+";}")

        slider.setMaximum(5/100 * self.sliderTicks)
        slider.setValue(0)
        slider.setMinimum(0)
        slider.valueChanged.connect(self.update_graph) # remove after animation
        
        button = QPushButton()
        name = os.path.basename(path).replace(".xlsx","")
        button.setText(name)
        button.clicked.connect(lambda: self.delete_slider(button)) 
        
        self.sliders.addWidget(slider) # slider
        self.buttons.addWidget(button) # button
        self.values.addWidget(QLabel("0 T/Ha")) # value

    def delete_slider(self, button):
        index = self.buttons.indexOf(button)
        self.buttons.itemAt(index).widget().setParent(None)
        self.sliders.itemAt(index).widget().setParent(None)
        self.values.itemAt(index).widget().setParent(None)
        del self.sliderLinks[index]
        del self.colors[index]
        self.update_graph()

    def graph_init(self):
        # fix zoom 
        self.graph  = QVBoxLayout()
        self.Layout.addLayout(self.graph)

        self.fig = Figure()
        self.fig.set_tight_layout(True)
        canvas = FigureCanvas(self.fig)
        self.graph.addWidget(canvas)

        # optional
        toolbar = NavigationToolbar2QT(canvas, self)
        self.graph.addWidget(toolbar)

        self.ax = canvas.figure.subplots()
        self.soil_link = r""
        self.ideal_link = r""
        self.sliderTicks = 10**4
        self.update_graph()
        # FuncAnimation(self.fig, update_graph)

    def update_graph(self):  # use animation
        # if avoids try but adds color bug
        try:
            self.soilValues, self.names = Files.run(self.soil_link)
        except:
            pass
        try:
            self.IdealValues, self.names = Files.run(self.ideal_link)
        except:
            pass
    
        self.ax.clear()

        xs = np.arange(len(self.names))
        self.ax.bar(xs, self.soilValues, color = "grey")

        values_sum = self.soilValues
        for index in range(self.sliders.count()):
            slider_value = self.sliders.itemAt(index).widget().value()
            ys = Files.run(self.sliderLinks[index])[0]*slider_value/self.sliderTicks
            self.ax.bar(xs, ys, bottom=values_sum, color=self.colors[index], edgecolor='black')
            values_sum += ys
            T_Ha = round(1330*slider_value/self.sliderTicks,1)
            self.values.itemAt(index).widget().setText(str(T_Ha)+"T/Ha")

        self.ax.bar(xs, self.IdealValues, facecolor="None", edgecolor='green') # want out of frame
        self.ax.bar(xs, self.IdealValues*4, facecolor="None", edgecolor='red') # want out of frame
        self.ax.set_xticks(xs)
        self.ax.set_xticklabels(self.names)
        self.ax.figure.canvas.draw()

    def context_menu_init(self):
        pass

class DragDrop(QLineEdit):
    def __init__(self):
        # inherit
        super(DragDrop, self).__init__()
        self.setGeometry(200,200,200,200)
        self.setStyleSheet("QWidget { background-color: "+MainWindow.color+" }")
        self.setText("Drag and drop here")
        self.setDragEnabled(True)
        self.show()

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
                url = str(urls[x].path())[1:]
                if url[-1*len(".XLSX"):].upper() == ".XLSX":
                    full_paths.append(url)
                else:
                    print("This is not a .xlsx file")
            MainWindow.Open(full_paths)
            # exit window

if __name__=='__main__':
    # close all windows after mains
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())