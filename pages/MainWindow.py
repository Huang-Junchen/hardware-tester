import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
from MonitorWindow import PerformanceMonitorApp

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个主窗口部件
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout(main_widget)

        # 创建选项卡部件
        tab_widget = QTabWidget()

        # 创建参数设置选项卡的内容
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        label1 = QLabel("这是参数设置选项卡的内容")
        tab1_layout.addWidget(label1)
        tab_widget.addTab(tab1, "参数设置")

        monitorWindow = PerformanceMonitorApp()
        tab_widget.addTab(monitorWindow, "性能监控")

        # 将选项卡部件添加到主布局中
        layout.addWidget(tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())