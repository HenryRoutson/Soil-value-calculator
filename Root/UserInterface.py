"""
to do :
fix max and ideal
fix vibrating and fix zoom glitch
pep8 http://pep8online.com/checkresult
"""

import os
import sys
import re
import shutil
import numpy as np
from pylab import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import *
from matplotlib.figure import Figure
import matplotlib.animation as animation
matplotlib.use('TkAgg') # fastest backend

# modules
import Adviser
import Files


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        "MainWindow preferences"

        # look
        self.text_size = 9.5
        self.main_color = -1 # the next index color is used on start
        self.main_colors = ["#EBEBEB","#9c9c9c","#363636"]
        self.setWindowTitle('GUI')
        self.setWindowIcon(QIcon('pythonlogo.png'))
        # size
        size = app.primaryScreen().size()
        self.setMinimumSize(size.width(), size.height()/2)
        self.showMaximized()
        # functional
        self.Widgets = Widgets(self)
        self.setCentralWidget(self.Widgets)

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

        self.font = QFont()
        text_size_Down = QAction("Text Size Down",self)
        text_size_Down.triggered.connect(self.change_text_size)
        SettingsMenu.addAction(text_size_Down)

        self.light_dark()
        light_dark = QAction("Light/Dark",self)
        light_dark.triggered.connect(self.light_dark)
        SettingsMenu.addAction(light_dark)

        # Help menu
        HelpMenu = MainMenu.addMenu('Help')

        Documentation = QAction("Open documentation",self)
        Documentation.triggered.connect(lambda: os.system('start Documentation'))
        HelpMenu.addAction(Documentation)

        # Open on launch
        # self.Open(['C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Compost 15mm 2018.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Compost 15mmm 2018_Office.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Compost 25mm 2018.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Compost Geelong Sample.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Ideal.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole Dam.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole Elephant Track.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole Little.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole Mail Box.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFiles/Soil N.Cole School.xlsx'])
        # self.Open(['C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Compost.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Ideal.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Soil.xlsx'])
        self.Open(['C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Compost_Testing_ContextMenu.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Ideal_Testing_ContextMenu.xlsx', 'C:/Users/henryro/OneDrive - Ballarat Grammar School/2019 Software/Sat/ExcelFilesTesting/Soil_Compost_ContextMenu.xlsx'])

    def Open(self, full_paths):
        # if there are no paths from drag drop
        if full_paths == False:
            # open the file menu
            full_paths = QFileDialog.getOpenFileNames(self,'Open File')[0]
            print(full_paths)

        # delete non xlsx (excel) files
        for i, url in enumerate(full_paths):
            if url[-5:].upper() != ".XLSX":
                del full_paths[i]

        # copy paths to AllExcelFilesBackup
        # update paths for graph and start
        for full_path in full_paths:
            # try avoids already there type file errors
            try:
                shutil.copy(full_path, "Root\AllExcelFilesBackup")
            except:
                pass
            name =  os.path.basename(full_path)
            if re.search("IDEAL", name.upper()):
                self.Widgets.ideal_path = full_path
            elif re.search("SOIL", name.upper()):
                self.Widgets.soil_path = full_path
            else:
                self.Widgets.create_slider(full_path)
        self.Widgets.start_graph()

    def DragAndDrop(self):
        self.DragDrop = DragDrop()
        self.Widgets.start_graph()

    # called on mainwindow close
    def closeEvent(self, event):
        # try avoids error if DragDrop is not open
        try:
            self.DragDrop.close()
        except:
            pass

    def change_text_size(self):

        change = 0.5
        if self.sender().text() == "Text Size Up":
            self.text_size += change
        elif self.sender().text() == "Text Size Down":
            if self.text_size>change:
                self.text_size += -change

        self.Widgets.setStyleSheet("font: "+str(self.text_size)+"pt")
        matplotlib.rcParams.update({'font.size': self.text_size + 2.5 })
        self.Widgets.start_graph()

    def light_dark(self):
        if self.main_color >= len(self.main_colors)-1:
            self.main_color = 0
        else:
            self.main_color += 1

        self.setStyleSheet("QWidget { background-color: "+self.main_colors[self.main_color]+" }")
        self.Widgets.ax.set_facecolor(self.main_colors[self.main_color])
        self.Widgets.fig.set_facecolor(self.main_colors[self.main_color])
        self.Widgets.start_graph()
       
class QCustomSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # super is used to refer to the QSlider parent
        self.max_float = 0.05
        super().setMinimum(0)
        super().setMaximum(1000)
        
    # used for directly setting float values
    def value(self):
        return super().value() / super().maximum() * self.max_float

    def setValue(self, value):
        super().setValue( int( value / self.max_float * super().maximum() ) )

    # allows click to position 
    # mousePressEvent code is from:
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

class Widgets(QWidget):
    def __init__(self, parent=MainWindow):
        super().__init__(parent)

        "Widgets preferences"

        # functional
        self.max_div_ideal = 4
        self.label_conversion = 1330 # 1330T T/Ha soil * percent compost added to soil
        self.label_unit = " T/Ha"

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
        self.labels = QHBoxLayout()

        self.slider_layout.addLayout(self.sliders)
        self.slider_layout.addLayout(self.buttons)
        self.slider_layout.addLayout(self.labels)

        self.all_slider_paths = []
        self.slider_paths = []
        self.all_slider_colors = []
        self.slider_colors = []
        self.slider_color_pos = 0
    
        # viridis for color blind
        # number can be set higher for more colors that are closer together
        cmap = cm.get_cmap('viridis', 10) 
        for i in range(cmap.N):
            rgb = cmap(i)[:3]
            self.all_slider_colors.append(matplotlib.colors.rgb2hex(rgb))

    def create_slider(self,path):

        # avoid duplicates
        for x in self.all_slider_paths:
            if path == x:
                return None
            
        self.all_slider_paths.append(path)
        # slider_paths is subset of all_slider_paths
        # and is used to get ideal values for example, on a single slider
        self.slider_paths.append(path)

        # create slider
        slider = QSlider(Qt.Vertical)
        custom_slider = QCustomSlider(slider)

        # color
        # go to start if out of colors
        if self.slider_color_pos >= len(self.all_slider_colors)-1:
            self.slider_color_pos = 0
        hex_color = self.all_slider_colors[self.slider_color_pos]
        self.slider_color_pos += 1
        self.slider_colors.append(hex_color)
        custom_slider.setStyleSheet("QSlider::handle:vertical {background-color: "+hex_color+";}")
        
        button = QPushButton()
        button.setStyleSheet("QPushButton:hover:!pressed { border: 2px solid red; }")
        name = os.path.basename(path).replace(".xlsx","")
        name = name.replace(" ","\n")
        button.setText(name)
        button.clicked.connect(lambda: self.delete_slider(button)) 
        
        self.sliders.addWidget(custom_slider)
        self.buttons.addWidget(button) 
        self.labels.addWidget(QLabel("0 T/Ha"))

    def delete_slider(self, button):
        index = self.buttons.indexOf(button)
        # GUI items are deleted first
        self.buttons.itemAt(index).widget().setParent(None)
        self.sliders.itemAt(index).widget().setParent(None)
        self.labels.itemAt(index).widget().setParent(None)
        self.bars[index].remove() # on graph
        del self.bars[index] # in memory
        del self.all_slider_paths[index]
        del self.slider_colors[index]

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
        self.soil_path = ""
        self.ideal_path = ""
        self.FuncAnimation = None

        # testing
        self.min_distance = 10**10

    def start_graph(self): 
        if self.soil_path == "" or self.ideal_path == "":
            return

        # graph is cleared to update things other than bar scale
        # updating these only when they are changed helps performance
        self.ax.clear()

        self.bars = []
        length = len(Files.values(self.soil_path)[0])
        # numpy arrays help performance 
        xs = np.arange(length) # 1,2,3
        ys = np.zeros(length) # 0,0,0

        # create bars
        for color in self.slider_colors:
            self.bars.append(self.ax.bar(xs, ys, color=color, edgecolor='black'))
        # using real values sets a propper frame
        self.bars.append(self.ax.bar(xs, Files.values(self.soil_path)[0], color = "grey"))
        self.bars.append(self.ax.bar(xs, Files.values(self.ideal_path)[0], facecolor="None", edgecolor='green'))
        self.bars.append(self.ax.bar(xs, Files.values(self.ideal_path)[0]*self.max_div_ideal, facecolor="None", edgecolor='red'))
        self.ax.set_xticks(xs)
        self.ax.set_xticklabels(Files.values(self.soil_path)[1])

        # Function animation is an optimized loop function that calls update_graph 
        # deletes old graph
        if self.FuncAnimation != None:  
            self.FuncAnimation.event_source.stop()
        # blit avoids a complete re-render and helps performance
        self.FuncAnimation = animation.FuncAnimation(self.fig,self.update_graph,interval=0,blit=True)

    def update_values(self, bars, values, bottom = []):
        for i, bar in enumerate(bars):
            bar.set_height(values[i])
        # set y raises the bar on top of the last
        if bottom != []:
            for i, bar in enumerate(bars):
                bar.set_y(bottom[i])

    def update_graph(self, frames):

        # testing
        distance = np.linalg.norm(self.get_vectors(1)[0])
        if distance < self.min_distance:
            print(distance)
            self.min_distance = distance

        bottom = Files.values(self.soil_path)[0]
        for i, slider_path in enumerate(self.all_slider_paths):
            slider_value = self.sliders.itemAt(i).widget().value()
            ys = Files.values(slider_path)[0] * slider_value
            self.update_values(self.bars[i], ys ,bottom)
            bottom += ys
            setText = ""
            setText = "...\n\n" # comment out if not wanted
            setText = setText + str(round(self.label_conversion*slider_value,1)) + self.label_unit
            self.labels.itemAt(i).widget().setText(setText)

        self.update_values(self.bars[-3], Files.values(self.soil_path)[0])
        self.update_values(self.bars[-2], Files.values(self.ideal_path)[0])
        self.update_values(self.bars[-1], Files.values(self.ideal_path)[0]*self.max_div_ideal)

        # returns single array of all subarrays to FuncAnimation
        return np.array(self.bars).ravel()
        
    def context_menu_init(self):
        self.context_menu = QMenu(self)

        reset_values = QAction("Reset values", self)
        reset_values.triggered.connect(self.reset_values)
        self.context_menu.addAction(reset_values)
        
        ideal_values = QAction("Ideal values", self)
        ideal_values.triggered.connect(self.ideal_values)
        self.context_menu.addAction(ideal_values)

        max_values = QAction("Max values", self)
        max_values.triggered.connect(self.max_values)
        self.context_menu.addAction(max_values)

    def contextMenuEvent(self, event):
        # if contextMenuEvent is above a slider button
        # set slider_paths to that slider_path
        # so ideal_values for example, will only run over that path
        # without needing a separate single path function
        
        self.slider_paths = self.all_slider_paths
        for index in range(self.buttons.count()):
            widget = self.buttons.itemAt(index).widget().geometry()
            if event.globalX() < widget.x() + widget.width():
                if index < len(self.all_slider_paths):
                    self.slider_paths = [self.all_slider_paths[index]]
                break
        self.context_menu.exec_(self.mapToGlobal(event.pos()))

    def reset_values(self):
        for i, slider_path in enumerate(self.slider_paths):
            index = self.all_slider_paths.index(slider_path)
            self.sliders.itemAt(index).widget().setValue(0)

    def get_vectors(self, scalar):
        change_vector = Files.values(self.ideal_path)[0] * scalar - Files.values(self.soil_path)[0]
        # create an array to append to
        sub_vectors = np.zeros(len(change_vector))
        # and for each of the vectors 
        for i, slider_path in enumerate(self.slider_paths):
            values = Files.values(slider_path)[0]
            slider_value = self.sliders.itemAt(i).widget().value()
            # update the change vector
            change_vector -= values * slider_value
            # and append the slider vector
            sub_vectors = np.vstack((sub_vectors, values))
        return change_vector, sub_vectors[1:]

    def ideal_values(self):
        change_vector, sub_vectors = self.get_vectors(1)
        
        index, setValue = Adviser.run(change_vector,sub_vectors)
        # if the advisor doesn't have a change to improve
        if setValue == None:
            # exit function
            return None

        # if this is a contextMenuEvent path
        # eg [[path]]
        if len(self.slider_paths) == 1:
            # make sure its index isn't always 0
            index = self.all_slider_paths.index(self.slider_paths[0])

        # add the value the slider is already on and setValue
        setValue += self.sliders.itemAt(index).widget().value()
        self.sliders.itemAt(index).widget().setValue(setValue)

    def max_values(self):
        change_vector, sub_vectors = self.get_vectors(self.max_div_ideal)
        setValue, index = 0, 0 

        # find the which compost can be put on the most witout going over limits:
        # for each of the vectors
        for i, sub_vector in enumerate(sub_vectors):
            # find the value that first goes over the limit and when
            if np.linalg.norm(sub_vector) == 0:
                continue
            limit = np.amin(change_vector/sub_vector)
            # if limit takes longer to go over the limit than previous sliders
            if setValue < limit:
                # make it the new set value
                setValue = limit  
                # and slider
                index = i

        # if there is a single path, update the index 
        if len(self.slider_paths) == 1:
            index = self.all_slider_paths.index(self.slider_paths[0])

        # add the value the slider is already on and set
        setValue += self.sliders.itemAt(index).widget().value()
        self.sliders.itemAt(index).widget().setValue(setValue)
   
class DragDrop(QLineEdit):
    def __init__(self):
        super(DragDrop, self).__init__()
        # dark mode not included for simplicity
        self.setGeometry(200,200,200,200)
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
        full_paths = []
        for x, url in enumerate(urls):
            full_paths.append(str(url.path())[1:])
        MainWindow.Open(full_paths)
        self.close()

if __name__=='__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
