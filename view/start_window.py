from os import listdir
from pathlib import Path

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

from utils.logger import Logger
from utils.resource_downloader import download_pdfs, download_magyarlanc
from utils.sqlite_runner import check_tables, create_tables
from utils.text_processor import TextProcessor
from view.all_sentence_comparison_window import AllSentenceComparisonWindow


class StartWindow(QDialog):
    def __init__(self, widgets):
        super(StartWindow, self).__init__()
        loadUi(Path("view/ui/start_window.ui"), self)
        self.setFixedSize(500, 400)

        self._widgets = widgets
        self._processor = TextProcessor()
        self._logger = Logger()

        self.set_labels()

        create_tables()

        self._logger.log("INFO", "A magyar szövegek elemzését bemutató alkalmazás sikeresen elindult!")

        self.create_database_button.clicked.connect(self.create_database)
        self.download_works_button.clicked.connect(self.download_books)
        self.next_page_button.clicked.connect(self.next_screen)

    def create_database(self):
        try:
            if len(listdir(Path("resources/books/jokai"))) != 41:
                self._logger.log("ERROR", "Jókai Mórnak nincs meg mind a 41 könyve!")
                self.create_message_button(
                    "Hiányzó művek",
                    "Jókai Mórnak nincs meg mind a 41 könyve!",
                    "",
                    QMessageBox.Critical
                )
                return

            if len(listdir(Path("resources/books/moricz"))) != 40:
                self._logger.log("ERROR", "Móricz Zsigmondnak nincs meg mind a 40 könyve!")
                self.create_message_button(
                    "Hiányzó művek",
                    "Móricz Zsigmondnak nincs meg mind a 40 könyve!",
                    "",
                    QMessageBox.Critical
                )
                return

        except FileNotFoundError:
            self._logger.log("ERROR", "Nem találhatóak meg a mappák, amikben az írók művei szerepelnek!")
            self.create_message_button(
                "Hiányzó mappák",
                "Nem találhatóak meg a mappák, amikben az írók művei szerepelnek!\nNyomd meg a művek letöltésére szolgáló gombot!",
                "",
                QMessageBox.Critical
            )
            return

        try:
            download_magyarlanc()
        except Exception:
            self._logger.log("ERROR", "Valami hiba történt a letöltés során.")
            self.create_message_button(
                "Adatbázis létrehozása",
                "Valami hiba történt a letöltés során.",
                "Próbálja meg újra.",
                QMessageBox.Critical
            )
            return
        result = self._processor.processing()
        if result:
            self._logger.log("INFO", "Az adatbázis létrehozása sikeres volt.")
            self.create_message_button(
                "Adatbázis létrehozása",
                "Az adatbázis létrehozása sikeres volt.",
                "",
                QMessageBox.Information
            )
        else:
            self._logger.log("ERROR", "Az adatbázis létrehozása során valami hiba történt.")
            self.create_message_button(
                "Adatbázis létrehozása",
                "Az adatbázis létrehozása során valami hiba történt.",
                "Próbálja meg újra.",
                QMessageBox.Critical
            )

    def download_books(self):
        try:
            self._logger.log("INFO", "A művek letöltése elkezdődött.")
            download_pdfs()
            self._logger.log("INFO", "A művek letöltése befejeződött.")
            self.create_message_button(
                "Sikeres letöltés",
                "A művek letöltése sikeresen befejeződött!",
                "",
                QMessageBox.Information
            )
        except Exception as error:
            self._logger.log("ERROR", error.args[1])
            self.create_message_button(
                "Hiányzó művek",
                error.args[1],
                "",
                QMessageBox.Critical
            )

    def set_labels(self):
        title_font = QFont("Arial", 16)
        title_font.setBold(True)

        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)

    def next_screen(self):
        if check_tables()[0][0] == 0 or check_tables()[1][0] == 0:
            self._logger.log("ERROR", "Az adatbázis üres!")
            self.create_message_button(
                "Üres adatbázis",
                "Az adatbázis üres! Nyomd meg az adatbázis létrehozása gombot!",
                "Csak az adatbázis létrehozása után tekinthetőek meg az elemzések.",
                QMessageBox.Critical
            )
            return
        else:
            if check_tables()[0][0] != 83 or check_tables()[1][0] != 83:
                self._logger.log("ERROR", "Az adatbázisból hiányoznak adatok!")
                self.create_message_button(
                    "Hiányzó adatok",
                    "Az adatbázisból hiányoznak adatok! Nyomd meg az adatbázis létrehozása gombot!",
                    "Csak az adatbázis létrehozása után tekinthetőek meg az elemzések.",
                    QMessageBox.Critical
                )
                return

        self._widgets.addWidget(AllSentenceComparisonWindow(self._widgets))
        self._widgets.setCurrentIndex(self._widgets.currentIndex() + 1)

    def create_message_button(self, window_title, text, informative_text, icon):
        msg = QMessageBox()
        msg.setWindowTitle(window_title)
        msg.setText(text)
        msg.setInformativeText(informative_text)
        msg.setIcon(icon)
        msg.exec_()
