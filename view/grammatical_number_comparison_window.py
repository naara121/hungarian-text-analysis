from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from controller.magyarlanc_controller import MagyarlancController


class GrammaticalNumberComparisonWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(GrammaticalNumberComparisonWindow, self).__init__()
        loadUi(Path("view/ui/grammatical_number_comparison_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._magyarlanc_controller = MagyarlancController()

        self._book_1_numbers = self._magyarlanc_controller.get_pos_number(self._book_1.writer, self._book_1.filename)
        self._book_2_numbers = self._magyarlanc_controller.get_pos_number(self._book_2.writer, self._book_2.filename)

        self.set_labels()

        self.prev_screen_button.clicked.connect(self.previous_screen)

        self._sing_figure_1 = Figure(figsize=(5, 5))
        self._sing_canvas_1 = FigureCanvasQTAgg(self._sing_figure_1)
        self.sing_vbox_1.addWidget(self._sing_canvas_1)
        self.sing_vbox_1.addWidget(self.sing_label_1)

        self._sing_figure_2 = Figure(figsize=(5, 5))
        self._sing_canvas_2 = FigureCanvasQTAgg(self._sing_figure_2)
        self.sing_vbox_2.addWidget(self._sing_canvas_2)
        self.sing_vbox_2.addWidget(self.sing_label_2)

        self.create_grammatical_number_bar_plot(self._sing_figure_1, self._sing_canvas_1, self._book_1_numbers["Sing"], "firebrick")
        self.create_grammatical_number_bar_plot(self._sing_figure_2, self._sing_canvas_2, self._book_2_numbers["Sing"], "firebrick")

        self._plur_figure_1 = Figure(figsize=(5, 5))
        self._plur_canvas_1 = FigureCanvasQTAgg(self._plur_figure_1)
        self.plur_vbox_1.addWidget(self._plur_canvas_1)
        self.plur_vbox_1.addWidget(self.plur_label_1)

        self._plur_figure_2 = Figure(figsize=(5, 5))
        self._plur_canvas_2 = FigureCanvasQTAgg(self._plur_figure_2)
        self.plur_vbox_2.addWidget(self._plur_canvas_2)
        self.plur_vbox_2.addWidget(self.plur_label_2)

        self.create_grammatical_number_bar_plot(self._plur_figure_1, self._plur_canvas_1, self._book_1_numbers["Plur"], "slateblue")
        self.create_grammatical_number_bar_plot(self._plur_figure_2, self._plur_canvas_2, self._book_2_numbers["Plur"], "slateblue")

    def set_labels(self):
        title_font = QFont("Arial", 14)
        title_font.setBold(True)

        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)

        self.sing_label_1.setText(f"{self._book_1.title} című műben, az egyes számú szavakból legtöbbszőr előforduló 10 szótő.")
        self.sing_label_1.setFont(QFont("Arial", 10, italic=True))
        self.sing_label_1.setAlignment(Qt.AlignCenter)
        self.sing_label_1.setWordWrap(True)

        self.sing_label_2.setText(f"{self._book_2.title} című műben, az egyes számú szavakból legtöbbszőr előforduló 10 szótő.")
        self.sing_label_2.setFont(QFont("Arial", 10, italic=True))
        self.sing_label_2.setAlignment(Qt.AlignCenter)
        self.sing_label_2.setWordWrap(True)

        self.plur_label_1.setText(f"{self._book_1.title} című műben, a többes számú szavakból legtöbbszőr előforduló 10 szótő.")
        self.plur_label_1.setFont(QFont("Arial", 10, italic=True))
        self.plur_label_1.setAlignment(Qt.AlignCenter)
        self.plur_label_1.setWordWrap(True)

        self.plur_label_2.setText(f"{self._book_2.title} című műben, a többes számú szavakból legtöbbszőr előforduló 10 szótő.")
        self.plur_label_2.setFont(QFont("Arial", 10, italic=True))
        self.plur_label_2.setAlignment(Qt.AlignCenter)
        self.plur_label_2.setWordWrap(True)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def create_grammatical_number_bar_plot(self, figure, canvas, number_dict, color):
        figure.clear()

        ax = figure.add_subplot(111)
        ax.barh(list(number_dict.keys())[:10], list(number_dict.values())[:10], height=0.5, color=color)
        ax.invert_yaxis()

        canvas.draw()
