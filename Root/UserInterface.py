__author__  = "Henry Routson"
__date__ = "2019-08-30"

# modules
import Adviser
import Files

# external
import os
import sys
import re
import shutil
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import matplotlib
from matplotlib import cm
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import *
from matplotlib.figure import Figure
import matplotlib.animation as animation
matplotlib.use('TkAgg')  # fastest backend


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        "MainWindow preferences"

        # look
        self.text_size = 9.5
        self.main_color = -1  # the next index color is used on start
        self.main_colors = ["#EBEBEB", "#9c9c9c", "#363636"]
        self.setWindowTitle('GUI')
        self.setWindowIcon(QIcon('pythonlogo.png'))
        # size
        size = app.primaryScreen().size()
        self.setMinimumSize(size.width(), size.height()/2)
        # self.showMaximized()
        # functional
        self.open_all = True  # open error files with zeros in gaps
        self.Widgets = Widgets(self)
        self.setCentralWidget(self.Widgets)

        'Menubar'

        MainMenu = self.menuBar()

        # File Menu
        FileMenu = MainMenu.addMenu('File')

        Open = QAction("Open", self)
        Open.triggered.connect(self.Open)
        FileMenu.addAction(Open)

        DragAndDrop = QAction("Drag&Drop Open", self)
        DragAndDrop.triggered.connect(self.DragAndDrop)
        FileMenu.addAction(DragAndDrop)

        Quit = QAction("Quit", self)
        Quit.triggered.connect(lambda: exit())
        FileMenu.addAction(Quit)

        # Settings menu
        SettingsMenu = MainMenu.addMenu('Settings')

        text_size_Up = QAction("Text Size Up", self)
        text_size_Up.triggered.connect(self.change_text_size)
        SettingsMenu.addAction(text_size_Up)

        self.font = QFont()
        text_size_Down = QAction("Text Size Down", self)
        text_size_Down.triggered.connect(self.change_text_size)
        SettingsMenu.addAction(text_size_Down)

        self.light_dark()
        light_dark = QAction("Light/Dark", self)
        light_dark.triggered.connect(self.light_dark)
        SettingsMenu.addAction(light_dark)

        # Help menu
        HelpMenu = MainMenu.addMenu('Help')

        Getting_started = QAction("Getting started", self)
        Getting_started.triggered.connect(lambda: os.system('start Documentation\Getting_started.docx'))
        HelpMenu.addAction(Getting_started)

        How_to_use_the_Program = QAction("How to use the Program", self)
        How_to_use_the_Program.triggered.connect(lambda: os.system('start Documentation\How_to_use_the_Program.docx'))
        HelpMenu.addAction(How_to_use_the_Program)

        Right_click_functions = QAction("Right click functions", self)
        Right_click_functions.triggered.connect(lambda: os.system('start Documentation\Right_click_functions.docx'))
        HelpMenu.addAction(Right_click_functions)


    def Open(self, full_paths):
        # if there are no paths from drag drop
        if not full_paths:
            # open the file menu
            full_paths = QFileDialog.getOpenFileNames(self, 'Open File')[0]

        for i, path in enumerate(full_paths):
            # delete non xlsx (excel) files
            if path[-5:].lower() != ".xlsx":
                del full_paths[i]
                continue

            if Files.values(path)[2]:  # True if errors present
                # delete non valid files
                if not self.open_all:
                    del full_paths[i]
                else:
                    # or rename to indicate error
                    message = "_ContainsErrors.xlsx"
                    if path[-len(message):] != message:
                        try:
                            os.rename(path, path[:-5] + message)
                            full_paths[i] = path[:-5] + message
                        except:
                            pass

        # copy paths to AllExcelFilesBackup
        # update paths for graph and start
        for full_path in full_paths:
            # try avoids already there type file errors
            try:
                shutil.copy(full_path, "Root\AllExcelFilesBackup")
            except:
                pass
            name = os.path.basename(full_path)
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
            if self.text_size > change:
                self.text_size += -change

        self.Widgets.setStyleSheet("font: "+str(self.text_size)+"pt")
        matplotlib.rcParams.update({'font.size': self.text_size + 2.5})
        self.Widgets.start_graph()

    def light_dark(self):
        if self.main_color >= len(self.main_colors)-1:
            self.main_color = 0
        else:
            self.main_color += 1

        color = self.main_colors[self.main_color]
        self.setStyleSheet("QWidget { background-color: "+color+" }")
        self.Widgets.ax.set_facecolor(color)
        self.Widgets.fig.set_facecolor(color)
        self.Widgets.start_graph()


class QCustomSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # super is used to refer to the QSlider parent
        self.max_float = 0.05
        super().setMinimum(0)
        super().setMaximum(665)

    # used for directly setting float values
    def value(self):
        return super().value() / super().maximum() * self.max_float

    def setValue(self, value):
        super().setValue(int(value / self.max_float * super().maximum()))

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
        self.label_conversion = 1330  # units per unit of soil
        self.label_unit = " T/Ha"  # 1330 Tonnes per Ha of soil

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

    def create_slider(self, path):

        # avoid duplicates
        if path in self.all_slider_paths:
            return

        self.all_slider_paths.append(path)
        self.slider_paths = self.all_slider_paths
        # slider_paths is subset of all_slider_paths
        # and is used to get ideal values for example, on a single slider

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
        name = os.path.basename(path).replace(".xlsx", "")
        name = name.replace(" ", "\n").replace("_", "\n")
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
        self.bars[index].remove()  # on graph
        del self.bars[index]  # in memory
        del self.slider_colors[index]
        del self.all_slider_paths[index]

    def graph_init(self):
        self.graph = QVBoxLayout()
        self.Layout.addLayout(self.graph)

        self.fig = Figure(tight_layout=True)
        canvas = FigureCanvas(self.fig)
        self.graph.addWidget(canvas)

        toolbar = NavigationToolbar2QT(canvas, self)
        self.graph.addWidget(toolbar)

        self.ax = canvas.figure.subplots()
        self.soil_path = r"Root\DefaultFiles\Soil_Zeros.xlsx"
        self.ideal_path = r"Root\DefaultFiles\Ideal_Zeros.xlsx"
        self.FuncAnimation = False

    # In the graph nutrients only account for percent of the mass
    # rock, organic matter and water are the rest

    def start_graph(self):
        # updating things other than bar scale only when they are changed helps performance

        self.length = len(Files.values(self.soil_path)[0])
        # numpy arrays help performance
        xs = np.arange(self.length)  # 1,2,3
        ys = np.zeros(self.length)  # 0,0,0

        # Function animation is an optimized loop function that calls update_graph
        self.bars = []
        if self.FuncAnimation:
            self.FuncAnimation._stop()
            self.ax.clear()

        # create bars

        for color in self.slider_colors:
            self.bars.append(self.ax.bar(xs, ys, color=color, edgecolor='black'))

        # using real values sets a propper frame

        self.bars.append(self.ax.bar(xs, Files.values(self.soil_path)[0], color="grey", edgecolor='black'))
        self.bars[-1].set_label(os.path.basename(self.soil_path)[:-5])

        self.bars.append(self.ax.bar(xs, Files.values(self.ideal_path)[0], facecolor="None", edgecolor='green'))
        self.bars[-1].set_label(os.path.basename(self.ideal_path)[:-5])
        self.bars.append(self.ax.bar(xs, Files.values(self.ideal_path)[0]*self.max_div_ideal, facecolor="None", edgecolor='red'))
        self.bars[-1].set_label(os.path.basename(self.ideal_path)[:-5]+"X"+str(self.max_div_ideal))

        self.ax.set_ylabel("Percent by mass of soil")
        self.ax.set_xlabel("Nutrients")

        xticklabels = Files.values(self.soil_path)[1]

        self.ax.set_xticks(xs)
        self.ax.set_xticklabels(xticklabels, rotation=30, horizontalalignment="right")

        self.ax.legend()

        # blit avoids a complete re-render and helps performance
        self.FuncAnimation = animation.FuncAnimation(self.fig, self.update_graph, interval=0, blit=True)

    def update_values(self, bars, values, y_values=[]):
        for bar, value in zip(bars, values):
            bar.set_height(value)
        # set y raises the bar on top of the last
        if y_values != []:
            for bar, y_value in zip(bars, y_values):
                bar.set_y(y_value)

    def update_graph(self, frames):
        y_values = Files.values(self.soil_path)[0]

        for i, slider_path in enumerate(self.all_slider_paths):
            slider_value = self.sliders.itemAt(i).widget().value()
            ys = Files.values(slider_path)[0] * slider_value
            self.update_values(self.bars[i], ys, y_values)
            y_values += ys
            setText = str(round(self.label_conversion*slider_value, 1)) + self.label_unit
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
        # reset slider_paths, which the context menu functions work over
        self.slider_paths = self.all_slider_paths
        # check if right click is above button
        for index in range(self.buttons.count()):
            widget = self.buttons.itemAt(index).widget().geometry()
            if event.globalX() < widget.x() + widget.width():
                # if so, set slider_paths to path
                # this avoids duplicate single path functions
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
        if self.sliders.count() == 0:
            return

        change_vector, sub_vectors = self.get_vectors(1)
        index, setValue = Adviser.run(change_vector, sub_vectors)
        # if the advisor doesn't have a change to improve
        if not setValue:
            # exit function
            return

        # if this is a contextMenuEvent path
        # eg [[path]]
        if len(self.slider_paths) == 1:
            # make sure its index isn't always 0
            index = self.all_slider_paths.index(self.slider_paths[0])

        # add the value the slider is already on and setValue
        setValue += self.sliders.itemAt(index).widget().value()
        self.sliders.itemAt(index).widget().setValue(setValue)

    def max_values(self):
        if self.sliders.count() == 0:
            return

        change_vector, sub_vectors = self.get_vectors(self.max_div_ideal)
        index, setValue = 0, 0.0

        # find the which compost can be put on the most witout going over limits:
        # for each of the vectors
        for i, sub_vector in enumerate(sub_vectors):
            # find the value that first goes over the limit and when
            if np.linalg.norm(sub_vector) != 0.0:
                # divide by zero errors are ignored as min value is taken
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
        self.setGeometry(200, 200, 300, 200)
        self.setText("Drag and drop saved files here")
        self.setDragEnabled(True)
        self.show()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    # doesn't support drops with no path
    # files have to be saved first
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        full_paths = []
        for x, url in enumerate(urls):
            full_paths.append(str(url.path())[1:])
        MainWindow.Open(full_paths)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
