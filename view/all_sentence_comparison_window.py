from collections import Counter
from multiprocessing import Process
from pathlib import Path
from re import sub

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from controller.book_controller import BookController
from controller.magyarlanc_controller import MagyarlancController
from view.all_top_words_window import AllTopWordsWindow
from view.sentence_comparison_window import SentenceComparisonWindow


class AllSentenceComparisonWindow(QDialog):
    def __init__(self, widgets):
        super(AllSentenceComparisonWindow, self).__init__()
        loadUi(Path("view/ui/all_sentence_comparison_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_controller = BookController()
        self._magyarlanc_controller = MagyarlancController()

        self._out_1 = self._magyarlanc_controller.get_magyaralanc_out("jokai", "jokai_osszes_muve")
        self._out_2 = self._magyarlanc_controller.get_magyaralanc_out("moricz", "moricz_osszes_muve")

        self._all_words_1 = self._out_1.all_words
        self._all_words_2 = self._out_2.all_words

        self._jokai_vocab = (sub(r"[^\w\s]", "", self._all_words_1)
                             .lower()
                             )

        self._moricz_vocab = (sub(r"[^\w\s]", "", self._all_words_2)
                              .lower()
                              )

        self._sentence_1 = self._jokai_vocab.split("\n")
        self._sentence_2 = self._moricz_vocab.split("\n")

        self.prev_screen_button.clicked.connect(self.previous_screen)
        self.next_screen_button.clicked.connect(self.next_screen)

        self.set_labels()
        self.init_work_combo_boxes()

        self.comparison_button.clicked.connect(self.comparison)

        self._all_words_figure = Figure(figsize=(5, 5))
        self._all_words_canvas = FigureCanvasQTAgg(self._all_words_figure)
        self.all_words_vbox.addWidget(self._all_words_canvas)
        self.all_words_vbox.addWidget(self.all_words_label)

        self.create_all_words_comparison_bar_plot(self._all_words_figure, self._all_words_canvas)

        self._vocab_figure = Figure(figsize=(5, 5))
        self._vocab_canvas = FigureCanvasQTAgg(self._vocab_figure)
        self.vocab_vbox.addWidget(self._vocab_canvas)
        self.vocab_vbox.addWidget(self.vocab_label)

        self.create_vocab_comparison_bar_plot(self._vocab_figure, self._vocab_canvas)

        # sentences vbox initialization
        self._sentences_figure = Figure(figsize=(5, 5))
        self._sentences_canvas = FigureCanvasQTAgg(self._sentences_figure)
        self.sentences_vbox.addWidget(self._sentences_canvas)
        self.sentences_vbox.addWidget(self.sentences_label)

        create_sentences_process = Process(
            target=self.create_sentence_comparison_bar_plot(self._sentences_figure, self._sentences_canvas))

        # avg sentences vbox initialization
        self._avg_sentences_figure = Figure(figsize=(5, 5))
        self._avg_sentences_canvas = FigureCanvasQTAgg(self._avg_sentences_figure)
        self.avg_sentences_vbox.addWidget(self._avg_sentences_canvas)
        self.avg_sentences_vbox.addWidget(self.avg_sentence_label)

        self.create_avg_sentence_length_bar_plot(self._avg_sentences_figure, self._avg_sentences_canvas,
                                                 self._sentence_1, self._sentence_2)

        # max sentences vbox initialization
        self._max_sentences_figure = Figure(figsize=(5, 5))
        self._max_sentences_canvas = FigureCanvasQTAgg(self._max_sentences_figure)
        self.max_sentence_vbox.addWidget(self._max_sentences_canvas)
        self.max_sentence_vbox.addWidget(self.max_sentence_label)

        create_max_sentence_process = Process(
            target=self.create_max_sentence_bar_plot(self._max_sentences_figure, self._max_sentences_canvas))

        create_sentences_process.start()
        create_max_sentence_process.start()

        create_sentences_process.join()
        create_max_sentence_process.join()

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def next_screen(self):
        self._widgets.addWidget(AllTopWordsWindow(self._widgets, self._out_1, self._out_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def set_labels(self):
        title_font = QFont("Arial", 10)
        title_font.setBold(True)

        self.compare_label.setFont(QFont("Arial", 10, italic=True))
        self.compare_label.setAlignment(Qt.AlignCenter)

        self.all_words_label.setFont(QFont("Arial", 10, italic=True))
        self.all_words_label.setAlignment(Qt.AlignCenter)
        self.all_words_label.setWordWrap(True)

        self.vocab_label.setFont(QFont("Arial", 10, italic=True))
        self.vocab_label.setAlignment(Qt.AlignCenter)
        self.vocab_label.setWordWrap(True)

        self.sentences_label.setFont(QFont("Arial", 10, italic=True))
        self.sentences_label.setAlignment(Qt.AlignCenter)
        self.sentences_label.setWordWrap(True)

        self.avg_sentence_label.setFont(QFont("Arial", 10, italic=True))
        self.avg_sentence_label.setAlignment(Qt.AlignCenter)
        self.avg_sentence_label.setWordWrap(True)

        self.max_sentence_label.setFont(QFont("Arial", 10, italic=True))
        self.max_sentence_label.setAlignment(Qt.AlignCenter)
        self.max_sentence_label.setWordWrap(True)

        self.writer_label.setFont(title_font)
        self.less_than_10_label.setFont(title_font)
        self.less_than_50_label.setFont(title_font)
        self.less_than_100_label.setFont(title_font)
        self.more_than_100_label.setFont(title_font)

        self.jokai_label.setFont(QFont("Arial", 10))
        self.jokai_less_than_10_label.setFont(QFont("Arial", 10))
        self.jokai_less_than_50_label.setFont(QFont("Arial", 10))
        self.jokai_less_than_100_label.setFont(QFont("Arial", 10))
        self.jokai_more_than_100_label.setFont(QFont("Arial", 10))

        self.moricz_label.setFont(QFont("Arial", 10))
        self.moricz_less_than_10_label.setFont(QFont("Arial", 10))
        self.moricz_less_than_50_label.setFont(QFont("Arial", 10))
        self.moricz_less_than_100_label.setFont(QFont("Arial", 10))
        self.moricz_more_than_100_label.setFont(QFont("Arial", 10))
    def init_work_combo_boxes(self):
        all_titles = self._book_controller.get_all_book_titles("jokai")
        all_titles.extend(self._book_controller.get_all_book_titles("moricz"))

        self.works_combo_box_1.addItems(all_titles)
        self.works_combo_box_1.setCurrentIndex(0)

        self.works_combo_box_2.addItems(all_titles)
        self.works_combo_box_2.setCurrentIndex(0)

    def comparison(self):
        combo_text_1 = self.works_combo_box_1.currentText().split(": ")
        combo_text_2 = self.works_combo_box_2.currentText().split(": ")

        writer_1 = "jokai"
        writer_2 = "jokai"

        if combo_text_1[0] == "Moricz Zsigmond":
            writer_1 = "moricz"

        if combo_text_2[0] == "Moricz Zsigmond":
            writer_2 = "moricz"

        title_1 = combo_text_1[1]
        title_2 = combo_text_2[1]

        if title_1 == title_2:
            self.create_message_button(
                "A két mű megegyezik",
                "A műveket nem lehet önmagukkal összehasonlítani!",
                "",
                QMessageBox.Information
            )
            return None

        book_1 = self._book_controller.get_one_book_by_title(writer_1, title_1)
        book_2 = self._book_controller.get_one_book_by_title(writer_2, title_2)

        self._widgets.addWidget(SentenceComparisonWindow(self._widgets, book_1, book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def create_message_button(self, window_title, text, informative_text, icon):
        msg = QMessageBox()
        msg.setWindowTitle(window_title)
        msg.setText(text)
        msg.setInformativeText(informative_text)
        msg.setIcon(icon)
        msg.exec_()

    def create_all_words_comparison_bar_plot(self, figure, canvas):
        figure.clear()

        ax = figure.add_subplot(111)
        bars = ax.bar(["Jókai Mór", "Móricz Zsigmond"], [len(self._jokai_vocab.split(" ")), len(self._moricz_vocab.split(" "))],
                      color="salmon", width=0.4)
        ax.bar_label(bars, label_type="center")
        figure.tight_layout()

        canvas.draw()

    def create_vocab_comparison_bar_plot(self, figure, canvas):
        figure.clear()

        ax = figure.add_subplot(111)
        bars = ax.bar(["Jókai Mór", "Móricz Zsigmond"], [len(set(self._jokai_vocab.split(" "))), len(set(self._moricz_vocab.split(" ")))],
                      color="salmon", width=0.2)
        ax.bar_label(bars, label_type="center")
        figure.tight_layout()

        canvas.draw()

    def create_sentence_comparison_bar_plot(self, figure, canvas):
        figure.clear()

        ax = figure.add_subplot(111)
        sentences = ax.bar(["Jókai Mór", "Móricz Zsigmond"], [len(self._sentence_1), len(self._sentence_2)],
                           color="sandybrown", width=0.2)
        ax.bar_label(sentences, label_type="center")
        figure.tight_layout()

        canvas.draw()

    def create_max_sentence_bar_plot(self, figure, canvas):
        max_sentence_1 = max(self._sentence_1, key=len).split(" ")
        max_sentence_2 = max(self._sentence_2, key=len).split(" ")

        figure.clear()

        ax = figure.add_subplot(111)
        max_sentences = ax.bar(["Jókai Mór", "Móricz Zsigmond"], [len(max_sentence_1), len(max_sentence_2)],
                               color="sienna", width=0.2)
        ax.bar_label(max_sentences, label_type="center")
        figure.tight_layout()

        canvas.draw()

    def create_avg_sentence_length_bar_plot(self, figure, canvas, sentence_1, sentence_2):
        figure.clear()

        sent_1 = [len(sent.split(" ")) for sent in sentence_1]
        sent_2 = [len(sent.split(" ")) for sent in sentence_2]

        max_sentences = [round(sum(sent_1) / len(sent_1), 2), round(sum(sent_2) / len(sent_2), 2)]

        ax = figure.add_subplot(111)
        max_sentences = ax.bar(["Jókai Mór", "Móricz Zsigmond"], max_sentences, color="peru", width=0.2)
        ax.bar_label(max_sentences, label_type="center")
        figure.tight_layout()

        canvas.draw()

        self.create_avg_table(sent_1, self.jokai_less_than_10_label, self.jokai_less_than_50_label, self.jokai_less_than_100_label, self.jokai_more_than_100_label)
        self.create_avg_table(sent_2, self.moricz_less_than_10_label, self.moricz_less_than_50_label, self.moricz_less_than_100_label, self.moricz_more_than_100_label)

    def create_avg_table(self, sentence, below_10_label, below_50_label, below_100_label, more_than_100_label):
        below_10 = 0
        below_50 = 0
        below_100 = 0
        abv_100 = 0

        for k, v in Counter(sentence).items():
            if int(k) < 10:
                below_10 += v
            elif 10 <= int(k) < 50:
                below_50 += v
            elif 50 <= int(k) < 100:
                below_100 += v
            else:
                abv_100 += v

        below_10_label.setText(str(below_10))
        below_50_label.setText(str(below_50))
        below_100_label.setText(str(below_100))
        more_than_100_label.setText(str(abv_100))
