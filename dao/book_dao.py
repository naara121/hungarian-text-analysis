from collections import Counter
from os.path import isdir
from pathlib import Path
from sqlite3 import connect

from model.book_entity import BookEntity


class BookDao:
    def get_conn(self):
        if isdir("resources") is False:
            raise FileExistsError("A resources nevű mappa nem létezik!")

        return connect(Path("resources/hungarian_texts.db"))

    def get_min_page_number_book(self, writer):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT title, MIN(page_number) FROM books WHERE writer = ? AND filename != ?", (writer, f"{writer}_osszes_muve"))

        title = ""
        page_num = 0
        for row in cursor.fetchall():
            title = row[0]
            page_num = int(row[1])

        cursor.close()
        conn.close()
        return title, page_num

    def get_max_page_number_book(self, writer):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT title, MAX(page_number) FROM books WHERE writer = ? AND filename != ?", (writer, f"{writer}_osszes_muve"))

        title = ""
        page_num = 0
        for row in cursor.fetchall():
            title = row[0]
            page_num = int(row[1])

        cursor.close()
        conn.close()
        return title, page_num

    def get_all_book_titles(self, writer):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM books WHERE writer = ?", (writer,))

        writer_name = "Jókai Mór"
        if writer == "moricz":
            writer_name = "Moricz Zsigmond"

        titles = list()

        for row in cursor.fetchall():
            if len(row[0]) > 1:
                titles.append(f"{writer_name}: {row[0]}")

        titles.sort()

        cursor.close()
        conn.close()
        return titles

    def get_page_number(self, writer, filename):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT page_number FROM books WHERE writer = ? AND filename = ?", (writer, filename))

        page_number = int(cursor.fetchone()[0])

        cursor.close()
        conn.close()
        return page_number

    def get_all_book_page_numbers(self, writer):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT page_number FROM books WHERE writer = ? AND filename != ?", (writer, f"{writer}_osszes_muve"))

        page_number = list()

        for row in cursor.fetchall():
            page_number.append(int(row[0]))

        cursor.close()
        conn.close()
        return page_number

    def get_one_book_by_title(self, writer, title):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE writer = ? AND title = ?", (writer, title,))

        entity = None

        for row in cursor.fetchall():
            entity = BookEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

        cursor.close()
        conn.close()
        return entity

    def get_most_frequent_words_from_book(self, writer, filename, count):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM books WHERE writer = ? AND filename = ?", (writer, filename))

        counted = None

        for row in cursor.fetchall():
            counted = Counter(row[0].split(" ")).most_common(count)

        cursor.close()
        conn.close()
        return counted

    def create_book(self, writer, filename, content, page_number):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (writer, filename, content, page_number) VALUES (?, ?, ?, ?)", (writer, filename, content, page_number,))
        conn.commit()

        entity = BookEntity(cursor.lastrowid, writer, filename, content, page_number=page_number)

        cursor.close()
        conn.close()

        return entity
