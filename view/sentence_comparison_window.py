from multiprocessing import Process
from pathlib import Path
from re import sub

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from numpy import arange

from controller.book_controller import BookController
from controller.magyarlanc_controller import MagyarlancController
from view.top_words_window import TopWordsWindow


class SentenceComparisonWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(SentenceComparisonWindow, self).__init__()
        loadUi(Path("view/ui/sentence_comparison_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._book_controller = BookController()
        self._magyarlanc_controller = MagyarlancController()
        self._all_words_1 = self._magyarlanc_controller.get_magyaralanc_out(self._book_1.writer, self._book_1.filename).all_words
        self._all_words_2 = self._magyarlanc_controller.get_magyaralanc_out(self._book_2.writer, self._book_2.filename).all_words
        self._sentence_1 = self._all_words_1.split("\n")
        self._sentence_2 = self._all_words_2.split("\n")

        self.prev_screen_button.clicked.connect(self.previous_screen)
        self.next_screen_button.clicked.connect(self.next_screen)

        self.set_labels()

        # all words vbox initialization
        self._all_words_figure = Figure(figsize=(5, 5))
        self._all_words_canvas = FigureCanvasQTAgg(self._all_words_figure)
        self.all_words_vbox.addWidget(self._all_words_canvas)
        self.all_words_vbox.addWidget(self.all_words_label)

        create_all_word_process = Process(target=self.create_all_word_comparison_bar_plot(self._all_words_figure, self._all_words_canvas))

        # sentences vbox initialization
        self._sentences_figure = Figure(figsize=(5, 5))
        self._sentences_canvas = FigureCanvasQTAgg(self._sentences_figure)
        self.sentences_vbox.addWidget(self._sentences_canvas)
        self.sentences_vbox.addWidget(self.sentences_label)

        create_sentences_process = Process(target=self.create_sentence_comparison_bar_plot(self._sentences_figure, self._sentences_canvas))

        # avg sentences vbox initialization
        self._avg_sentences_figure = Figure(figsize=(5, 5))
        self._avg_sentences_canvas = FigureCanvasQTAgg(self._avg_sentences_figure)
        self.avg_sentences_vbox.addWidget(self._avg_sentences_canvas)
        self.avg_sentences_vbox.addWidget(self.avg_sentence_label)

        # max sentences vbox initialization
        self._max_sentences_figure = Figure(figsize=(5, 5))
        self._max_sentences_canvas = FigureCanvasQTAgg(self._max_sentences_figure)
        self.max_sentence_vbox.addWidget(self._max_sentences_canvas)
        self.max_sentence_vbox.addWidget(self.max_sentence_label)

        create_max_sentence_process = Process(target=self.create_max_sentence_bar_plot(self._max_sentences_figure, self._max_sentences_canvas))

        create_all_word_process.start()
        create_sentences_process.start()
        create_max_sentence_process.start()

        create_all_word_process.join()
        create_sentences_process.join()
        create_max_sentence_process.join()

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def next_screen(self):
        self._widgets.addWidget(TopWordsWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def set_labels(self):
        self.all_words_label.setFont(QFont("Arial", 12, italic=True))
        self.all_words_label.setAlignment(Qt.AlignCenter)
        self.all_words_label.setWordWrap(True)

        self.sentences_label.setFont(QFont("Arial", 12, italic=True))
        self.sentences_label.setAlignment(Qt.AlignCenter)
        self.sentences_label.setWordWrap(True)

        self.avg_sentence_label.setFont(QFont("Arial", 12, italic=True))
        self.avg_sentence_label.setAlignment(Qt.AlignCenter)
        self.avg_sentence_label.setWordWrap(True)

        self.max_sentence_label.setFont(QFont("Arial", 12, italic=True))
        self.max_sentence_label.setAlignment(Qt.AlignCenter)
        self.max_sentence_label.setWordWrap(True)

    def create_all_word_comparison_bar_plot(self, figure, canvas):
        vocab_1 = sub(r"[^\w\s]", "", self._all_words_1).lower().replace("  ", "").split(" ")
        vocab_2 = sub(r"[^\w\s]", "", self._all_words_2).lower().replace("  ", "").split(" ")

        figure.clear()

        ax = figure.add_subplot(111)
        all_words = ax.bar(arange(2) - 0.2, [len(vocab_1), len(vocab_2)], color="orangered", label="Összes szó",
                           width=0.2)
        diff_words = ax.bar(arange(2) + 0.2, [len(set(vocab_1)), len(set(vocab_2))], color="darksalmon",
                            label="Különböző szavak", width=0.2)
        ax.bar_label(all_words, label_type="center")
        ax.bar_label(diff_words, label_type="center")
        ax.legend()
        ax.set_xticks(arange(2), labels=[self._book_1.title, self._book_2.title])

        canvas.draw()

    def create_sentence_comparison_bar_plot(self, figure, canvas):
        figure.clear()

        ax = figure.add_subplot(111)
        sentences = ax.bar([self._book_1.title, self._book_2.title], [len(self._sentence_1), len(self._sentence_2)],
                           color="sandybrown", width=0.2)
        ax.bar_label(sentences, label_type="center")
        figure.tight_layout()

        canvas.draw()

    def create_max_sentence_bar_plot(self, figure, canvas):
        max_sentence_1 = max(self._sentence_1, key=len).split(" ")
        max_sentence_2 = max(self._sentence_2, key=len).split(" ")

        figure.clear()

        ax = figure.add_subplot(111)
        max_sentences = ax.bar([self._book_1.title, self._book_2.title], [len(max_sentence_1), len(max_sentence_2)],
                               color="sienna", width=0.2)
        ax.bar_label(max_sentences, label_type="center")
        figure.tight_layout()

        canvas.draw()

        self.create_avg_sentence_length_bar_plot(self._avg_sentences_figure, self._avg_sentences_canvas, max_sentence_1,
                                                 max_sentence_2)

    def create_avg_sentence_length_bar_plot(self, figure, canvas, max_sentence_1, max_sentence_2):
        figure.clear()

        max_sentences = [float(round(sum(map(len, max_sentence_1)) / float(len(max_sentence_1)), 2)),
                         float(round(sum(map(len, max_sentence_2)) / float(len(max_sentence_2)), 2))
                         ]

        ax = figure.add_subplot(111)
        max_sentences = ax.bar([self._book_1.title, self._book_2.title], max_sentences, color="peru", width=0.2)
        ax.bar_label(max_sentences, label_type="center")
        figure.tight_layout()

        canvas.draw()
