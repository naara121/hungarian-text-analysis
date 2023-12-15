**Alkalmazás alapvető szükségletei:**
- Minimum Python 3.8
- Minimum Java 8 (ha az adatbázis újboli kiíépítése szükséges)
- Sükségünk lesz a megfelelő könyvtárakra, ezt egyszerűen le tudjuk tölteni a `requirements.txt` segítségével. Ehhez szükség lesz a `pip`-re és a következő paranccsal egyszerűen megoldható: 
	- `pip install -r requirements.txt` 
- A következő lépés az nltk-hoz tartozó letöltések amik:
	- `python -m nltk.downloader stopwords`
	- `python -m nltk.downloader punkt`
	**Megjegyzés:** Bizonyos rendszereken lehet nem elég a `python`, kellhet például, hogy `python3` 

Ezután már elindítható az alkalmazás a terminálból a `python main.py` vagy `python3 main.py` segítségével.

Miután elindult létrehozott pár mappát számunkra amik szükségesek lesznek. Ilyen a `resources` és azon belül található a `books`, amibe a könyvek szerepelhetnek, és a `magyarlanc`, ahol a magyarlanc jar fájl szerepelhet. Ezekre csak akkor van szükség, ha újra fel akarjuk építeni az adatbázist, de ez nem szükséges.

Ami számunkra fontos, hogy a `resources` mappán belül kell elhelyezni a már elkészült adatbázist, aminek a neve `hungarian_texts.db`. A `resources` mappában az alkalmazás elindulásakor már létrehoz oda egy üres adatbázist és ezt egyszerűen csak ki kell kicserélni az adatokat tartalmazóra.

Miután ez sikerült, a program teljes mértékben működik és használható, megtekinthető.

Linux és Windows operációs rendszeren is működik az alkalmazás, azonban Windows-on bizonyos rendszereknél lehetséges, hogy a saját adatbázis kiépítése nem működik, viszont ez nem is szükséges, hiszen elérhető számunka az adatbázis (maga a program is ugyan ezt csinálná meg újra, szóval nem is lényeges).

Ha valamilyen okból el akarnánk mégis végezni, akkor az alkalmazás legelső oldalán található a `Művek letöltése` gomb, majd az `Adatbázis elkészítése` gomb és ezek segítségével automatikusan elvégezhető.

**Figyelem** az adatbázis létrehozása sok időt, több órát vesz igénybe, a magyarlanc elemzése miatt!
