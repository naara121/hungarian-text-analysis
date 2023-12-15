from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from numpy import arange

from controller.magyarlanc_controller import MagyarlancController
from view.grammatical_number_comparison_window import GrammaticalNumberComparisonWindow
from view.object_dependency_relation_window import ObjectDependencyRelationWindow
from view.root_dependency_relation_window import RootDependencyRelationWindow
from view.subject_dependency_relation_window import SubjectDependencyRelationWindow
from view.tense_comparison_window import TenseComparisonWindow


class FifthCompareWorksWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(FifthCompareWorksWindow, self).__init__()
        loadUi(Path("view/ui/lexical_properties_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._magyarlanc_controller = MagyarlancController()

        self.set_labels()

        self.prev_screen_button.clicked.connect(self.previous_screen)
        self.tense_button.clicked.connect(self.tense_screen)
        self.grammatical_number_button.clicked.connect(self.grammatical_number_screen)
        self.root_button.clicked.connect(self.root_screen)
        self.subject_button.clicked.connect(self.subject_screen)
        self.object_button.clicked.connect(self.object_screen)

        self._past_figure = Figure(figsize=(5, 5))
        self._past_canvas = FigureCanvasQTAgg(self._past_figure)
        self.past_words_vbox.addWidget(self._past_canvas)
        self.past_words_vbox.addWidget(self.past_words_label)

        self.create_grammatical_tense_comparison_bar_plot(self._past_figure, self._past_canvas)

        self._numbers_figure = Figure(figsize=(5, 5))
        self._numbers_canvas = FigureCanvasQTAgg(self._numbers_figure)
        self.pos_number_vbox.addWidget(self._numbers_canvas)
        self.pos_number_vbox.addWidget(self.pos_number_label)

        self.create_pos_number_comparison_bar_plot(self._numbers_figure, self._numbers_canvas)

    def set_labels(self):
        self.past_words_label.setFont(QFont("Arial", 12, italic=True))
        self.past_words_label.setAlignment(Qt.AlignCenter)
        self.past_words_label.setWordWrap(True)

        self.pos_number_label.setFont(QFont("Arial", 12, italic=True))
        self.pos_number_label.setAlignment(Qt.AlignCenter)
        self.pos_number_label.setWordWrap(True)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def tense_screen(self):
        self._widgets.addWidget(TenseComparisonWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def grammatical_number_screen(self):
        self._widgets.addWidget(GrammaticalNumberComparisonWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def root_screen(self):
        self._widgets.addWidget(RootDependencyRelationWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def subject_screen(self):
        self._widgets.addWidget(SubjectDependencyRelationWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def object_screen(self):
        self._widgets.addWidget(ObjectDependencyRelationWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def create_grammatical_tense_comparison_bar_plot(self, figure, canvas):
        book_1_tenses = self._magyarlanc_controller.get_grammatical_tenses(self._book_1.writer, self._book_1.filename)
        book_2_tenses = self._magyarlanc_controller.get_grammatical_tenses(self._book_2.writer, self._book_2.filename)

        figure.clear()

        ax = figure.add_subplot(111)
        past = ax.bar(arange(2) - 0.2, [sum(list(book_1_tenses["Past"].values())), sum(list(book_2_tenses["Past"].values()))], color="firebrick", label="Múlt", width=0.2)
        pres = ax.bar(arange(2) + 0.2, [sum(list(book_1_tenses["Pres"].values())), sum(list(book_2_tenses["Pres"].values()))], color="slateblue", label="Jelen", width=0.2)
        ax.bar_label(past, label_type="center")
        ax.bar_label(pres, label_type="center")
        ax.legend()
        ax.set_xticks(arange(2), labels=[self._book_1.title, self._book_2.title])

        canvas.draw()

    def create_pos_number_comparison_bar_plot(self, figure, canvas):
        numbers_1 = self._magyarlanc_controller.get_pos_number(self._book_1.writer, self._book_1.filename)
        numbers_2 = self._magyarlanc_controller.get_pos_number(self._book_2.writer, self._book_2.filename)

        figure.clear()

        ax = figure.add_subplot(111)
        past = ax.bar(arange(2) - 0.2, [sum(list(numbers_1["Sing"].values())), sum(list(numbers_2["Sing"].values()))], color="firebrick", label="Egyes szám", width=0.2)
        pres = ax.bar(arange(2) + 0.2, [sum(list(numbers_1["Plur"].values())), sum(list(numbers_2["Plur"].values()))], color="slateblue", label="Többes szám", width=0.2)
        ax.bar_label(past, label_type="center")
        ax.bar_label(pres, label_type="center")
        ax.legend()
        ax.set_xticks(arange(2), labels=[self._book_1.title, self._book_2.title])

        canvas.draw()
