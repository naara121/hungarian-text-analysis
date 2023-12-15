class BookEntity:
    def __init__(self, book_id, writer, filename, content, title="", themes="", page_number=0):
        self.book_id = book_id
        self.writer = writer
        self.filename = filename
        self.content = content
        self.title = title
        self.themes = themes
        self.page_number = page_number

    @property
    def book_id(self):
        return self._book_id

    @property
    def writer(self):
        return self._writer

    @property
    def filename(self):
        return self._filename

    @property
    def content(self):
        return self._content

    @property
    def title(self):
        return self._title

    @property
    def themes(self):
        return self._themes

    @property
    def page_number(self):
        return self._page_number

    @book_id.setter
    def book_id(self, book_id):
        if not isinstance(book_id, int):
            raise ValueError("Az id formátuma nem megfelelő!")
        self._book_id = book_id

    @writer.setter
    def writer(self, writer):
        if not isinstance(writer, str):
            raise ValueError("Az író formátuma nem megfelelő!")
        self._writer = writer

    @filename.setter
    def filename(self, filename):
        if not isinstance(filename, str):
            raise ValueError("A fájl nevének formátuma nem megfelelő!")
        self._filename = filename

    @content.setter
    def content(self, content):
        if not isinstance(content, str):
            raise ValueError("A szöveg formátuma nem megfelelő!")
        self._content = content

    @title.setter
    def title(self, title):
        if title is None:
            self._title = ""
        else:
            if not isinstance(title, str):
                raise ValueError("A cím formátuma nem megfelelő!")
            self._title = title

    @themes.setter
    def themes(self, themes):
        if themes is None:
            self._themes = ""
        else:
            if not isinstance(themes, str):
                raise ValueError("A témák formátuma nem megfelelő!")
            self._themes = themes

    @page_number.setter
    def page_number(self, page_number):
        if page_number is None:
            self._page_number = 0
        else:
            if not isinstance(page_number, int):
                raise ValueError("Az oldalszám formátuma nem megfelelő!")
            self._page_number = page_number
