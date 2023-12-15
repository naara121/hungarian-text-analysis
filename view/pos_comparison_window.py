from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from numpy import arange

from controller.book_controller import BookController
from controller.magyarlanc_controller import MagyarlancController
from view.pos_words_and_similarity_window import PosWordsAndSimilarityWindow


class PosComparisonWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(PosComparisonWindow, self).__init__()
        loadUi(Path("view/ui/pos_comparison_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._magyarlanc_controller = MagyarlancController()
        self._book_controller = BookController()

        self._sorted_pos_1 = self._magyarlanc_controller.get_magyaralanc_out(self._book_1.writer, self._book_1.filename).sorted_pos
        self._sorted_pos_2 = self._magyarlanc_controller.get_magyaralanc_out(self._book_2.writer, self._book_2.filename).sorted_pos

        self.prev_screen_button.clicked.connect(self.previous_screen)
        self.next_screen_button.clicked.connect(self.next_screen)

        # first vbox initialization
        self._figure_1 = Figure(figsize=(5, 5))
        self._canvas_1 = FigureCanvasQTAgg(self._figure_1)
        self.vbox_1.addWidget(self._canvas_1)
        self.vbox_1.addWidget(self.pos_pie_label_1)
        self.vbox_1.addWidget(self.themes_1)
        self.vbox_1.addWidget(self.page_number_label_1)

        # second vbox initialization
        self._figure_2 = Figure(figsize=(5, 5))
        self._canvas_2 = FigureCanvasQTAgg(self._figure_2)
        self.vbox_2.addWidget(self._canvas_2)
        self.vbox_2.addWidget(self.pos_pie_label_2)
        self.vbox_2.addWidget(self.themes_2)
        self.vbox_2.addWidget(self.page_number_label_2)

        self.set_labels()

        self.create_parts_of_speech_chart(self._sorted_pos_1, self._figure_1, self._canvas_1)
        self.create_parts_of_speech_chart(self._sorted_pos_2, self._figure_2, self._canvas_2)

        self.set_themes()

        # pos comparison vbox initialization
        self._pos_comp_figure = Figure(figsize=(9, 9))
        self._pos_comp_canvas = FigureCanvasQTAgg(self._pos_comp_figure)
        self.pos_vbox.addWidget(self._pos_comp_canvas)
        self.pos_vbox.addWidget(self.pos_comp_label)

        self.create_parts_of_speech_comparison_bar_plot(self._pos_comp_figure, self._pos_comp_canvas)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def next_screen(self):
        self._widgets.addWidget(PosWordsAndSimilarityWindow(self._widgets, self._book_1, self._book_2))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def set_labels(self):
        title_font = QFont("Arial", 20)
        title_font.setBold(True)

        self.title_1.setText(
            f"Jókai Mór: {self._book_1.title}" if self._book_1.writer == "jokai" else f"Móricz Zsigmond: {self._book_1.title}")
        self.title_1.setFont(title_font)
        self.title_1.setAlignment(Qt.AlignCenter)

        self.title_2.setText(
            f"Jókai Mór: {self._book_2.title}" if self._book_2.writer == "jokai" else f"Móricz Zsigmond: {self._book_2.title}")
        self.title_2.setFont(title_font)
        self.title_2.setAlignment(Qt.AlignCenter)

        self.pos_pie_label_1.setFont(QFont("Arial", 10, italic=True))
        self.pos_pie_label_1.setAlignment(Qt.AlignCenter)
        self.pos_pie_label_1.setWordWrap(True)

        self.pos_pie_label_2.setFont(QFont("Arial", 10, italic=True))
        self.pos_pie_label_2.setAlignment(Qt.AlignCenter)
        self.pos_pie_label_2.setWordWrap(True)

        self.pos_comp_label.setFont(QFont("Arial", 10, italic=True))
        self.pos_comp_label.setAlignment(Qt.AlignCenter)
        self.pos_comp_label.setWordWrap(True)

        self.page_number_label_1.setText(f"A mű összesen {self._book_1.page_number} oldalból áll.")
        self.page_number_label_1.setFont(QFont("Arial", 10, italic=True))
        self.page_number_label_1.setAlignment(Qt.AlignCenter)

        self.page_number_label_2.setText(f"A mű összesen {self._book_2.page_number} oldalból áll.")
        self.page_number_label_2.setFont(QFont("Arial", 10, italic=True))
        self.page_number_label_2.setAlignment(Qt.AlignCenter)

    def set_themes(self):
        self.themes_1.setText(f"Az adott mű témái: {self._book_1.themes}")
        self.themes_1.setFont(QFont("Arial", 10, italic=True))
        self.themes_1.setAlignment(Qt.AlignCenter)
        self.themes_1.setWordWrap(True)

        self.themes_2.setText(f"Az adott mű témái: {self._book_2.themes}")
        self.themes_2.setFont(QFont("Arial", 10, italic=True))
        self.themes_2.setAlignment(Qt.AlignCenter)
        self.themes_2.setWordWrap(True)

    def create_parts_of_speech_chart(self, sorted_pos, figure, canvas):
        figure.clear()

        ax = figure.add_subplot(111)
        ax.pie(sorted_pos.values())
        percentage_legend = ax.legend(labels=self.set_percentage(sorted_pos), bbox_to_anchor=(1, 1), fontsize=10)
        ax.legend(labels=sorted_pos.keys(), bbox_to_anchor=(0, 1), fontsize=10)
        ax.add_artist(percentage_legend)

        canvas.draw()

    def set_percentage(self, sorted_pos):
        values = sum(sorted_pos.values())

        percentage = list()

        for word, value in sorted_pos.items():
            perc = round(((value / values) * 100), 2)
            percentage.append(f"{perc}%")

        return percentage

    def create_parts_of_speech_comparison_bar_plot(self, figure, canvas):
        figure.clear()

        label = list(self._sorted_pos_1.keys()) if len(self._sorted_pos_1.keys()) > len(self._sorted_pos_2.keys()) else list(self._sorted_pos_2.keys())

        try:
            label[label.index("Határozószó")] = "Határozó-\nszó"
            label[label.index("Tulajdonnév")] = "Tulajdon-\nnév"
            label[label.index("Determináns")] = "Deter-\nmináns"
            label[label.index("Alárendelő kötőszó")] = "Alárendelő\nkötőszó"
            label[label.index("Elöljáró és névutó")] = "Elöljáró és\nnévutó"
        except ValueError:
            pass

        pos_1 = self.create_pos_dict(label, self._sorted_pos_1)
        pos_2 = self.create_pos_dict(label, self._sorted_pos_2)

        ax = figure.add_subplot(111)
        jokai_pos = ax.bar(arange(len(pos_1.values())) - 0.25, pos_1.values(),
                           color="mediumpurple", label=self._book_1.title, width=0.5)
        moricz_pos = ax.bar(arange(len(pos_2.values())) + 0.25, pos_2.values(), color="coral",
                            label=self._book_2.title, width=0.5)
        ax.bar_label(jokai_pos, label_type="center")
        ax.bar_label(moricz_pos, label_type="center")
        ax.legend()
        ax.set_xticks(arange(len(label)), labels=label)

        canvas.draw()

    def create_pos_dict(self, _list, pos_dict):
        mod_dict = {"Határozószó": "Határozó-\nszó", "Tulajdonnév": "Tulajdon-\nnév", "Determináns": "Deter-\nmináns",
                    "Alárendelő kötőszó": "Alárendelő\nkötőszó", "Elöljáró és névutó": "Elöljáró és\nnévutó"
                    }

        pos_list = list(pos_dict.keys())

        for key, value in mod_dict.items():
            if key not in pos_list:
                continue

            pos_dict[value] = pos_dict.pop(key)

        pos = dict()

        for pos_v in _list:
            value = pos_dict.get(pos_v)
            if value is None:
                continue

            pos[pos_v] = value

        return pos
