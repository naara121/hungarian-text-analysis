from operator import itemgetter
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from seaborn import regplot

from controller.book_controller import BookController
from controller.magyarlanc_controller import MagyarlancController
from view.lexical_properties_window import FifthCompareWorksWindow


class PosWordsAndSimilarityWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(PosWordsAndSimilarityWindow, self).__init__()
        loadUi(Path("view/ui/pos_words_and_similarity_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._book_controller = BookController()
        self._magyarlanc_controller = MagyarlancController()

        self.set_labels()

        self.prev_screen_button.clicked.connect(self.previous_screen)
        self.next_screen_button.clicked.connect(self.next_screen)

        # first top parts of speech vbox initialization
        self._top_pos_figure_1 = Figure(figsize=(5, 5))
        self._top_pos_canvas_1 = FigureCanvasQTAgg(self._top_pos_figure_1)
        self.top_pos_vbox_1.addWidget(self._top_pos_canvas_1)
        self.top_pos_vbox_1.addWidget(self.pos_label_1)

        # second top parts of speech vbox initialization
        self._top_pos_figure_2 = Figure(figsize=(5, 5))
        self._top_pos_canvas_2 = FigureCanvasQTAgg(self._top_pos_figure_2)
        self.top_pos_vbox_2.addWidget(self._top_pos_canvas_2)
        self.top_pos_vbox_2.addWidget(self.pos_label_2)

        self.init_pos()
        self.pos_event_1()
        self.pos_event_2()

        self.pos_button_1.clicked.connect(self.pos_event_1)
        self.pos_button_2.clicked.connect(self.pos_event_2)

        self.count_textbox.setValidator(QIntValidator(1, 1000, self))

        # scatter vbox initialization
        self._scatter_figure = Figure(figsize=(5, 5))
        self._scatter_canvas = FigureCanvasQTAgg(self._scatter_figure)
        self.scatter_vbox.addWidget(self._scatter_canvas)

        self.create_linear_regressions_scatter_plot(self._scatter_figure, self._scatter_canvas, 10)

        self.corr_button.clicked.connect(self.correlation_event)

    def set_labels(self):
        self.pos_label_1.setText(f"{self._book_1.title} című műben, az adott szófajban a 10 legtöbbször előforduló szó.")
        self.pos_label_1.setFont(QFont("Arial", 10, italic=True))
        self.pos_label_1.setAlignment(Qt.AlignCenter)
        self.pos_label_1.setWordWrap(True)

        self.pos_label_2.setText(f"{self._book_2.title} című műben, az adott szófajban a 10 legtöbbször előforduló szó.")
        self.pos_label_2.setFont(QFont("Arial", 10, italic=True))
        self.pos_label_2.setAlignment(Qt.AlignCenter)
        self.pos_label_2.setWordWrap(True)

        bold_font = QFont("Arial", 10)
        bold_font.setBold(True)

        self.corr_text_label.setFont(QFont("Arial", 10, italic=True))
        self.corr_text_label.setAlignment(Qt.AlignCenter)

        self.corr_label.setFont(bold_font)
        self.p_value_label.setFont(bold_font)
        self.coef_label.setFont(bold_font)

        self.similarity_label.setFont(bold_font)
        self.sim_value_label.setFont(bold_font)

        self.pearson_label.setFont(QFont("Arial", 10))
        self.spearman_label.setFont(QFont("Arial", 10))
        self.kendall_label.setFont(QFont("Arial", 10))
        self.cosine_label.setFont(QFont("Arial", 10))
        self.jaccard_label.setFont(QFont("Arial", 10))

        bold_italic_font = QFont("Arial", 10, italic=True)
        bold_italic_font.setBold(True)

        self.pearson_p_value.setFont(bold_italic_font)
        self.spearman_p_value.setFont(bold_italic_font)
        self.kendall_p_value.setFont(bold_italic_font)

        self.pearson_coef.setFont(bold_italic_font)
        self.spearman_coef.setFont(bold_italic_font)
        self.kendall_coef.setFont(bold_italic_font)

        self.set_cosine_similarity()

        self.set_jaccard_similarity()

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def next_screen(self):
        self._widgets.addWidget(FifthCompareWorksWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def init_pos(self):
        pos_list = ["Főnév", "Melléknév", "Számnév", "Tulajdonnév", "Névmás", "Ige", "Határozószó", "Kötőszó"]

        self.pos_combo_box_1.addItems(pos_list)
        self.pos_combo_box_1.setCurrentIndex(0)

        self.pos_combo_box_2.addItems(pos_list)
        self.pos_combo_box_2.setCurrentIndex(0)

    def pos_event_1(self):
        self.create_pos_bar_plot(self._top_pos_figure_1, self._top_pos_canvas_1, self.pos_combo_box_1, self._book_1.writer, self._book_1.filename)

    def pos_event_2(self):
        self.create_pos_bar_plot(self._top_pos_figure_2, self._top_pos_canvas_2, self.pos_combo_box_2, self._book_2.writer, self._book_2.filename)

    def create_pos_bar_plot(self, figure, canvas, combo_box, writer, filename):
        result = self._magyarlanc_controller.get_magyaralanc_out(writer, filename).content.split("\n")

        figure.clear()

        words = self._magyarlanc_controller.get_top_pos(result, combo_box.currentText())

        sorted_words = dict(sorted(words.items(), key=itemgetter(1), reverse=True)[:10])

        ax = figure.add_subplot(111)
        ax.barh(list(sorted_words.keys()), list(sorted_words.values()), height=0.5, color="cornflowerblue")
        ax.invert_yaxis()

        canvas.draw()

    def correlation_event(self):
        count = 10
        if self.count_textbox.text() == "":
            count = 0
        else:
            count = int(self.count_textbox.text())

        self.create_linear_regressions_scatter_plot(self._scatter_figure, self._scatter_canvas, count)

    def create_linear_regressions_scatter_plot(self, figure, canvas, count):
        if count > 1000:
            count = 1000

        result = self._book_controller.get_labeled_words(self._book_1, self._book_2, count)

        figure.clear()

        ax = figure.add_subplot(111)
        regplot(x=result[0], y=result[1], ax=ax, scatter_kws={"color": "black"}, line_kws={"color": "red"})

        canvas.draw()

        self.set_pearson_correlation(result[0], result[1])
        self.set_spearman_correlation(result[0], result[1])
        self.set_kendall_correlation(result[0], result[1])

    def set_pearson_correlation(self, label_1, label_2):
        pearson = self._book_controller.get_pearsonr_correlation(label_1, label_2)
        self.pearson_coef.setText(str(round(pearson[0], 2)))
        self.pearson_p_value.setText(str(round(pearson[1], 2)))

    def set_spearman_correlation(self, label_1, label_2):
        spearman = self._book_controller.get_spearman_correlation(label_1, label_2)
        self.spearman_coef.setText(str(round(spearman[0], 2)))
        self.spearman_p_value.setText(str(round(spearman[1], 2)))

    def set_kendall_correlation(self, label_1, label_2):
        kendall = self._book_controller.get_kendall_correlation(label_1, label_2)
        self.kendall_coef.setText(str(round(kendall[0], 2)))
        self.kendall_p_value.setText(str(round(kendall[1], 2)))

    def set_cosine_similarity(self):
        bold_italic_font = QFont("Arial", 10, italic=True)
        bold_italic_font.setBold(True)

        self.cosine_value_label.setText(str(round(self._book_controller.get_cosine_similarity(self._book_1, self._book_2), 2)))
        self.cosine_value_label.setFont(bold_italic_font)

    def set_jaccard_similarity(self):
        bold_italic_font = QFont("Arial", 10, italic=True)
        bold_italic_font.setBold(True)

        self.jaccard_value_label.setText(str(round(self._book_controller.get_jaccard_similarity(self._book_1.content, self._book_2.content), 2)))
        self.jaccard_value_label.setFont(bold_italic_font)
