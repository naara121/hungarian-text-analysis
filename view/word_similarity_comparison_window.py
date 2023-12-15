from multiprocessing import Process, Queue
from pathlib import Path
from re import sub

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from controller.book_controller import BookController
from controller.magyarlanc_controller import MagyarlancController
from utils.logger import Logger
from view.pos_comparison_window import PosComparisonWindow


class WordSimilarityComparisonWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(WordSimilarityComparisonWindow, self).__init__()
        loadUi(Path("view/ui/word_similarity_comparison_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._magyarlanc_controller = MagyarlancController()
        self._book_controller = BookController()
        self._logger = Logger()

        self._all_words_1 = sub(r"(?<=[0-9])([a-zA-Z]+)", "", self._magyarlanc_controller.get_magyaralanc_out(self._book_1.writer, self._book_1.filename).all_words)

        self._all_words_2 = sub(r"(?<=[0-9])([a-zA-Z]+)", "", self._magyarlanc_controller.get_magyaralanc_out(self._book_2.writer, self._book_2.filename).all_words)

        self.prev_screen_button.clicked.connect(self.previous_screen)
        self.next_screen_button.clicked.connect(self.next_screen)

        self.set_labels()

        self._similar_words_figure_1 = Figure(figsize=(5, 5))
        self._similar_words_canvas_1 = FigureCanvasQTAgg(self._similar_words_figure_1)
        self.similar_words_vbox_1.addWidget(self._similar_words_canvas_1)
        self.similar_words_vbox_1.addWidget(self.word_similarity_label_1)

        self._similar_words_figure_2 = Figure(figsize=(5, 5))
        self._similar_words_canvas_2 = FigureCanvasQTAgg(self._similar_words_figure_2)
        self.similar_words_vbox_2.addWidget(self._similar_words_canvas_2)
        self.similar_words_vbox_2.addWidget(self.word_similarity_label_2)

        self._similarity_queue = Queue()

        similarity_process_1 = Process(
            self._magyarlanc_controller.get_word_similarity(self._similarity_queue, self._all_words_1))
        similarity_process_2 = Process(
            self._magyarlanc_controller.get_word_similarity(self._similarity_queue, self._all_words_2))

        similarity_process_1.start()
        similarity_process_2.start()

        similarity_process_1.join()
        similarity_process_2.join()

        self._word_similarity_model_1 = self._similarity_queue.get()
        self._word_similarity_model_2 = self._similarity_queue.get()

        self.similar_words_button_1.clicked.connect(self.get_word_similarity_1)
        self.similar_words_button_2.clicked.connect(self.get_word_similarity_2)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def next_screen(self):
        self._widgets.addWidget(PosComparisonWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def set_labels(self):
        self.word_similarity_label_1.setText(
            f"{self._book_1.title} című mű szövegkörnyezetében, az adott szó körül előforduló szavak.")
        self.word_similarity_label_1.setFont(QFont("Arial", 12, italic=True))
        self.word_similarity_label_1.setAlignment(Qt.AlignCenter)
        self.word_similarity_label_1.setWordWrap(True)

        self.word_similarity_label_2.setText(
            f"{self._book_2.title} című mű szövegkörnyezetében, az adott szó körül előforduló szavak.")
        self.word_similarity_label_2.setFont(QFont("Arial", 12, italic=True))
        self.word_similarity_label_2.setAlignment(Qt.AlignCenter)
        self.word_similarity_label_2.setWordWrap(True)

    def get_word_similarity_1(self):
        self.create_word_similarity_bar_plot(self._word_similarity_model_1, self.similar_word_textbox_1.text(),
                                             self._similar_words_figure_1, self._similar_words_canvas_1, "royalblue")

    def get_word_similarity_2(self):
        self.create_word_similarity_bar_plot(self._word_similarity_model_2, self.similar_word_textbox_2.text(),
                                             self._similar_words_figure_2, self._similar_words_canvas_2, "crimson")

    def create_word_similarity_bar_plot(self, model, word, figure, canvas, color):
        if len(word) > 0:
            try:
                similar = dict()
                similar_pairs = model.wv.similar_by_word(word, topn=10)

                for pair in similar_pairs:
                    similar[sub(r"[^\w\s]", "", pair[0])] = pair[1]

                figure.clear()

                ax = figure.add_subplot(111)
                ax.barh(list(similar.keys()), list(similar.values()), height=0.5, color=color)
                ax.invert_yaxis()

                canvas.draw()
            except KeyError:
                self._logger.log("INFO", "Nem található ilyen szó a műben!")
