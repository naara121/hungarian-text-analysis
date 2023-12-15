from collections import defaultdict
from operator import itemgetter
from os import path, listdir, system, remove
from os.path import isdir
from pathlib import Path, PurePath
from re import sub

import fitz
from gensim.utils import simple_preprocess
from nltk import sent_tokenize
from nltk.corpus import stopwords
from simplemma import lemmatize

from controller.book_controller import BookController
from controller.magyarlanc_controller import MagyarlancController
from utils.logger import Logger
from utils.resource_downloader import download_magyarlanc, download_pdfs
from utils.sqlite_runner import create_tables, update_title_in_books, update_themes_in_books, delete_all_data


class TextProcessor:
    def __init__(self):
        self._book_controller = BookController()
        self._magyarlanc_controller = MagyarlancController()
        self._logger = Logger()

    def text_processor(self, writer):
        if isdir("resources") is False:
            download_pdfs()

        if isdir(Path("resources/books")) is False:
            download_pdfs()

        book_dir = Path(f"resources/books/{writer}")

        # Contains the full path of all pdf files in the given writer's directory
        files = [path.join(book_dir, file) for file in listdir(book_dir)
                 if path.exists(path.join(book_dir, file)) and file.endswith(".pdf")]

        file_counter = 0
        preprocessed_all_texts = ""
        all_page_num = 0

        self._logger.log("INFO", "A művek feldolgozása elkezdődött.")

        unnecessary_words = ["révai", "arcanum", "franklin-társulat", "tartalom", "athenaeum", "elektronikus", "isbn",
                             "tartalomjegyzék", "fejezet", "huszadik beszélgetés", "epizód"]

        for file in files:
            text = ""
            doc = fitz.open(file)

            filename = PurePath(file).parts[-1].replace(".pdf", "")

            for page in doc:
                if page.number <= 4:
                    if any(substring in page.get_text().lower() for substring in unnecessary_words):
                        continue

                text += page.get_text()

            magyarlanc_text = self.preprocess_magyarlanc_text(text)
            preprocessed_text = self.preprocess_text(magyarlanc_text)
            preprocessed_all_texts += preprocessed_text
            all_page_num += doc.page_count

            self._logger.log("INFO", "A művek feldolgozása befejeződött.")
            self._book_controller.create_book(
                writer,
                filename,
                preprocessed_text,  # saves the lemmatized text
                doc.page_count
            )
            file_counter += 1
            self._logger.log("INFO", f"{len(files)} fájlból {file_counter} kész.")

            self.create_magyarlanc_analysis(writer, filename, magyarlanc_text, "depparse")

        self._logger.log("INFO", "Következik az adott író összes művének feldolgozása egyben.")

        self._book_controller.create_book(
            writer,
            f"{writer}_osszes_muve",
            preprocessed_all_texts,
            all_page_num
        )
        self._logger.log("INFO", "Elkészült az összes mű feldolgozása.")

        self.create_magyarlanc_analysis(writer, f"{writer}_osszes_muve", "", "depparse")

    def preprocess_magyarlanc_text(self, text):
        text = (text
                .replace("˝u", "ű").replace("˝U", "Ű").replace("˝o", "ő").replace("˝O", "Ő")
                .replace("-\n", "").replace(".oOo.", "").replace("\n-", "\n").replace("»", "").replace("«", "")
                )

        text = sub(r"\s{2,}", " ", text)
        text = sub(r"\\.{2,}", ".", text)
        text = sub(r"[\s\n]{2,}[^a-zA-Z0-9.,?!-:;]", "\n", text)
        text = sub(r"–", "", text)
        text = sub(r"[_\s]{2,}[^a-zA-Z0-9]", "", text)
        text = sub(r"[—\s]{2,}[^a-zA-Z0-9]", "", text)
        text = sub(r"\n[0-9]+\n", "\n", text)
        text = sub(r"\n[0-9]+\s", "\n", text)
        text = sub(r"\n[0-9]+.", "\n", text)
        text = sub(r"\n[a-zA-Z\\. FEJEZET]+\n", "\n", text)
        text = sub(r"\n[a-zA-Z\\. Fejezet]+\n", "\n", text)
        text = sub(r"\n[a-zA-Z\\. fejezet]+\n", "\n", text)
        text = sub(r"[\\.]{3}(?=\s[A-Z])", ".", text)
        text = sub(r"[\\.]{3}(?=\s[a-z0-9])", "", text)
        text = sub(r"[\\.]{3}(?=\s[ÖÜÓŐÚŰÁÉ])", ".", text)
        text = sub(r"[\\.]{3}(?=\s[öüóőúéáű])", "", text)
        text = sub(r"[\\.]{3}(?=[A-Z])", ". ", text)
        text = sub(r"[\\.]{3}(?=[a-z0-9])", " ", text)
        text = sub(r"[\\.]{3}(?=[ÖÜÓŐÚŰÁÉ])", ". ", text)
        text = sub(r"[\\.]{3}(?=[öüóőúéáű])", " ", text)
        text = sub(r"\s-\s", " ", text)

        return text

    def preprocess_text(self, text):
        plus_stopwords = ["én", "te", "ő", "mi" "ti", "ők", "is", "ha"] + stopwords.words("hungarian")

        puncts = ["!", "#", "$", "%", "&", "'", "(", ")", "*", "+", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@",
                  "[", ']', "^", "_", "`", '{', '|', '}', '~', '"']

        for punct in puncts:
            text = text.replace(punct, "")

        lemmatized = list(map(lambda token: lemmatize(token, lang="hu"), simple_preprocess(text)))

        filtered_text = list(filter(lambda token: len(token) > 1 and token not in plus_stopwords, lemmatized))

        return " ".join(filtered_text).lower()

    def create_magyarlanc_analysis(self, writer, filename, text, mode):
        if isdir("resources") is False:
            raise FileExistsError("A resources nevű mappa nem létezik!")

        if filename == f"{writer}_osszes_muve":
            all_content = ""
            all_pos = defaultdict(int)
            all_words = ""
            all_outs = self._magyarlanc_controller.get_all_magyarlanc_outs(writer)

            for out in all_outs:
                all_content += out.content

                for key, value in out.sorted_pos.items():
                    all_pos[key] += value

                all_words += out.all_words

            sorted_pos = dict(sorted(all_pos.items(), key=itemgetter(1), reverse=True))

            self._magyarlanc_controller.create_magyarlanc_entity(writer, f"{writer}_osszes_muve", all_content, str(sorted_pos), all_words)
            return

        processed = Path(f"resources/magyarlanc/{filename}_processed.docx")
        out = Path(f"resources/magyarlanc/{filename}_magyarlanc_out.docx")
        magyarlanc = Path("resources/magyarlanc")

        if isdir(magyarlanc) is False:
            download_magyarlanc()

        if "magyarlanc-3.0.jar" not in listdir(magyarlanc):
            download_magyarlanc()

        sent_text = "\n".join(sent_tokenize(text))

        with open(processed, "w") as doc_writer:
            doc_writer.write(sent_text)

        self._logger.log("INFO", "A magyarlanccal való elemzés elkezdődött.")

        system(
            f"java -Xmx2G -jar {Path(magyarlanc) / 'magyarlanc-3.0.jar'} -mode {mode} -input {processed} -output {out}"
        )

        remove(processed)

        self._logger.log("INFO", "Az elemzés adatbázisba való mentése elkezdődött.")

        with open(out, "r") as doc_reader:
            doc = doc_reader.read()
            pos_list = {"NOUN": "Főnév", "VERB": "Ige", "ADJ": "Melléknév", "ADV": "Határozószó", "PRON": "Névmás",
                        "PROPN": "Tulajdonnév", "NUM": "Számnév", "ADP": "Elöljáró és névutó",
                        "SCONJ": "Alárendelő kötőszó",
                        "CONJ": "Kötőszó", "INTJ": "Indulatszó", "AUX": "Segédige", "X": "Egyéb",
                        "PUNCT": "Központozás",
                        "SYM": "Szimbólum", "DET": "Determináns", "PART": "Partikula"}

            for pos, hu_pos in pos_list.items():
                doc = sub(fr"\t{pos}\t(?=[^\n])", f"\t{hu_pos}\t", doc)

            pos_dict = defaultdict(int)

            doc_split = doc.split("\n")
            for line in doc_split:
                if len(line) <= 1:
                    continue

                split_line = line.split("\t")
                pos_dict[split_line[3]] += 1

            if pos_dict.get("") is not None:
                pos_dict.pop("")

            sorted_pos = dict(sorted(pos_dict.items(), key=itemgetter(1), reverse=True))

            self._magyarlanc_controller.create_magyarlanc_entity(writer, filename, doc, str(sorted_pos), sent_text)

        self._logger.log("INFO", "Az adatbázisba való mentés befejeződött.")

        remove(out)

    def processing(self):
        self._logger.log("INFO", "Az adatbázis előkészítése megkezdődött. Ne álltsa le a programot!")
        self._logger.log("INFO", "Amint befejeződik az adatok mentése, elindul az alkalmazás!")

        try:
            create_tables()
            delete_all_data()
            self.text_processor("jokai")
            self.text_processor("moricz")
            update_title_in_books()
            update_themes_in_books()
            return True
        except FileNotFoundError:
            self._logger.log("INFO", "Hiba történt!")
            return False
