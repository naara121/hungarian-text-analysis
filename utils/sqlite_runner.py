from os import mkdir
from os.path import isdir
from pathlib import Path
from sqlite3 import connect

from utils.logger import Logger

logger = Logger()


def create_tables():
    if isdir("resources") is False:
        mkdir("resources")

    if isdir(Path("resources/books")) is False:
        mkdir(Path("resources/books"))

    if isdir(Path("resources/magyarlanc")) is False:
        mkdir(Path("resources/magyarlanc"))

    conn = connect(Path("resources/hungarian_texts.db"))
    cursor = conn.cursor()

    cursor.execute('''
              CREATE TABLE IF NOT EXISTS books(
              book_id INTEGER PRIMARY KEY AUTOINCREMENT,
              writer TEXT NOT NULL,
              filename TEXT UNIQUE NOT NULL,
              content TEXT NOT NULL,
              title TEXT,
              themes TEXT,
              page_number INTEGER
              )
              ''')

    cursor.execute('''
              CREATE TABLE IF NOT EXISTS magyarlanc(
              work_id INTEGER PRIMARY KEY AUTOINCREMENT,
              writer TEXT NOT NULL,
              filename TEXT UNIQUE NOT NULL,
              content TEXT NOT NULL,
              sorted_pos TEXT NOT NULL,
              all_words TEXT NOT NULL,
              FOREIGN KEY(filename) REFERENCES books(filename) ON DELETE CASCADE
              )
              ''')

    conn.commit()
    cursor.close()
    conn.close()


def check_tables():
    conn = connect(Path("resources/hungarian_texts.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(book_id) FROM books")
    tables = list()
    tables.append(cursor.fetchone())
    cursor.execute("SELECT COUNT(work_id) FROM magyarlanc")
    tables.append(cursor.fetchone())
    cursor.close()
    conn.close()
    return tables


def delete_all_data():
    conn = connect(Path("resources/hungarian_texts.db"))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books")
    cursor.execute("DELETE FROM magyarlanc")
    conn.commit()
    cursor.close()
    conn.close()


def update_title_in_books():
    conn = connect(Path("resources/hungarian_texts.db"))
    cursor = conn.cursor()

    update_sql = "UPDATE books SET title = ? WHERE writer = ? AND filename = ?"

    logger.log("INFO", "Jókai Mór könyveihez tartozó adatok beszúrása.")

    cursor.execute(update_sql, ("1848", "jokai", "1848"))
    cursor.execute(update_sql, ("A baratfalvi lévita", "jokai", "a_baratfalvi_levita"))
    cursor.execute(update_sql, ("A bűntárs", "jokai", "a_buntars"))
    cursor.execute(update_sql, ("Ahol a pénz nem isten", "jokai", "ahol_a_penz_nem_isten"))
    cursor.execute(update_sql, ("A huszti beteglátogatók", "jokai", "a_huszti_beteglatogatok"))
    cursor.execute(update_sql, ("Aki a szívet a homlokán hordja", "jokai", "aki_a_szivet_a_homlokan_hordja"))
    cursor.execute(update_sql, ("A kőszívű ember fiai", "jokai", "a_koszivu_ember_fiai"))
    cursor.execute(update_sql, ("A Káró", "jokai", "a_krao"))
    cursor.execute(update_sql, ("Árnyképek", "jokai", "arnykepek"))
    cursor.execute(update_sql, ("A serfőző", "jokai", "a_serfozo"))
    cursor.execute(update_sql, ("Sikrő-album", "jokai", "sirko_album"))
    cursor.execute(update_sql, ("A szabadságharc hősei", "jokai", "a_szabadsagharc_hosie"))
    cursor.execute(update_sql, ("Az arany ember", "jokai", "az_arany_ember"))
    cursor.execute(update_sql, ("Az én kortársaim", "jokai", "az_en_kortarsaim"))
    cursor.execute(update_sql, ("Börtön virága", "jokai", "borton_viraga"))
    cursor.execute(update_sql, ("Egy asszonyi hajszál", "jokai", "egy_asszonyi_hajszal"))
    cursor.execute(update_sql, ("Az egyhuszasos leány", "jokai", "az_egyhuszasos_leany"))
    cursor.execute(update_sql, ("Az egyiptusi rózsa", "jokai", "az_egyiptusi_rozsa"))
    cursor.execute(update_sql, ("Fekete gyémántok", "jokai", "fekete_gyemantok"))
    cursor.execute(update_sql, ("Fráter György", "jokai", "frater_gyorgy"))
    cursor.execute(update_sql, ("Kárpáthy Zoltán", "jokai", "karpathy_zoltan"))
    cursor.execute(update_sql, ("Kertészgazdászati jegyzetek", "jokai", "kerteszgazdaszati_jegyzetek"))
    cursor.execute(update_sql, ("Két menyegző", "jokai", "ket_menyegzo"))
    cursor.execute(update_sql, ("A kétszarvű ember", "jokai", "a_ketszarvu_ember"))
    cursor.execute(update_sql, ("Lenczi fráter", "jokai", "lenczi_frater"))
    cursor.execute(update_sql, ("Levente", "jokai", "levente"))
    cursor.execute(update_sql, ("A lőcsei fehér asszony", "jokai", "a_locsei_feher_asszony"))
    cursor.execute(update_sql, ("A Magláy-család", "jokai", "a_maglay_csalad"))
    cursor.execute(update_sql, ("Magnéta", "jokai", "magneta"))
    cursor.execute(update_sql, ("Magyarhon szépségei, Legvitézebb huszár", "jokai", "magyarhon_szepsegei"))
    cursor.execute(update_sql, ("Milyenek a férfiak? Milyenek a nők?", "jokai", "milyenek_a_ferfiak_nok"))
    cursor.execute(update_sql, ("Névtelen vár", "jokai", "nevtelen_var"))
    cursor.execute(update_sql, ("Oroszlánhűség", "jokai", "oroszlanhuseg"))
    cursor.execute(update_sql, ("Őszi fény", "jokai", "oszi_feny"))
    cursor.execute(update_sql, ("Páter Péter", "jokai", "pater_peter"))
    cursor.execute(update_sql, ("Politikai divatok", "jokai", "politikai_divatok"))
    cursor.execute(update_sql, ("Regék", "jokai", "regek"))
    cursor.execute(update_sql, ("Szélcsend alatt", "jokai", "szelcsend_alatt"))
    cursor.execute(update_sql, ("Tégy jót", "jokai", "tegy_jot"))
    cursor.execute(update_sql, ("Úti rajzok", "jokai", "uti_rajzok"))
    cursor.execute(update_sql, ("Van még új a nap alatt", "jokai", "van_meg_uj_a_nap_alatt"))
    cursor.execute(update_sql, ("", "jokai", "jokai_osszes_muve"))

    logger.log("INFO", "Móricz Zsigmond könyveihez tartozó adatok beszúrása.")

    cursor.execute(update_sql, ("A boldog ember", "moricz", "a_boldog_ember"))
    cursor.execute(update_sql, ("A fáklya", "moricz", "a_faklya"))
    cursor.execute(update_sql, ("A galamb papné", "moricz", "a_galamb_papné"))
    cursor.execute(update_sql, ("A nagy fejedelem", "moricz", "a_nagy_fejedelem"))
    cursor.execute(update_sql, ("A nap árnyéka", "moricz", "a_nap_arnyeka"))
    cursor.execute(update_sql, ("Arany szoknyák", "moricz", "arany_szoknyak"))
    cursor.execute(update_sql, ("Árvácska", "moricz", "arvacska"))
    cursor.execute(update_sql, ("Az asszony beleszól", "moricz", "az_asszony_beleszol"))
    cursor.execute(update_sql, ("Az isten háta mögött", "moricz", "az_isten_hata_mogott"))
    cursor.execute(update_sql, ("Bál", "moricz", "bal"))
    cursor.execute(update_sql, ("Baleset", "moricz", "baleset"))
    cursor.execute(update_sql, ("Betyár", "moricz", "betyar"))
    cursor.execute(update_sql, ("Boldog világ", "moricz", "boldog_vilag"))
    cursor.execute(update_sql, ("Csibe", "moricz", "csibe"))
    cursor.execute(update_sql, ("Életem regénye", "moricz", "eletem_regenye"))
    cursor.execute(update_sql, ("Esőleső társaság", "moricz", "esoleso_tarsasag"))
    cursor.execute(update_sql, ("Forr a bor", "moricz", "forr_a_bor"))
    cursor.execute(update_sql, ("Forró mezők", "moricz", "forro_mezok"))
    cursor.execute(update_sql, ("Fortunátus", "moricz", "fortunatus"))
    cursor.execute(update_sql, ("Harmatos rózsa", "moricz", "harmatos_rozsa"))
    cursor.execute(update_sql, ("Házasságtörés", "moricz", "hazassagtores"))
    cursor.execute(update_sql, ("Jobb mint otthon", "moricz", "jobb_mint_otthon"))
    cursor.execute(update_sql, ("Jószerencsét", "moricz", "joszerencset"))
    cursor.execute(update_sql, ("Kerek Ferkó", "moricz", "kerek_ferko"))
    cursor.execute(update_sql, ("Kivilágos kivirradtig", "moricz", "kivilagos_kivirradtig"))
    cursor.execute(update_sql, ("Komor ló", "moricz", "komor_lo"))
    cursor.execute(update_sql, ("Légy jó mindhalálig", "moricz", "legy_jo_mindhalalig"))
    cursor.execute(update_sql, ("Mese a zöld füvön", "moricz", "mese_a_zold_fuvon"))
    cursor.execute(update_sql, ("Nem élhetek muzsikaszó nélkül", "moricz", "nem_elhetek_muzsikaszo_nelkul"))
    cursor.execute(update_sql, ("Pillangó", "moricz", "pillango"))
    cursor.execute(update_sql, ("Pipacsok a tengeren", "moricz", "pipacsok_a_tengeren"))
    cursor.execute(update_sql, ("Rab oroszlán", "moricz", "rab_oroszlan"))
    cursor.execute(update_sql, ("Rokonok", "moricz", "rokonok"))
    cursor.execute(update_sql, ("Rózsa Sándor a lovát ugratja", "moricz", "rozsa_sandor_a_lovat_ugratja"))
    cursor.execute(update_sql, ("Rózsa Sándor összevonja a szemöldökét", "moricz", "rozsa_sandor_osszevonja_a_szemoldoket"))
    cursor.execute(update_sql, ("Sárarany", "moricz", "sararany"))
    cursor.execute(update_sql, ("A szerelmes levél", "moricz", "a_szerelmes_level"))
    cursor.execute(update_sql, ("Tündérkert", "moricz", "tunderkert"))
    cursor.execute(update_sql, ("Úri muri", "moricz", "uri_muri"))
    cursor.execute(update_sql, ("Válogatott elbeszélések", "moricz", "valogatott_elbeszelesek"))
    cursor.execute(update_sql, ("", "moricz", "moricz_osszes_muve"))

    conn.commit()

    cursor.close()
    conn.close()


def update_themes_in_books():
    conn = connect(Path("resources/hungarian_texts.db"))
    cursor = conn.cursor()

    update_sql = "UPDATE books SET themes = ? WHERE writer = ? AND filename = ?"

    logger.log("INFO", "Jókai Mór könyveihez tartozó témák beszúrása.")

    cursor.execute(update_sql, (
    "klasszikus magyar irodalom, hadtörténet, magyar történelem 1791-1867, 1848/49-es forradalom és szabadságharc, 19. sz.",
    "jokai", "1848"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "a_baratfalvi_levita"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "a_buntars"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "ahol_a_penz_nem_isten"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "a_huszti_beteglatogatok"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "aki_a_szivet_a_homlokan_hordja"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "a_koszivu_ember_fiai"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "a_krao"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "arnykepek"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "jokai", "a_serfozo"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "sirko_album"))
    cursor.execute(update_sql, (
    "klasszikus magyar irodalom, hadtörténet, Magyar történelem 1791-1867, 1848/49-es forradalom és szabadságharc, hősiesség, 19. sz.",
    "jokai", "a_szabadsagharc_hosie"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "jokai", "az_arany_ember"))
    cursor.execute(update_sql, (
    "klasszikus magyar irodalom, 1848/49-es forradalom és szabadságharc, 19-20. sz.", "jokai", "az_en_kortarsaim"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "borton_viraga"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "egy_asszonyi_hajszal"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "az_egyhuszasos_leany"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "az_egyiptusi_rozsa"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "fekete_gyemantok"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "frater_gyorgy"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "karpathy_zoltan"))
    cursor.execute(update_sql, (
    "növénytermesztés, kertészet, kertészkedés, szőlőtermesztés, gyümölcstermesztés, növényvédelem, talajművelés, kártevőirtás",
    "jokai", "kerteszgazdaszati_jegyzetek"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "ket_menyegzo"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "a_ketszarvu_ember"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "lenczi_frater"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, verses dráma, 19-20. sz.", "jokai", "levente"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "a_locsei_feher_asszony"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "a_maglay_csalad"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "magneta"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "magyarhon_szepsegei"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "jokai", "milyenek_a_ferfiak_nok"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "nevtelen_var"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "oroszlanhuseg"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "oszi_feny"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "jokai", "pater_peter"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "politikai_divatok"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "jokai", "regek"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "szelcsend_alatt"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19. sz.", "jokai", "tegy_jot"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, útirajz, Olaszország , 19-20. sz.", "jokai", "uti_rajzok"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "jokai", "van_meg_uj_a_nap_alatt"))

    logger.log("INFO", "Móricz Zsigmond könyveihez tartozó témák beszúrása.")

    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "a_boldog_ember"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "a_faklya"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "a_galamb_papné"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "a_nagy_fejedelem"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "a_nap_arnyeka"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 20. sz.", "moricz", "arany_szoknyak"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "arvacska"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "az_asszony_beleszol"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "az_isten_hata_mogott"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 20. sz.", "moricz", "bal"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "baleset"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "betyar"))
    cursor.execute(update_sql, (
    "klasszikus magyar irodalom, gyermek- és ifjúsági irodalom, állatmese, 19-20. sz.", "moricz", "boldog_vilag"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 20. sz.", "moricz", "csibe"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "eletem_regenye"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "esoleso_tarsasag"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "forr_a_bor"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "forro_mezok"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 20. sz.", "moricz", "fortunatus"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "harmatos_rozsa"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "hazassagtores"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "jobb_mint_otthon"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "joszerencset"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "kerek_ferko"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "kivilagos_kivirradtig"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "komor_lo"))
    cursor.execute(update_sql, (
    "klasszikus magyar irodalom, gyermek- és ifjúsági irodalom, ifjúsági regény, 19-20. sz.", "moricz",
    "legy_jo_mindhalalig"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "mese_a_zold_fuvon"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "nem_elhetek_muzsikaszo_nelkul"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "pillango"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "pipacsok_a_tengeren"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "rab_oroszlan"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "rokonok"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "rozsa_sandor_a_lovat_ugratja"))
    cursor.execute(update_sql,
                   ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "rozsa_sandor_osszevonja_a_szemoldoket"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "sararany"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "a_szerelmes_level"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "tunderkert"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "uri_muri"))
    cursor.execute(update_sql, ("klasszikus magyar irodalom, 19-20. sz.", "moricz", "valogatott_elbeszelesek"))

    conn.commit()

    cursor.close()
    conn.close()
