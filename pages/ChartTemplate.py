import sys

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MonitorChart(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.chart = PerformanceChart()
        self.layout.addWidget(self.chart)

    def add_data(self, value):
        self.chart.add_data(value)

    def draw_line(self, data):
        self.chart.draw_line(data)


class PerformanceChart(FigureCanvas):
    def __init__(self):
        super().__init__()
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.data = []

        FigureCanvas.__init__(self, self.fig)
        self.setParent(None)

        self.setMinimumSize(100, 300)
        self.ax.set_xlim(0, 60)  # 显示最近60秒的数据
        self.ax.set_ylim(0, 100)  # CPU 或内存使用率范围
        # self.ax.set_xlabel("时间（秒）")
        self.ax.set_ylabel("Temperature/C")

        # self.line, = self.ax.plot([], [], label="性能")
        self.line, = self.ax.plot([], [])

    def add_data(self, value):
        self.data.append(value)
        if len(self.data) > 60:
            self.data.pop(0)

        self.line.set_data(np.arange(len(self.data)), self.data)
        self.ax.relim()
        self.ax.autoscale_view()

        self.draw()

    def draw_line(self, data):
        self.data = data
        if len(data) > 60:
            self.data = data[-60:]
        self.line.set_data(np.arange(len(self.data)), self.data)
        self.ax.relim()
        self.ax.autoscale_view()

        self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
