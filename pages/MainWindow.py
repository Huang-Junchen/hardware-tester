import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
from pages.MonitorWindow import PerformanceMonitorApp
from pages.StressWindow import StressWindow


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
        monitorWindow = PerformanceMonitorApp()
        stressWindow = StressWindow()

        tab_widget.addTab(stressWindow, "压力测试")
        tab_widget.addTab(monitorWindow, "性能监控")

        # 将选项卡部件添加到主布局中
        layout.addWidget(tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())