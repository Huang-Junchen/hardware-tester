import os
import sys
from datetime import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, \
    QCheckBox, QSpinBox, QLineEdit, QComboBox, QScrollArea

from pages.ChartTemplate import MonitorChart
from utils.CpuMonitor import CpuMonitor
from utils.GpuMonitor import GpuMonitor
from utils.Recoder import Recoder


class PerformanceMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.remaining_seconds = None
        self.current_cpu_chart = None
        self.current_gpu_chart = None

        self.cpu_monitor = CpuMonitor()
        self.cpu_num = self.cpu_monitor.num
        try:
            self.gpu_monitor = GpuMonitor()
        except:
            print("No GPU det")
        self.gpu_num = self.gpu_monitor.num
        self.data = []

        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_performance_data)

    def init_ui(self):
        self.setWindowTitle("性能监控")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()  # 使用 QHBoxLayout 布局
        self.central_widget.setLayout(self.layout)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 50, 20, 20)
        self.left_layout.setSpacing(20)
        self.layout.addLayout(self.left_layout, 3)
        self.layout.addLayout(self.right_layout, 7)

        self.init_left_layout()
        self.init_right_layout()

    def init_left_layout(self):
        # 左侧布局
        # 勾选框
        self.cpu_checkbox = QCheckBox("CPU", self)
        self.cpu_checkbox.setChecked(True)
        self.gpu_checkbox = QCheckBox("GPU", self)
        self.left_layout.addWidget(self.cpu_checkbox)
        self.left_layout.addWidget(self.gpu_checkbox)

        # 计时器
        self.countdown = QSpinBox(self)
        self.countdown.setRange(0, 999)
        self.countdown.setMinimum(1)
        self.countdown.setValue(60)
        self.countdown_layout = QHBoxLayout()
        self.left_layout.addLayout(self.countdown_layout)
        self.countdown_layout.addWidget(QLabel("监控持续时间:"))
        self.countdown_layout.addWidget(self.countdown)
        self.countdown_layout.addWidget(QLabel("秒", self))

        # 保存文件名
        self.logname_layout = QHBoxLayout()
        self.filenameLineEdit = QLineEdit(self)
        self.left_layout.addLayout(self.logname_layout)
        self.logname_layout.addWidget(QLabel("日志文件名："))
        self.logname_layout.addWidget(self.filenameLineEdit)

        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start)
        self.left_layout.addWidget(self.start_button)

        self.record_button = QPushButton("保存")
        self.record_button.clicked.connect(self.record)
        self.left_layout.addWidget(self.record_button)
        self.record_button.setEnabled(False)

        self.left_layout.addStretch()

    def init_right_layout(self):
        # 右侧布局
        self.cpu_label_layout = QHBoxLayout()
        self.gpu_label_layout = QHBoxLayout()
        self.cpu_label = QLabel("CPU")
        self.gpu_label = QLabel("GPU")

        self.cpu_list = QComboBox()
        self.cpu_list.currentIndexChanged.connect(self.on_cpu_list_changed)
        if self.cpu_num == 0:
            self.cpu_list.addItem("None")
        else:
            self.cpu_list.addItems([f"{i}" for i in range(0, self.cpu_num)])
            self.current_cpu_chart = 0

        # self.gpu_tester = GpuTester()
        self.gpu_list = QComboBox()
        if self.gpu_num == 0:
            self.gpu_list.addItem("None")
        else:
            self.gpu_list.addItems([f"{i}" for i in range(0, self.gpu_num)])
            self.current_gpu_chart = 0

        self.gpu_list.currentIndexChanged.connect(self.on_gpu_list_changed)
        self.cpu_label_layout.addSpacing(20)
        self.cpu_label_layout.addWidget(self.cpu_label)
        self.cpu_label_layout.addWidget(self.cpu_list)
        self.cpu_label_layout.addStretch()
        self.gpu_label_layout.addSpacing(20)
        self.gpu_label_layout.addWidget(self.gpu_label)
        self.gpu_label_layout.addWidget(self.gpu_list)
        self.gpu_label_layout.addStretch()

        self.cpu_chart = MonitorChart()
        self.gpu_chart = MonitorChart()

        self.right_layout.addLayout(self.cpu_label_layout)
        self.right_layout.addWidget(self.cpu_chart)
        self.right_layout.addLayout(self.gpu_label_layout)
        self.right_layout.addWidget(self.gpu_chart)

    def start(self):
        self.data = []
        self.remaining_seconds = self.countdown.value()
        self.countdown.setEnabled(False)
        self.start_button.setEnabled(False)
        self.cpu_checkbox.setEnabled(False)
        self.gpu_checkbox.setEnabled(False)
        self.default_filename = datetime.now().strftime("%Y%m%d%H%M%S")

        self.timer.start(1000)  # 每秒更新一次数据

    def record(self):
        log_file = os.path.join("./logs", self.filenameLineEdit.text() + ".csv")
        log = Recoder(log_file)
        log.write_record_file(log.generate_table_header(self.cpu_num, self.gpu_num))
        for row in self.data:
            log.write_record_file(','.join(row))
        pass

    def on_cpu_list_changed(self, index):
        self.current_cpu_chart = int(self.cpu_list.currentText())

    def on_gpu_list_changed(self, index):
        self.current_gpu_chart = int(self.gpu_list.currentText())

    def update_performance_data(self):
        self.remaining_seconds -= 1
        self.countdown.setValue(self.remaining_seconds)
        if self.remaining_seconds == 0:

            self.timer.stop()
            self.countdown.setValue(60)
            self.cpu_checkbox.setEnabled(True)
            self.gpu_checkbox.setEnabled(True)
            self.countdown.setEnabled(True)
            self.start_button.setEnabled(True)
            self.record_button.setEnabled(True)
            if self.filenameLineEdit.text() == "":
                self.filenameLineEdit.setText(self.default_filename)


        timestamp = str(datetime.now()).split('.')[0]
        data_row = [timestamp]
        data_row.extend(self.cpu_monitor.get_statistics())
        if self.gpu_checkbox.isChecked():
            data_row.extend(self.gpu_monitor.get_statistics())

        self.data.append(data_row)

        print(data_row)
        if self.cpu_checkbox.isChecked():
            self.cpu_chart.draw_line([float(row[self.current_cpu_chart * self.cpu_num + 1]) for row in self.data])
        if self.gpu_checkbox.isChecked():
            self.gpu_chart.draw_line(
                [float(row[2 * self.cpu_num + self.current_gpu_chart * self.gpu_num + 3]) for row in self.data])
        # log.write_record_file(','.join(data_row))

def main():
    app = QApplication(sys.argv)
    window = PerformanceMonitorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
