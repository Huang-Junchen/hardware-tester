import sys

from PyQt5.QtWidgets import QApplication

from pages.MonitorWindow import PerformanceMonitorApp



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PerformanceMonitorApp()
    window.show()
    sys.exit(app.exec_())