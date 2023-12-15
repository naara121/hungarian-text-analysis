from multiprocessing import Process
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from controller.book_controller import BookController
from controller.magyarlanc_controller import MagyarlancController
from view.word_similarity_comparison_window import WordSimilarityComparisonWindow


class TopWordsWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(TopWordsWindow, self).__init__()
        loadUi(Path("view/ui/all_top_words_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._book_controller = BookController()
        self._magyarlanc_controller = MagyarlancController()

        self.set_labels()

        self.prev_screen_button.clicked.connect(self.previous_screen)
        self.next_screen_button.clicked.connect(self.next_screen)

        self._top_words_figure_1 = Figure(figsize=(5, 5))
        self._top_words_canvas_1 = FigureCanvasQTAgg(self._top_words_figure_1)
        self.top_word_vbox_1.addWidget(self._top_words_canvas_1)
        self.top_word_vbox_1.addWidget(self.top_word_label_1)

        self._top_words_figure_2 = Figure(figsize=(5, 5))
        self._top_words_canvas_2 = FigureCanvasQTAgg(self._top_words_figure_2)
        self.top_word_vbox_2.addWidget(self._top_words_canvas_2)
        self.top_word_vbox_2.addWidget(self.top_word_label_2)

        top_word_process_1 = Process(
            target=self.create_top_10_words_bar_plot(
                self._top_words_figure_1, self._top_words_canvas_1,
                self._book_controller.get_most_frequent_words_from_book(
                    self._book_1.writer, self._book_1.filename, 20
                ),
                "firebrick"
            )
        )

        top_word_process_2 = Process(
            target=self.create_top_10_words_bar_plot(
                self._top_words_figure_2, self._top_words_canvas_2,
                self._book_controller.get_most_frequent_words_from_book(
                    self._book_2.writer, self._book_2.filename, 20
                ),
                "firebrick"
            )
        )

        top_word_process_1.start()
        top_word_process_2.start()

        top_word_process_1.join()
        top_word_process_2.join()

    def set_labels(self):
        self.top_word_label_1.setText(f"{self._book_1.title} című műben legtöbbszőr előforduló 20 szótő.")
        self.top_word_label_1.setFont(QFont("Arial", 10, italic=True))
        self.top_word_label_1.setAlignment(Qt.AlignCenter)
        self.top_word_label_1.setWordWrap(True)

        self.top_word_label_2.setText(f"{self._book_2.title} című műben legtöbbszőr előforduló 20 szótő.")
        self.top_word_label_2.setFont(QFont("Arial", 10, italic=True))
        self.top_word_label_2.setAlignment(Qt.AlignCenter)
        self.top_word_label_2.setWordWrap(True)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def next_screen(self):
        self._widgets.addWidget(WordSimilarityComparisonWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def create_top_10_words_bar_plot(self, figure, canvas, word_dict, color):
        figure.clear()

        ax = figure.add_subplot(111)
        ax.bar(word_dict.keys(), word_dict.values(), width=0.5, color=color)
        figure.tight_layout()

        canvas.draw()
