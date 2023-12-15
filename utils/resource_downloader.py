from os import mkdir, listdir, remove
from os.path import isdir
from pathlib import Path
from shutil import copyfileobj
from urllib.request import urlopen

from requests import get

from utils.logger import Logger


def download_pdfs():
    jokai_works = {
        "1848": "https://mek.oszk.hu/18700/18755/pdf/18755.pdf",
        "a_baratfalvi_levita": "https://mek.oszk.hu/00700/00785/00785.pdf",
        "a_buntars": "https://mek.oszk.hu/11500/11589/pdf/11589.pdf",
        "ahol_a_penz_nem_isten": "https://mek.oszk.hu/00700/00778/00778.pdf",
        "a_huszti_beteglatogatok": "https://mek.oszk.hu/07300/07315/07315.pdf",
        "aki_a_szivet_a_homlokan_hordja": "https://mek.oszk.hu/00800/00811/00811.pdf",
        "a_koszivu_ember_fiai": "https://mek.oszk.hu/00600/00695/00695.pdf",
        "a_krao": "https://mek.oszk.hu/18000/18047/pdf/18047.pdf",
        "arnykepek": "https://mek.oszk.hu/07300/07324/07324.pdf",
        "a_serfozo": "https://mek.oszk.hu/11500/11513/pdf/11513.pdf",
        "sirko_album": "https://mek.oszk.hu/00700/00700/00700.pdf",
        "a_szabadsagharc_hosie": "https://mek.oszk.hu/18700/18747/pdf/18747.pdf",
        "az_arany_ember": "https://mek.oszk.hu/00600/00688/00688.pdf",
        "az_en_kortarsaim": "https://mek.oszk.hu/18800/18835/pdf/18835.pdf",
        "borton_viraga": "https://mek.oszk.hu/08100/08117/08117.pdf",
        "egy_asszonyi_hajszal": "https://mek.oszk.hu/18500/18568/pdf/18568.pdf",
        "az_egyhuszasos_leany": "https://mek.oszk.hu/16300/16372/pdf/16372.pdf",
        "az_egyiptusi_rozsa": "https://mek.oszk.hu/16500/16559/16559.pdf",
        "fekete_gyemantok": "https://mek.oszk.hu/00600/00691/00691.pdf",
        "frater_gyorgy": "https://mek.oszk.hu/00800/00841/00841.pdf",
        "karpathy_zoltan": "https://mek.oszk.hu/00800/00828/00828.pdf",
        "kerteszgazdaszati_jegyzetek": "https://mek.oszk.hu/11500/11569/pdf/11569.pdf",
        "ket_menyegzo": "https://mek.oszk.hu/16100/16126/pdf/16126.pdf",
        "a_ketszarvu_ember": "https://mek.oszk.hu/02200/02204/02204.pdf",
        "lenczi_frater": "https://mek.oszk.hu/11600/11662/pdf/11662.pdf",
        "levente": "https://mek.oszk.hu/14500/14569/pdf/14569.pdf",
        "a_locsei_feher_asszony": "https://mek.oszk.hu/00600/00696/00696.pdf",
        "a_maglay_csalad": "https://mek.oszk.hu/11400/11437/pdf/11437.pdf",
        "magneta": "https://mek.oszk.hu/15700/15731/pdf/15731.pdf",
        "magyarhon_szepsegei": "https://mek.oszk.hu/09200/09290/pdf/09290.pdf",
        "milyenek_a_ferfiak_nok": "https://mek.oszk.hu/16400/16475/pdf/16475.pdf",
        "nevtelen_var": "https://mek.oszk.hu/00600/00697/00697.pdf",
        "oroszlanhuseg": "https://mek.oszk.hu/18900/18982/pdf/18982.pdf",
        "oszi_feny": "https://mek.oszk.hu/07300/07307/07307.pdf",
        "pater_peter": "https://mek.oszk.hu/16200/16276/pdf/16276.pdf",
        "politikai_divatok": "https://mek.oszk.hu/00600/00698/00698.pdf",
        "regek": "https://mek.oszk.hu/11500/11508/pdf/11508.pdf",
        "szelcsend_alatt": "https://mek.oszk.hu/07400/07451/pdf/07451.pdf",
        "tegy_jot": "https://mek.oszk.hu/00700/00702/00702.pdf",
        "uti_rajzok": "https://mek.oszk.hu/14400/14429/pdf/14429.pdf",
        "van_meg_uj_a_nap_alatt": "https://mek.oszk.hu/18300/18362/pdf/18362.pdf"
    }

    moricz_works = {
        "a_boldog_ember": "https://mek.oszk.hu/00900/00988/00988.pdf",
        "a_faklya": "https://mek.oszk.hu/01100/01171/01171.pdf",
        "a_galamb_papné": "https://mek.oszk.hu/05100/05170/05170.pdf",
        "a_nagy_fejedelem": "https://mek.oszk.hu/00900/00985/00985.pdf",
        "a_nap_arnyeka": "https://mek.oszk.hu/01200/01206/01206.pdf",
        "arany_szoknyak": "https://mek.oszk.hu/07000/07064/07064.pdf",
        "arvacska": "https://mek.oszk.hu/00900/00981/00981.pdf",
        "az_asszony_beleszol": "https://mek.oszk.hu/00900/00982/00982.pdf",
        "az_isten_hata_mogott": "https://mek.oszk.hu/01400/01435/01435.pdf",
        "bal": "https://mek.oszk.hu/11600/11629/pdf/11629.pdf",
        "baleset": "https://mek.oszk.hu/05700/05770/05770.pdf",
        "betyar": "https://mek.oszk.hu/00900/00987/00987.pdf",
        "boldog_vilag": "https://mek.oszk.hu/11400/11475/pdf/11475.pdf",
        "csibe": "https://mek.oszk.hu/21400/21468/pdf/21468.pdf",
        "eletem_regenye": "https://mek.oszk.hu/01200/01204/01204.pdf",
        "esoleso_tarsasag": "https://mek.oszk.hu/05600/05685/05685.pdf",
        "forr_a_bor": "https://mek.oszk.hu/05000/05093/05093.pdf",
        "forro_mezok": "https://mek.oszk.hu/01100/01175/01175.pdf",
        "fortunatus": "https://mek.oszk.hu/06800/06873/06873.pdf",
        "harmatos_rozsa": "https://mek.oszk.hu/05200/05261/05261.pdf",
        "hazassagtores": "https://mek.oszk.hu/06000/06043/06043.pdf",
        "jobb_mint_otthon": "https://mek.oszk.hu/01300/01333/01333.pdf",
        "joszerencset": "https://mek.oszk.hu/05300/05358/05358.pdf",
        "kerek_ferko": "https://mek.oszk.hu/05000/05074/05074.pdf",
        "kivilagos_kivirradtig": "https://mek.oszk.hu/00900/00990/00990.pdf",
        "komor_lo": "https://mek.oszk.hu/16700/16716/pdf/16716.pdf",
        "legy_jo_mindhalalig": "https://mek.oszk.hu/00900/00991/00991.pdf",
        "mese_a_zold_fuvon": "https://mek.oszk.hu/11200/11272/pdf/11272.pdf",
        "nem_elhetek_muzsikaszo_nelkul": "https://mek.oszk.hu/01500/01503/01503.pdf",
        "pillango": "https://mek.oszk.hu/04400/04417/04417.pdf",
        "pipacsok_a_tengeren": "https://mek.oszk.hu/01200/01203/01203.pdf",
        "rab_oroszlan": "https://mek.oszk.hu/01300/01334/01334.pdf",
        "rokonok": "https://mek.oszk.hu/01100/01150/01150.pdf",
        "rozsa_sandor_a_lovat_ugratja": "https://mek.oszk.hu/01500/01501/01501.pdf",
        "rozsa_sandor_osszevonja_a_szemoldoket": "https://mek.oszk.hu/01500/01546/01546.pdf",
        "sararany": "https://mek.oszk.hu/05000/05060/05060.pdf",
        "a_szerelmes_level": "https://mek.oszk.hu/01200/01281/01281.pdf",
        "tunderkert": "https://mek.oszk.hu/01100/01164/01164.pdf",
        "uri_muri": "https://mek.oszk.hu/01400/01431/01431.pdf",
        "valogatott_elbeszelesek": "https://mek.oszk.hu/01500/01502/01502.pdf"
    }

    if isdir("resources") is False:
        mkdir("resources")

    jokai_dir = Path("resources/books/jokai")
    moricz_dir = Path("resources/books/moricz")

    if isdir(Path("resources/books")):
        if isdir(jokai_dir):
            for file in listdir(jokai_dir):
                remove(Path(f"{jokai_dir}/{file}"))
        else:
            mkdir(jokai_dir)

        if isdir(moricz_dir):
            for file in listdir(moricz_dir):
                remove(Path(f"{moricz_dir}/{file}"))
        else:
            mkdir(moricz_dir)
    else:
        mkdir(Path("resources/books"))
        mkdir(jokai_dir)
        mkdir(moricz_dir)

    logger = Logger()

    for filename, url in jokai_works.items():
        response = get(url)

        work = Path(f"{jokai_dir}/{filename}.pdf")

        with open(work, "wb") as writer:
            writer.write(response.content)

        logger.log("INFO", f"{filename}.pdf elkészült.")

    for filename, url in moricz_works.items():
        response = get(url)

        work = Path(f"{moricz_dir}/{filename}.pdf")

        with open(work, "wb") as writer:
            writer.write(response.content)

        logger.log("INFO", f"{filename}.pdf elkészült.")

    if len(listdir(jokai_dir)) != 41:
        raise Exception("Jókai Mórnak nincs meg mind a 41 könyve!")

    if len(listdir(moricz_dir)) != 40:
        raise Exception("Móricz Zsigmondnak nincs meg mind a 40 könyve!")


def download_magyarlanc():
    if isdir("resources") is False:
        mkdir("resources")

    magyarlanc_dir = Path("resources/magyarlanc")

    if isdir(magyarlanc_dir) is False:
        mkdir(magyarlanc_dir)

    if "magyarlanc-3.0.jar" not in listdir(magyarlanc_dir):
        logger = Logger()
        logger.log("INFO", "A magyarlanc-3.0.jar fájl letöltése elkezdődött.")
        with urlopen("https://rgai.inf.u-szeged.hu/sites/rgai.inf.u-szeged.hu/files/magyarlanc-3.0.jar") as response, open(
                Path(f"{magyarlanc_dir}/magyarlanc-3.0.jar"), "wb") as out_file:
            copyfileobj(response, out_file)
            logger.log("INFO", "A fájl letöltése befejeződött.")
