from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from controller.magyarlanc_controller import MagyarlancController


class TenseComparisonWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(TenseComparisonWindow, self).__init__()
        loadUi(Path("view/ui/tense_comparison_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._magyarlanc_controller = MagyarlancController()

        self.prev_screen_button.clicked.connect(self.previous_screen)

        self.set_labels()

        self._book_1_tenses = self._magyarlanc_controller.get_grammatical_tenses(self._book_1.writer, self._book_1.filename)
        self._book_2_tenses = self._magyarlanc_controller.get_grammatical_tenses(self._book_2.writer, self._book_2.filename)

        self._past_figure_1 = Figure(figsize=(5, 5))
        self._past_canvas_1 = FigureCanvasQTAgg(self._past_figure_1)
        self.past_tense_vbox_1.addWidget(self._past_canvas_1)
        self.past_tense_vbox_1.addWidget(self.past_label_1)

        self._past_figure_2 = Figure(figsize=(5, 5))
        self._past_canvas_2 = FigureCanvasQTAgg(self._past_figure_2)
        self.past_tense_vbox_2.addWidget(self._past_canvas_2)
        self.past_tense_vbox_2.addWidget(self.past_label_2)

        self.create_grammatical_tense_bar_plot(self._past_figure_1, self._past_canvas_1, self._book_1_tenses["Past"], "firebrick")
        self.create_grammatical_tense_bar_plot(self._past_figure_2, self._past_canvas_2, self._book_2_tenses["Past"], "firebrick")

        self._pres_figure_1 = Figure(figsize=(5, 5))
        self._pres_canvas_1 = FigureCanvasQTAgg(self._pres_figure_1)
        self.pres_tense_vbox_1.addWidget(self._pres_canvas_1)
        self.pres_tense_vbox_1.addWidget(self.pres_label_1)

        self._pres_figure_2 = Figure(figsize=(5, 5))
        self._pres_canvas_2 = FigureCanvasQTAgg(self._pres_figure_2)
        self.pres_tense_vbox_2.addWidget(self._pres_canvas_2)
        self.pres_tense_vbox_2.addWidget(self.pres_label_2)

        self.create_grammatical_tense_bar_plot(self._pres_figure_1, self._pres_canvas_1, self._book_1_tenses["Pres"], "slateblue")
        self.create_grammatical_tense_bar_plot(self._pres_figure_2, self._pres_canvas_2, self._book_2_tenses["Pres"], "slateblue")

    def set_labels(self):
        title_font = QFont("Arial", 14)
        title_font.setBold(True)

        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)

        self.past_label_1.setText(f"{self._book_1.title} című műben, a múlt idejű szavakból legtöbbszőr előforduló 10 szótő.")
        self.past_label_1.setFont(QFont("Arial", 10, italic=True))
        self.past_label_1.setAlignment(Qt.AlignCenter)
        self.past_label_1.setWordWrap(True)

        self.past_label_2.setText(f"{self._book_2.title} című műben, a múlt idejű szavakból legtöbbszőr előforduló 10 szótő.")
        self.past_label_2.setFont(QFont("Arial", 10, italic=True))
        self.past_label_2.setAlignment(Qt.AlignCenter)
        self.past_label_2.setWordWrap(True)

        self.pres_label_1.setText(f"{self._book_1.title} című műben, a jelen idejű szavakból legtöbbszőr előforduló 10 szótő.")
        self.pres_label_1.setFont(QFont("Arial", 10, italic=True))
        self.pres_label_1.setAlignment(Qt.AlignCenter)
        self.pres_label_1.setWordWrap(True)

        self.pres_label_2.setText(f"{self._book_2.title} című műben, a jelen idejű szavakból legtöbbszőr előforduló 10 szótő.")
        self.pres_label_2.setFont(QFont("Arial", 10, italic=True))
        self.pres_label_2.setAlignment(Qt.AlignCenter)
        self.pres_label_2.setWordWrap(True)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def create_grammatical_tense_bar_plot(self, figure, canvas, tense_dict, color):
        figure.clear()

        ax = figure.add_subplot(111)
        ax.barh(list(tense_dict.keys())[:10], list(tense_dict.values())[:10], height=0.5, color=color)
        ax.invert_yaxis()

        canvas.draw()
