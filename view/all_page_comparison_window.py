from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from controller.book_controller import BookController
from controller.magyarlanc_controller import MagyarlancController


class BookComparisonWindow(QDialog):
    def __init__(self, widgets):
        super(BookComparisonWindow, self).__init__()
        loadUi(Path("view/ui/all_page_comparison_window.ui"), self)
        widgets.resize(1920, 1080)

        self._widgets = widgets
        self._book_controller = BookController()
        self._magyarlanc_controller = MagyarlancController()
        self._jokai_num = self._book_controller.get_all_book_page_numbers("jokai")
        self._moricz_num = self._book_controller.get_all_book_page_numbers("moricz")

        self.set_labels()
        self.prev_screen_button.clicked.connect(self.previous_screen)

        self._scatter_figure = Figure(figsize=(5, 5))
        self._scatter_canvas = FigureCanvasQTAgg(self._scatter_figure)
        self.scatter_vbox.addWidget(self._scatter_canvas)
        self.scatter_vbox.addWidget(self.scatter_label)

        self.create_page_number_scatter_plot(self._scatter_figure, self._scatter_canvas)

        self._min_figure = Figure(figsize=(5, 5))
        self._min_canvas = FigureCanvasQTAgg(self._min_figure)
        self.shortest_book_vbox.addWidget(self._min_canvas)
        self.shortest_book_vbox.addWidget(self.short_label)

        self.create_min_page_bar_plot(self._min_figure, self._min_canvas)

        self._max_figure = Figure(figsize=(5, 5))
        self._max_canvas = FigureCanvasQTAgg(self._max_figure)
        self.longest_book_vbox.addWidget(self._max_canvas)
        self.longest_book_vbox.addWidget(self.long_label)

        self.create_max_page_bar_plot(self._max_figure, self._max_canvas)

        self._page_number_figure = Figure(figsize=(5, 5))
        self._page_number_canvas = FigureCanvasQTAgg(self._page_number_figure)
        self.page_number_vbox.addWidget(self._page_number_canvas)
        self.page_number_vbox.addWidget(self.page_number_label)

        self.create_page_number_bar_plot(self._page_number_figure, self._page_number_canvas)

        self._avg_page_number_figure = Figure(figsize=(5, 5))
        self._avg_page_number_canvas = FigureCanvasQTAgg(self._avg_page_number_figure)
        self.avg_page_number_vbox.addWidget(self._avg_page_number_canvas)
        self.avg_page_number_vbox.addWidget(self.avg_label)

        self.create_avg_page_number_bar_plot(self._avg_page_number_figure, self._avg_page_number_canvas)

    def set_labels(self):
        self.scatter_label.setText("Jókai Mór és Móricz Zsigmond műveinek eloszlása az oldalszámuk alapján.")
        self.scatter_label.setFont(QFont("Arial", 10, italic=True))
        self.scatter_label.setAlignment(Qt.AlignCenter)
        self.scatter_label.setWordWrap(True)

        self.page_number_label.setText("Jókai Mór és Móricz Zsigmond összes oldalának száma.")
        self.page_number_label.setFont(QFont("Arial", 10, italic=True))
        self.page_number_label.setAlignment(Qt.AlignCenter)
        self.page_number_label.setWordWrap(True)

        self.short_label.setText("Legrövidebb művek.")
        self.short_label.setFont(QFont("Arial", 10, italic=True))
        self.short_label.setAlignment(Qt.AlignCenter)
        self.short_label.setWordWrap(True)

        self.long_label.setText("Leghosszabb művek.")
        self.long_label.setFont(QFont("Arial", 10, italic=True))
        self.long_label.setAlignment(Qt.AlignCenter)
        self.long_label.setWordWrap(True)

        self.avg_label.setText("Művek átlagos hossza a két írónál.")
        self.avg_label.setFont(QFont("Arial", 10, italic=True))
        self.avg_label.setAlignment(Qt.AlignCenter)
        self.avg_label.setWordWrap(True)

    def previous_screen(self):
        deletable = self._widgets.currentWidget()
        self._widgets.setCurrentIndex(self._widgets.currentIndex() - 1)
        self._widgets.removeWidget(deletable)
        deletable.deleteLater()

    def create_page_number_scatter_plot(self, figure, canvas):
        figure.clear()

        ax = figure.add_subplot(111)
        ax.scatter(range(len(self._jokai_num)), self._jokai_num, c="red", label="Jókai Mór")
        ax.scatter(range(len(self._moricz_num)), self._moricz_num, c="blue", label="Móricz Zsigmond")

        ax.set_xlabel("Könyvek száma")
        ax.set_ylabel("Oldalszám")

        ax.legend()

        canvas.draw()

    def create_page_number_bar_plot(self, figure, canvas):
        page_num_1 = self._book_controller.get_page_number("jokai", "jokai_osszes_muve")
        page_num_2 = self._book_controller.get_page_number("moricz", "moricz_osszes_muve")

        figure.clear()

        ax = figure.add_subplot(111)
        numbers = ax.bar(["Jókai Mór", "Móricz Zsigmond"], [page_num_1, page_num_2], color="sienna", width=0.2)
        ax.bar_label(numbers, label_type="center")

        canvas.draw()

    def create_min_page_bar_plot(self, figure, canvas):
        figure.clear()

        jokai_result = self._book_controller.get_min_page_number_book("jokai")
        moricz_result = self._book_controller.get_min_page_number_book("moricz")

        ax = figure.add_subplot(111)
        min_page = ax.bar([f"Jókai Mór:\n{jokai_result[0]}", f"Móricz Zsigmond:\n{moricz_result[0]}"],
                          [jokai_result[1], moricz_result[1]], color="sienna", width=0.2)
        ax.bar_label(min_page, label_type="center")

        canvas.draw()

    def create_max_page_bar_plot(self, figure, canvas):
        figure.clear()

        jokai_result = self._book_controller.get_max_page_number_book("jokai")
        moricz_result = self._book_controller.get_max_page_number_book("moricz")

        ax = figure.add_subplot(111)
        min_page = ax.bar([f"Jókai Mór:\n{jokai_result[0]}", f"Móricz Zsigmond:\n{moricz_result[0]}"],
                          [jokai_result[1], moricz_result[1]], color="sienna", width=0.2)
        ax.bar_label(min_page, label_type="center")

        canvas.draw()

    def create_avg_page_number_bar_plot(self, figure, canvas):
        jokai_num = round(sum(self._jokai_num) / len(self._jokai_num), 2)
        moricz_num = round(sum(self._moricz_num) / len(self._moricz_num), 2)

        figure.clear()

        ax = figure.add_subplot(111)
        numbers = ax.bar(["Jókai Mór", "Móricz Zsigmond"], [jokai_num, moricz_num], color="sienna", width=0.2)
        ax.bar_label(numbers, label_type="center")

        canvas.draw()
