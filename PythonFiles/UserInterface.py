"GUI"

"""
to do :
expand click for index 
update mouse click for adaptable
fix max and ideal
animation matplots
ideals out of frame
inherit
closeall after main
import changes
pep8 http://pep8online.com/checkresult
pure functions
comments
"""

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
matplotlib.use('TkAgg') # speed increase

# modules
import Adviser
import Files

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # param
        self.UI = UI(self)
        self.setCentralWidget(self.UI)
        size = app.primaryScreen().size()
        self.setMinimumSize(size.width(), size.height()/2)
        self.showMaximized()
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
        text_size_Up.triggered.connect(self.text_size)
        SettingsMenu.addAction(text_size_Up)

        self.font = QFont()
        self.text_size_value = 9
        text_size_Down = QAction("Text Size Down",self)
        text_size_Down.triggered.connect(self.text_size)
        SettingsMenu.addAction(text_size_Down)

        self.color = ""
        self.Light_Dark()
        Light_Dark = QAction("Light/Dark",self)
        Light_Dark.triggered.connect(self.Light_Dark)
        SettingsMenu.addAction(Light_Dark)

        # Help menu
        HelpMenu = MainMenu.addMenu('Help')

        Documentation = QAction("Open documentation",self)
        Documentation.triggered.connect(lambda: os.system('start Documentation'))
        HelpMenu.addAction(Documentation)

        # testing
        self.Open(['C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Compost 15mm 2018.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Compost 15mmm 2018_Office.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Compost 25mm 2018.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Compost Geelong Sample.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Ideal.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole Dam.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole Elephant Track.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole Little.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole Mail Box.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole School.xlsx'])
        # self.Open(['C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Compost.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Ideal.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Soil.xlsx'])

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

    def text_size(self):
        change = 1
        try:
            if self.sender().text() == "Text Size Up":
                self.text_size_value += change
            elif self.sender().text() == "Text Size Down":
                if self.text_size>change:
                    self.text_size_value += -change
        except:
            pass
        self.UI.setStyleSheet("font: "+str(self.text_size_value)+"pt")
        rcParams.update({'font.size': self.text_size_value + 3})
        self.UI.update_graph()

    def Light_Dark(self):
        if self.color == "#EBEBEB":
            self.color = "#70706D"
        else:
            self.color = "#EBEBEB"
        try:
            self.DragDrop.setStyleSheet("QWidget { background-color: "+self.color+" }")
        except:
            pass
        self.setStyleSheet("QWidget { background-color: "+self.color+" }")
        self.UI.ax.set_facecolor(self.color)
        self.UI.fig.set_facecolor(self.color)
        self.UI.update_graph()

class QCustomSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._min_value = 0.00
        self._max_value = 0.05
        self._max_int = 1000

        super().setMinimum(0)
        super().setMaximum(self._max_int)

    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super().value()) / self._max_int * self._value_range() + self._min_value

    def setValue(self, value):
        super().setValue(int((value - self._min_value) / self._value_range() * self._max_int))

    # https://github.com/PyQt5/PyQt/blob/master/QSlider/ClickJumpSlider.py
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            option = QStyleOptionSlider()
            self.initStyleOption(option)
            rect = self.style().subControlRect(
                QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
            if rect.contains(event.pos()):
                super(QCustomSlider, self).mousePressEvent(event)
                return
            setValue = self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                (self.height() - event.y()) if not self.invertedAppearance( 
                ) else event.y(), self.height())
            super().setValue(setValue)
        else:
            MainWindow.UI.mousePressEvent(event)

class UI(QWidget):
    def __init__(self, parent=MainWindow):
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

        self.slider_links = []
        self.current_slider_links = []
        self.color_options = []
        self.colors = []
        self.color_pos = 0
        self.index = 0
    
        # viridis for color blind
        cmap = cm.get_cmap('viridis', 8)
        for i in range(cmap.N):
            rgb = cmap(i)[:3]
            self.color_options.append(matplotlib.colors.rgb2hex(rgb))

    def create_slider(self,path):

        for x in self.slider_links:
            if path == x:
                return None
            
        self.slider_links.append(path)
        self.current_slider_links.append(path)
        slider = QSlider(Qt.Vertical)
        custom_slider = QCustomSlider(slider)

        if self.color_pos == len(self.color_options):
            self.color_pos = 0
        hex_color = self.color_options[self.color_pos]
        self.color_pos += 1
        self.colors.append(hex_color)
        custom_slider.setStyleSheet("QSlider::handle:vertical {background-color: "+hex_color+";}")
        custom_slider.valueChanged.connect(lambda: self.update_graph()) # change after animation
        
        button = QPushButton()
        button.setStyleSheet("QPushButton:hover:!pressed { border: 2px solid red; }")
        name = os.path.basename(path).replace(".xlsx","")
        name = name.replace(" ","\n")
        button.setText(name)
        button.clicked.connect(lambda: self.delete_slider(button)) 
        
        self.sliders.addWidget(custom_slider)
        self.buttons.addWidget(button) 
        self.values.addWidget(QLabel("0 T/Ha"))

    def delete_slider(self, button):
        index = self.buttons.indexOf(button)
        self.buttons.itemAt(index).widget().setParent(None)
        self.sliders.itemAt(index).widget().setParent(None)
        self.values.itemAt(index).widget().setParent(None)
        del self.slider_links[index]
        del self.colors[index]
        self.update_graph()

    def graph_init(self):
        self.graph  = QVBoxLayout()
        self.Layout.addLayout(self.graph)

        self.fig = Figure()
        self.fig.set_tight_layout(True)
        canvas = FigureCanvas(self.fig)
        self.graph.addWidget(canvas)

        toolbar = NavigationToolbar2QT(canvas, self)
        self.graph.addWidget(toolbar)

        self.ax = canvas.figure.subplots()
        self.soil_link = r""
        self.ideal_link = r""
        self.update_graph()

    def update_graph(self):  
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
            ys = Files.run(self.slider_links[index])[0]*slider_value
            self.ax.bar(xs, ys, bottom=values_sum, color=self.colors[index], edgecolor='black')
            values_sum += ys
            T_Ha = round(1330*slider_value,1)
            self.values.itemAt(index).widget().setText(str(T_Ha)+"T/Ha")

        self.ax.bar(xs, self.IdealValues, facecolor="None", edgecolor='green')
        self.ax.bar(xs, self.IdealValues*4, facecolor="None", edgecolor='red')
        self.ax.set_xticks(xs)
        self.ax.set_xticklabels(self.names)
        self.ax.figure.canvas.draw()

    def context_menu_init(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)

        sliders_reset = QAction("sliders reset", self)
        sliders_reset.triggered.connect(self.sliders_reset)
        self.addAction(sliders_reset)
        
        auto_ideal = QAction("auto ideal", self)
        auto_ideal.triggered.connect(self.auto_ideal)
        self.addAction(auto_ideal)

        auto_max = QAction("auto max", self)
        auto_max.triggered.connect(self.auto_max)
        self.addAction(auto_max)

    # def mouseActivation(self):
    #     print("mouseActivation")

    # def QContextMenuEvent(self, event):
    #     print("QContextMenuEvent")
    #     print(event)

    # def contextMenuEvent(self, event):
    #     print("contextMenuEvent")
    #     print(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.current_slider_links = self.slider_links
            width = 125 #
            # Widget = QApplication.widgetAt(event.globalPos())
            # width = Widget.frameGeometry().width() 
            # print(width)
            index = int( event.globalX() / width )
            print(index)
            if index < len(self.slider_links):
                self.current_slider_links = [self.slider_links[index]]

    def sliders_reset(self):
        for i in range(len(self.current_slider_links)):
            index = self.slider_links.index(self.current_slider_links[i])
            self.sliders.itemAt(index).widget().setValue(0)

    def auto_ideal(self):
        # get soil
        change_vector = self.IdealValues-self.soilValues
        # get slider values
        sub_vectors = np.zeros(len(change_vector)) 
        for i in range(len(self.current_slider_links)):
            values = Files.run(self.current_slider_links[i])[0]
            slider_value = self.sliders.itemAt(i).widget().value()
            change_vector -= values * slider_value
            sub_vectors = np.vstack((sub_vectors, values))
        # run
        index, setValue = Adviser.run(change_vector,sub_vectors[1:])
        if setValue == None:
            return None
        if len(self.current_slider_links) == 1:
            index = self.slider_links.index(self.current_slider_links[0])
        # update 
        self.sliders.itemAt(index).widget().setValue(setValue)

    def auto_max(self):
        setValueMax = 0
        indexMax = -1
        for index in range(len(self.current_slider_links)):
            change_vector = self.IdealValues*4-self.soilValues
            values = Files.run(self.current_slider_links[index])[0]
            setValue = np.amin(change_vector/values)
            if setValueMax<setValue:
                setValueMax = setValue  
                indexMax = index
        if len(self.current_slider_links) == 1:
            indexMax = self.slider_links.index(self.current_slider_links[0])
        print(setValueMax)
        self.sliders.itemAt(indexMax).widget().setValue(setValueMax)
                
class DragDrop(QLineEdit):
    def __init__(self):
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
        for x in range(len(urls)):
            url = str(urls[x].path())[1:]
            if url[-5:].upper() == ".XLSX":
                full_paths.append(url)
        MainWindow.Open(full_paths)
        self.close()

if __name__=='__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
    