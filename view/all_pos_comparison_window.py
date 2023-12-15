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
from view.all_page_comparison_window import BookComparisonWindow


class AllPosComparisonWindow(QDialog):
    def __init__(self, widgets, out_1, out_2):
        super(AllPosComparisonWindow, self).__init__()
        loadUi(Path("view/ui/all_pos_comparison_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._out_1 = out_1
        self._out_2 = out_2
        self._book_controller = BookController()
        self._magyarlanc_controller = MagyarlancController()

        self._sorted_pos_1 = self._out_1.sorted_pos
        self._sorted_pos_2 = self._out_2.sorted_pos

        self.next_page_button.clicked.connect(self.next_screen)
        self.prev_page_button.clicked.connect(self.previous_screen)

        self.set_labels()

        self._pie_figure_1 = Figure(figsize=(5, 5))
        self._pie_canvas_1 = FigureCanvasQTAgg(self._pie_figure_1)
        self.pie_vbox_1.addWidget(self._pie_canvas_1)

        self._pie_figure_2 = Figure(figsize=(5, 5))
        self._pie_canvas_2 = FigureCanvasQTAgg(self._pie_figure_2)
        self.pie_vbox_2.addWidget(self._pie_canvas_2)

        self.create_all_work_parts_of_speech_pie_chart(self._sorted_pos_1, self._pie_figure_1, self._pie_canvas_1)
        self.create_all_work_parts_of_speech_pie_chart(self._sorted_pos_2, self._pie_figure_2, self._pie_canvas_2)

        self._pos_comp_figure = Figure(figsize=(9, 9))
        self._pos_comp_canvas = FigureCanvasQTAgg(self._pos_comp_figure)
        self.pos_vbox.addWidget(self._pos_comp_canvas)
        self.pos_vbox.addWidget(self.pos_comp_label)

        self.create_parts_of_speech_comparison_bar_plot(self._pos_comp_figure, self._pos_comp_canvas)

    def next_screen(self):
        self._widgets.addWidget(BookComparisonWindow(self._widgets))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def set_labels(self):
        work_title_font = QFont("Arial", 16)
        work_title_font.setBold(True)

        self.jokai_pie_label.setFont(work_title_font)
        self.jokai_pie_label.setAlignment(Qt.AlignCenter)

        self.moricz_pie_label.setFont(work_title_font)
        self.moricz_pie_label.setAlignment(Qt.AlignCenter)

        self.pos_comp_label.setFont(QFont("Arial", 12, italic=True))
        self.pos_comp_label.setAlignment(Qt.AlignCenter)

    def set_all_words_label(self):
        self.all_words_label.setFont(QFont("Arial", 12, italic=True))
        self.all_words_label.setAlignment(Qt.AlignCenter)
        self.all_words_label.setWordWrap(True)

    def set_vocab_label(self):
        self.vocab_label.setFont(QFont("Arial", 12, italic=True))
        self.vocab_label.setAlignment(Qt.AlignCenter)
        self.vocab_label.setWordWrap(True)

    def set_word_cloud_label(self):
        self.word_cloud_label.setFont(QFont("Arial", 12, italic=True))
        self.word_cloud_label.setAlignment(Qt.AlignCenter)
        self.word_cloud_label.setWordWrap(True)

    def create_all_work_parts_of_speech_pie_chart(self, sorted_pos, figure, canvas):
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

        label = list(self._sorted_pos_1.keys()) if len(self._sorted_pos_1.keys()) > len(
            self._sorted_pos_2.keys()) else list(self._sorted_pos_2.keys())

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
        ax.bar(arange(len(pos_1.values())) - 0.25, pos_1.values(), color="mediumpurple",
               label="Jókai Mór", width=0.5)
        ax.bar(arange(len(pos_2.values())) + 0.25, pos_2.values(), color="coral",
               label="Móricz Zsigmond", width=0.5)
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
