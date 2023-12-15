from os.path import isdir
from pathlib import Path
from sqlite3 import connect

from model.magyarlanc_entity import MagyarlancEntity


class MagyarlancDao:
    def get_conn(self):
        if isdir("resources") is False:
            raise FileExistsError("A resources nevű mappa nem létezik!")

        return connect(Path("resources/hungarian_texts.db"))

    def get_all_magyarlanc_outs(self, writer):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magyarlanc WHERE writer = ?", (writer,))

        outs = list()

        for row in cursor.fetchall():
            outs.append(MagyarlancEntity(row[0], row[1], row[2], row[3], row[4], row[5]))

        cursor.close()
        conn.close()
        return outs

    def get_magyaralanc_out(self, writer, filename):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magyarlanc WHERE writer = ? AND filename = ?", (writer, filename))

        out = None

        for row in cursor.fetchall():
            out = MagyarlancEntity(row[0], row[1], row[2], row[3], row[4], row[5])

        cursor.close()
        conn.close()
        return out

    def create_magyarlanc_entity(self, writer, filename, content, sorted_pos, all_words):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magyarlanc (writer, filename, content, sorted_pos, all_words) VALUES (?, ?, ?, ?, ?)", (writer, filename, content, sorted_pos, all_words,))
        conn.commit()

        entity = MagyarlancEntity(cursor.lastrowid, writer, filename, content, sorted_pos, all_words)

        cursor.close()
        conn.close()
        return entity
