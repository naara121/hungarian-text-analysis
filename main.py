from pathlib import Path
from sys import argv, exit

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtWidgets import QApplication

from view.start_window import StartWindow

if __name__ == "__main__":
    app = QApplication(argv)
    app.setApplicationName("Hungarian Text Analysis")
    app.setWindowIcon(QIcon(Path("hta.jpg").name))

    widgets = QtWidgets.QStackedWidget()

    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.white)
    widgets.setAutoFillBackground(True)
    widgets.setPalette(palette)

    widgets.addWidget(StartWindow(widgets))

    widgets.show()

    exit(app.exec_())
