from collections import defaultdict
from operator import itemgetter
from string import punctuation

from gensim.models import Word2Vec
from nltk.corpus import stopwords

from dao.magyarlanc_dao import MagyarlancDao


class MagyarlancController:
    def __init__(self):
        self._dao = MagyarlancDao()
        self._stopwords = stopwords.words("hungarian") + ["én", "te", "ő", "mi" "ti", "ők", "is", "ha"]

    def get_magyaralanc_out(self, writer, filename):
        return self._dao.get_magyaralanc_out(writer, filename)

    def get_all_magyarlanc_outs(self, writer):
        return self._dao.get_all_magyarlanc_outs(writer)

    def create_magyarlanc_entity(self, writer, filename, content, sorted_pos, all_words):
        return self._dao.create_magyarlanc_entity(writer, filename, content, sorted_pos, all_words)

    def get_top_pos(self, text, pos):
        batch_size = 100
        text_batches = [text[i:i + batch_size] for i in range(0, len(text), batch_size)]
        words = defaultdict(int)

        for batch in text_batches:
            for line in batch:
                if len(line) <= 0:
                    continue

                split = line.split("\t")
                if split[3] != pos:
                    continue

                if split[3] == "Tulajdonnév":
                    if split[1][0].isupper():
                        if split[1][-1] in punctuation:
                            continue
                            
                        words[split[1]] += 1
                else:
                    if split[1][0].islower():
                        words[split[1].lower()] += 1

        return words

    def get_word_similarity(self, queue, all_words):
        model = Word2Vec(
            sentences=list(map(lambda x: x.split(" "), all_words.split("\n"))),
            min_count=2,
            window=2,
            workers=2
        )

        queue.put(model)

        return None

    def get_grammatical_tenses(self, writer, filename):
        past_dict = defaultdict(int)
        pres_dict = defaultdict(int)

        result = self._dao.get_magyaralanc_out(writer, filename).content.split("\n")

        for _ in self.universal_feature_generator(result, past_dict, pres_dict, "Tense", ("Past", "Pres")):
            pass

        sorted_past_dict = dict(sorted(past_dict.items(), key=itemgetter(1), reverse=True))
        sorted_pres_dict = dict(sorted(pres_dict.items(), key=itemgetter(1), reverse=True))

        return {"Past": sorted_past_dict, "Pres": sorted_pres_dict}

    def get_pos_number(self, writer, filename):
        sing_dict = defaultdict(int)
        plur_dict = defaultdict(int)

        result = self._dao.get_magyaralanc_out(writer, filename).content.split("\n")

        for _ in self.universal_feature_generator(result, sing_dict, plur_dict, "Number", ("Sing", "Plur")):
            pass

        sorted_past_dict = dict(sorted(sing_dict.items(), key=itemgetter(1), reverse=True))
        sorted_pres_dict = dict(sorted(plur_dict.items(), key=itemgetter(1), reverse=True))

        return {"Sing": sorted_past_dict, "Plur": sorted_pres_dict}

    def get_dependency_relation_counts(self, writer, filename, dependency_rel):
        relation_counts = defaultdict(int)
        numbers = list()
        pos = defaultdict(int)
        in_sentence = list()

        result = self._dao.get_magyaralanc_out(writer, filename).content.split("\n")

        for _ in self.dependency_relation_generator(result, in_sentence, dependency_rel, numbers, pos, relation_counts):
            pass

        sorted_relation_counts = dict(sorted(relation_counts.items(), key=itemgetter(1), reverse=True))
        relation_avg = sum(numbers) / len(numbers)
        in_sentence_avg = sum(in_sentence) / len(in_sentence)

        pos_list = list(pos.keys())
        if "Tulajdonnév" in pos_list:
            pos["Tulajdon-\nnév"] = pos.pop("Tulajdonnév")

        if "Határozószó" in pos_list:
            pos["Határozó-\nszó"] = pos.pop("Határozószó")

        sorted_pos = dict(sorted(pos.items(), key=itemgetter(1), reverse=True))

        return sorted_relation_counts, relation_avg, sorted_pos, in_sentence_avg

    def universal_feature_generator(self, result, tag_dict_1, tag_dict_2, uni_feature, feature_tags):
        batch_size = 100

        text_batches = [result[i:i + batch_size] for i in range(0, len(result), batch_size)]

        for batch in text_batches:
            for line in batch:
                if f"{uni_feature}=" not in line:
                    continue

                split_line = line.split("\t")
                # if split_line[2].lower() in self._stopwords:
                #     continue

                if f"{uni_feature}={feature_tags[0]}" in split_line[4]:
                    tag_dict_1[split_line[2]] += 1

                if f"{uni_feature}={feature_tags[1]}" in split_line[4]:
                    tag_dict_2[split_line[2]] += 1

        yield None

    def dependency_relation_generator(self, result, in_sentence, dependency_rel, numbers, pos, relation_counts):
        batch_size = 100
        text_batches = [result[i:i + batch_size] for i in range(0, len(result), batch_size)]
        idx = -1

        for batch in text_batches:
            for line in batch:
                if len(line) <= 0:
                    continue

                split_line = line.split("\t")

                if int(split_line[0]) == 1:
                    in_sentence.append(0)
                    idx += 1

                if dependency_rel not in split_line[6]:
                    continue

                in_sentence[idx] += 1

                if split_line[2].lower() not in self._stopwords:
                    numbers.append(int(split_line[0]) + 1)
                    pos[split_line[3]] += 1
                    relation_counts[split_line[2]] += 1
                    yield None
