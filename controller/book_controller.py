from scipy.stats import spearmanr, kendalltau, pearsonr
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from dao.book_dao import BookDao


class BookController:
    def __init__(self):
        self._dao = BookDao()

    def get_page_number(self, writer, filename):
        return self._dao.get_page_number(writer, filename)

    def get_min_page_number_book(self, writer):
        return self._dao.get_min_page_number_book(writer)

    def get_max_page_number_book(self, writer):
        return self._dao.get_max_page_number_book(writer)

    def get_all_book_titles(self, writer):
        return self._dao.get_all_book_titles(writer)

    def get_all_book_page_numbers(self, writer):
        return self._dao.get_all_book_page_numbers(writer)

    def get_one_book_by_title(self, writer, title):
        return self._dao.get_one_book_by_title(writer, title)

    def get_most_frequent_words_from_book(self, writer, filename, count):
        frequent = self._dao.get_most_frequent_words_from_book(writer, filename, count)

        return dict(frequent)

    def create_book(self, writer, filename, content, page_number):
        return self._dao.create_book(writer, filename, content, page_number)

    def get_labeled_words(self, book_1, book_2, count):
        le = preprocessing.LabelEncoder()

        words_1 = list(self.get_most_frequent_words_from_book(book_1.writer, book_1.filename, count).keys())
        words_2 = list(self.get_most_frequent_words_from_book(book_2.writer, book_2.filename, count).keys())

        le.fit(list(set(words_1 + words_2)))

        labels_1 = le.transform(words_1)
        labels_2 = le.transform(words_2)

        return labels_1.tolist(), labels_2.tolist()

    def get_spearman_correlation(self, labels_1, labels_2):
        return spearmanr(labels_1, labels_2)

    def get_kendall_correlation(self, labels_1, labels_2):
        return kendalltau(labels_1, labels_2)

    def get_pearsonr_correlation(self, labels_1, labels_2):
        return pearsonr(labels_1, labels_2)

    def get_cosine_similarity(self, book_1, book_2):
        cv = CountVectorizer()

        sparse_matrix = cv.fit_transform([book_1.content, book_2.content])
        doc_term_matrix = sparse_matrix.todense()

        return cosine_similarity(sparse_matrix)[0][1]

    def get_jaccard_similarity(self, content_1, content_2):
        set_1 = set(content_1.split(" "))
        set_2 = set(content_2.split(" "))

        intersection = len(set_1.intersection(set_2))

        union = len(set_1.union(set_2))

        return intersection / union
