import os
import sys
from datetime import datetime

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, \
    QCheckBox, QSpinBox, QLineEdit, QComboBox
from utils.CpuStressTester import CpuStressTester
from utils.GpuStressTester import GpuStressTester


class StressWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cpu_tester = CpuStressTester()
        self.gpu_tester = GpuStressTester()
        self.init_ui()

        self.cpu_timer = QTimer(self)
        self.gpu_timer = QTimer(self)
        self.cpu_timer.timeout.connect(self.cpu_stress_timer)
        self.gpu_timer.timeout.connect(self.gpu_stress_timer)
        # self.timer.timeout.connect(self.start)

    def init_ui(self):
        self.setWindowTitle("压力测试")
        self.setGeometry(100, 100, 800, 600)

        # CPU压力测试
        cpu_param_layout = QHBoxLayout()
        cpu_param_layout.addWidget(QLabel("CPU 压力测试"))
        cpu_param_layout.addWidget(QLabel("测试核心数: "))
        self.cpu_core_input = QSpinBox()
        self.cpu_core_input.setValue(self.cpu_tester.core_num)
        cpu_param_layout.addWidget(self.cpu_core_input)
        cpu_param_layout.addSpacing(100)
        cpu_param_layout.addWidget(QLabel("测试持续时间： "))
        self.cpu_duration_input = QSpinBox()
        cpu_param_layout.addWidget(self.cpu_duration_input)
        cpu_param_layout.addSpacing(100)

        cpu_button_layout = QHBoxLayout()
        self.cpu_start_button = QPushButton("开始")
        self.cpu_start_button.clicked.connect(self.start_cpu_stress)
        cpu_button_layout.addWidget(self.cpu_start_button)
        self.cpu_stop_button = QPushButton("停止")
        self.cpu_stop_button.setEnabled(False)
        self.cpu_stop_button.clicked.connect(self.stop_cpu_stress)
        cpu_button_layout.addWidget(self.cpu_stop_button)

        cpu_layout = QVBoxLayout()
        cpu_layout.addLayout(cpu_param_layout)
        cpu_layout.addLayout(cpu_button_layout)
        cpu_layout.addSpacing(20)

        # GPU 压力测试部分
        gpu_param_layout = QHBoxLayout()
        gpu_param_layout.addWidget(QLabel("GPU 压力测试"))
        gpu_param_layout.addWidget(QLabel("测试显卡编号:"))
        self.gpu_core_input = QSpinBox()
        gpu_param_layout.addWidget(self.gpu_core_input)
        gpu_param_layout.addSpacing(100)
        gpu_param_layout.addWidget(QLabel("测试持续时间: "))
        self.gpu_duration_input = QSpinBox()
        gpu_param_layout.addWidget(self.gpu_duration_input)
        gpu_param_layout.addSpacing(100)

        gpu_button_layout = QHBoxLayout()
        self.gpu_start_button = QPushButton("开始")
        self.gpu_start_button.clicked.connect(self.start_gpu_stress)
        gpu_button_layout.addWidget(self.gpu_start_button)
        self.gpu_stop_button = QPushButton("停止")
        self.gpu_stop_button.setEnabled(False)
        self.gpu_stop_button.clicked.connect(self.stop_gpu_stress)
        gpu_button_layout.addWidget(self.gpu_stop_button)

        gpu_layout = QVBoxLayout()
        gpu_layout.addLayout(gpu_param_layout)
        gpu_layout.addLayout(gpu_button_layout)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(cpu_layout)
        main_layout.addLayout(gpu_layout)
        main_layout.addSpacing(500)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def start_cpu_stress(self):

        # init variables
        if self.cpu_core_input.value() == 0:
            self.cpu_core_input.setValue(self.cpu_tester.core_num)
        if self.cpu_duration_input.value() == 0:
            self.cpu_duration_input.setValue(60)


        self.cpu_remaining_seconds = self.cpu_duration_input.value()
        self.cpu_core_input.setEnabled(False)
        self.cpu_duration_input.setEnabled(False)
        self.cpu_start_button.setEnabled(False)
        self.cpu_stop_button.setEnabled(True)
        self.cpu_tester.start_test(self.cpu_core_input.value(), self.cpu_remaining_seconds)

        self.cpu_timer.start(1000)  # 每秒更新一次数据

    def stop_cpu_stress(self):
        self.cpu_tester.stop_test()
        self.cpu_timer.stop()
        self.cpu_core_input.setEnabled(True)
        self.cpu_duration_input.setEnabled(True)
        self.cpu_start_button.setEnabled(True)
        self.cpu_stop_button.setEnabled(False)

    def cpu_stress_timer(self):
        self.cpu_remaining_seconds -= 1
        self.cpu_duration_input.setValue(self.cpu_remaining_seconds)
        if self.cpu_remaining_seconds == 0:
            self.stop_cpu_stress()
        pass


    def start_gpu_stress(self):
        # init variables
        if self.gpu_duration_input.value() == 0:
            self.gpu_duration_input.setValue(60)

        self.gpu_remaining_seconds = self.gpu_duration_input.value()
        self.gpu_core_input.setEnabled(False)
        self.gpu_duration_input.setEnabled(False)
        self.gpu_start_button.setEnabled(False)
        self.gpu_stop_button.setEnabled(True)
        self.gpu_tester.start_test(self.gpu_remaining_seconds)

        self.gpu_timer.start(1000)  # 每秒更新一次数据

    def stop_gpu_stress(self):
        self.gpu_tester.stop_test()
        self.gpu_timer.stop()
        self.gpu_core_input.setEnabled(True)
        self.gpu_duration_input.setEnabled(True)
        self.gpu_start_button.setEnabled(True)
        self.gpu_stop_button.setEnabled(False)

    def gpu_stress_timer(self):
        self.gpu_remaining_seconds -= 1
        self.gpu_duration_input.setValue(self.gpu_remaining_seconds)
        if self.gpu_remaining_seconds == 0:
            self.stop_cpu_stress()
        pass
