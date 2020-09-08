
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QDial,
                             QVBoxLayout, QApplication, QHBoxLayout,
                             QPushButton, QLabel, QGroupBox,
                             QDoubleSpinBox, )
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np
import FOC
import time


screen_width = 360
screen_height = 4
screen_dpi = 100
sample_num = 360


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=screen_width, height=screen_height, dpi=screen_dpi):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        # self.axes.hold(False)

        self.axes.set_xlim(0, screen_width)
        self.axes.set_ylim(-screen_height//2, screen_height//2)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def compute_initial_figure(self):
        pass


class Example(QWidget):

    def __init__(self, foc):
        super().__init__()
        self.foc = foc
        self.initUI()
        self.appendTheta = 0
        self.appendSpeed = 1

        self.is_position = True

    def initUI(self):

        self.label_iq = QLabel('Iq:', self)
        self.label_iq.setAlignment(Qt.AlignRight)

        self.spinBox_iq = QDoubleSpinBox(self)
        self.spinBox_iq.setValue(self.foc.get_iq())
        self.spinBox_iq.setSingleStep(0.1)
        self.spinBox_iq.setMinimum(-2)
        self.spinBox_iq.setMaximum(2)

        self.sldChangeV = QSlider(Qt.Horizontal, self)
        self.sldChangeV.setValue(self.foc.get_speed())

        self.dial = QDial(self)  #实例化旋转按钮
        self.dial.setFixedSize(100, 100)  # 固定旋钮大小，否则会随窗口的变化而发生变化
        self.dial.setRange(0, 360)  #设置表盘数值范围，当然也可以使用setMinimum()和setMaximum()方法
        self.dial.setNotchesVisible(True)  # 是否显示刻度，刻度会根据我们设置的数值自动调整
        self.dial.valueChanged.connect(self.on_change_func)  # 当数值发生变化时发出信号

        self.label = QLabel('0', self)


        self.mode_button = QPushButton('Speed', self)
        self.mode_button.setCheckable(True)
        self.mode_button.clicked[bool].connect(self.setMode)


        self.canvas = MyMplCanvas(self, width=screen_width, height=screen_height, dpi=screen_dpi)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)

        hbox = QHBoxLayout()

        self.groupboxPID = QGroupBox('FOC', self)

        self.groupboxPID.setLayout(hbox)

        hbox.addWidget(self.label_iq)
        hbox.addWidget(self.spinBox_iq)

        vbox.addWidget(self.mode_button)

        vbox.addWidget(self.groupboxPID)

        vbox.addWidget(self.sldChangeV)

        vbox.addWidget(self.dial)
        vbox.addWidget(self.label)


        self.setLayout(vbox)

        self.spinBox_iq.valueChanged.connect(self.change_iq)

        self.sldChangeV.valueChanged.connect(self.update_speed)

        self.x = np.linspace(0, screen_width, sample_num)

        self.foc.set_theta(self.x)
        a_b_c = self.foc.dq2abc()

        self.a_array = a_b_c[0]
        self.b_array = a_b_c[1]
        self.c_array = a_b_c[2]

        self.line_a, = self.canvas.axes.plot(self.x, self.a_array, color='r', label='a', animated=True, lw=1)
        self.line_b, = self.canvas.axes.plot(self.x, self.b_array, color='b', label='b', animated=True, lw=1)
        self.line_c, = self.canvas.axes.plot(self.x, self.c_array, color='g', label='c', animated=True, lw=1)

        self.appendV = 0

        self.canvas.axes.legend(loc="upper left", shadow=True)

        # self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('F O C 调节器')

        self.show()

    def setMode(self, pressed):
        source = self.sender()
        if source.text() == "Position" or source.text() == "Speed":
            if pressed:
                self.mode_button.setText('Position')
                self.is_position=False
                print('speed')
            else:
                self.mode_button.setText('Speed')
                self.is_position=True
                print('position')

    def on_change_func(self):
        self.appendTheta = self.dial.value()
        self.label.setText(str(self.appendTheta))

    def change_iq(self):
        iq_value = self.spinBox_iq.value()
        self.foc.set_iq(iq_value)

    def update_speed(self, i):
        self.appendSpeed = int(i * 10 / 100)
        self.foc.set_speed(self.appendSpeed)

    def update_line(self, i):
        if self.is_position:
            self.foc.set_theta(self.appendTheta)
        else:
            index = i % 360
            self.foc.set_theta(index)

        a_b_c = self.foc.dq2abc()
        a = a_b_c[0]
        b = a_b_c[1]
        c = a_b_c[2]

        a_list = self.a_array.tolist()
        b_list = self.b_array.tolist()
        c_list = self.c_array.tolist()

        a_list.pop(0)
        b_list.pop(0)
        c_list.pop(0)

        a_list.append(a)
        b_list.append(b)
        c_list.append(c)

        self.a_array = np.array(a_list)
        self.b_array = np.array(b_list)
        self.c_array = np.array(c_list)

        self.line_a.set_ydata(self.a_array)
        self.line_b.set_ydata(self.b_array)
        self.line_c.set_ydata(self.c_array)

        return [self.line_a, self.line_b, self.line_c]

if __name__ == '__main__':
    foc = FOC.FOC(theta=0)
    app = QApplication(sys.argv)
    ex = Example(foc)
    ani = FuncAnimation(ex.canvas.figure, ex.update_line,
                        blit=True, interval=25)
    sys.exit(app.exec_())

