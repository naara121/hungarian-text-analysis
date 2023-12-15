class MagyarlancEntity:
    def __init__(self, work_id, writer, filename, content, sorted_pos, all_words):
        self.work_id = work_id
        self.writer = writer
        self.filename = filename
        self.content = content
        self.sorted_pos = sorted_pos
        self.all_words = all_words

    @property
    def work_id(self):
        return self._work_id

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
    def sorted_pos(self):
        return self._sorted_pos

    @property
    def all_words(self):
        return self._all_words

    @work_id.setter
    def work_id(self, work_id):
        if not isinstance(work_id, int):
            raise ValueError("Az id formátuma nem megfelelő!")
        self._work_id = work_id

    @writer.setter
    def writer(self, writer):
        if not isinstance(writer, str):
            raise ValueError("Az író formátuma nem megfelelő!")
        self._writer = writer

    @filename.setter
    def filename(self, filename):
        if not isinstance(filename, str):
            raise ValueError("Az fájl név formátuma nem megfelelő!")
        self._filename = filename

    @content.setter
    def content(self, content):
        if not isinstance(content, str):
            raise ValueError("A szöveg formátuma nem megfelelő!")
        self._content = content

    @sorted_pos.setter
    def sorted_pos(self, sorted_pos):
        if not isinstance(sorted_pos, str):
            raise ValueError("A szöveg formátuma nem megfelelő!")
        self._sorted_pos = eval(sorted_pos)

    @all_words.setter
    def all_words(self, all_words):
        if not isinstance(all_words, str):
            raise ValueError("A szöveg formátuma nem megfelelő!")
        self._all_words = all_words
