from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from controller.magyarlanc_controller import MagyarlancController


class RootDependencyRelationWindow(QDialog):
    def __init__(self, widgets, book_1, book_2):
        super(RootDependencyRelationWindow, self).__init__()
        loadUi(Path("view/ui/dependency_relation_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_1 = book_1
        self._book_2 = book_2
        self._magyarlanc_controller = MagyarlancController()

        self._relation_1 = self._magyarlanc_controller.get_dependency_relation_counts(self._book_1.writer, self._book_1.filename, "ROOT")
        self._relation_2 = self._magyarlanc_controller.get_dependency_relation_counts(self._book_2.writer, self._book_2.filename, "ROOT")

        self.set_labels()

        self.prev_screen_button.clicked.connect(self.previous_screen)

        self._relation_figure_1 = Figure(figsize=(5, 5))
        self._relation_canvas_1 = FigureCanvasQTAgg(self._relation_figure_1)
        self.relation_vbox_1.addWidget(self._relation_canvas_1)
        self.relation_vbox_1.addWidget(self.relation_label_1)

        self._relation_figure_2 = Figure(figsize=(5, 5))
        self._relation_canvas_2 = FigureCanvasQTAgg(self._relation_figure_2)
        self.relation_vbox_2.addWidget(self._relation_canvas_2)
        self.relation_vbox_2.addWidget(self.relation_label_2)

        self.create_root_dependency_relation_bar_plot(self._relation_figure_1, self._relation_canvas_1, self._relation_1[0])
        self.create_root_dependency_relation_bar_plot(self._relation_figure_2, self._relation_canvas_2, self._relation_2[0])

        self._pos_figure_1 = Figure(figsize=(5, 5))
        self._pos_canvas_1 = FigureCanvasQTAgg(self._pos_figure_1)
        self.relation_pos_vbox_1.addWidget(self._pos_canvas_1)

        self._pos_figure_2 = Figure(figsize=(5, 5))
        self._pos_canvas_2 = FigureCanvasQTAgg(self._pos_figure_2)
        self.relation_pos_vbox_2.addWidget(self._pos_canvas_2)

        self.create_root_pos_bar_plot(self._pos_figure_1, self._pos_canvas_1, self._relation_1[2])
        self.create_root_pos_bar_plot(self._pos_figure_2, self._pos_canvas_2, self._relation_2[2])

        self._avg_figure = Figure(figsize=(5, 5))
        self._avg_canvas = FigureCanvasQTAgg(self._avg_figure)
        self.avg_vbox.addWidget(self._avg_canvas)
        self.avg_vbox.addWidget(self.avg_label)

        self.create_root_avg_bar_plot(self._avg_figure, self._avg_canvas, self._relation_1[1], self._relation_2[1])

    def set_labels(self):
        title_font = QFont("Arial", 16)
        title_font.setBold(True)

        self.title_label.setText("A mondatok gyökerének előfordulása")
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)

        self.relation_label_1.setText(f"{self._book_1.title} című műben, a mondatok gyökere közül legtöbbszőr előforduló 10 szótő.")
        self.relation_label_1.setFont(QFont("Arial", 12, italic=True))
        self.relation_label_1.setAlignment(Qt.AlignCenter)
        self.relation_label_1.setWordWrap(True)

        self.relation_label_2.setText(f"{self._book_2.title} című műben, a mondatok gyökere közül legtöbbszőr előforduló 10 szótő.")
        self.relation_label_2.setFont(QFont("Arial", 12, italic=True))
        self.relation_label_2.setAlignment(Qt.AlignCenter)
        self.relation_label_2.setWordWrap(True)

        self.avg_label.setText("A két mű mondataiban átlagosan hanyadik szó a mondat gyökere.")
        self.avg_label.setFont(QFont("Arial", 12, italic=True))
        self.avg_label.setAlignment(Qt.AlignCenter)
        self.avg_label.setWordWrap(True)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def create_root_dependency_relation_bar_plot(self, figure, canvas, root_dict):
        figure.clear()

        ax = figure.add_subplot(111)
        ax.barh(list(root_dict.keys())[:10], list(root_dict.values())[:10], height=0.5, color="chocolate")
        ax.invert_yaxis()

        canvas.draw()

    def create_root_pos_bar_plot(self, figure, canvas, pos_dict):
        figure.clear()

        ax = figure.add_subplot(111)
        ax.bar(list(pos_dict.keys())[:5], list(pos_dict.values())[:5], width=0.5, color="tomato")
        figure.tight_layout()

        canvas.draw()

    def create_root_avg_bar_plot(self, figure, canvas, avg_root_1, avg_root_2):
        figure.clear()

        averages = [float(round(avg_root_1, 2)), float(round(avg_root_2, 2))]

        ax = figure.add_subplot(111)
        bars = ax.bar([self._book_1.title, self._book_2.title], averages, color="peru", width=0.2)
        ax.bar_label(bars, label_type="center")
        figure.tight_layout()

        canvas.draw()
