from pybolt.bolt_nlp import Tokenizer
from pybolt.bolt_text import BoltText


class WordsTagging(object):
    """Label the words in the sentence
    """

    def __init__(self, label_dic: str, word_pool: set = set(), cooc_data: list = [], cooc_order: bool = False):
        self.__tk = Tokenizer(label_dic)
        self.__bt = BoltText()
        self.__word_tag_map = self.__generate_word_tag_project(label_dic, word_pool)
        self.__init_co_occurrence_words(cooc_data, cooc_order)

    def tag(self, sentence: str, use_hmm=True, co_order=False):
        word_tag_list = [[word, self.__word_tag_map.get(word, 'New')] for word in self.__tk.cut(sentence, HMM=use_hmm)]
        print(word_tag_list)
        query_words = [word for word, tag in word_tag_list if word in self.__bt.keywords]
        # co occurrence words adjust
        match_words, words_index = self.__bt.get_co_occurrence_words(sentence, founds_words=query_words, order=co_order)
        index_tag = {}
        for k, v in words_index.items():
            for x in range(v[0], v[1]):
                index_tag[x] = match_words[k]
        i = -1
        for word, tag in word_tag_list:
            if word in match_words:
                tag = match_words[word]
            for ch in word:
                i += 1
                if i in index_tag:
                    tag = index_tag[i]

                yield (ch, tag)

    def __generate_word_tag_project(self, label_dic, word_pool):
        word_tag_map = {}
        with open(label_dic, 'r', encoding='utf-8') as f:
            for line in f:
                t = line.strip().split()
                word_tag_map[t[0]] = t[2]
        for word in word_pool:
            if word not in word_tag_map:
                word_tag_map[word] = "Normal"
        return word_tag_map

    def __en_check(self):
        pass

    def __num_check(self):
        pass

    def __cooc_check(self):
        pass

    def __init_co_occurrence_words(self, cooc_data: list, order: bool = False):
        """Initialize co-occurrence keywords
        :param cooc_data: like [(word1,word2,word3,..., Label), (word1,word2,...,Label),...]
        :return:
        """
        for words in cooc_data:
            self.__bt.add_co_occurrence_words(words[:-1], words[-1], order)


if __name__ == '__main__':
    pass

    wt = WordsTagging(label_dic="/home/geb/PycharmProjects/nlp-data/default_dict.txt",
                      cooc_data=[["长者", "续一秒", "Politics"], ["我", "大大", "长者", "Abuse"]])

    a = wt.tag("我为长者和大大续一秒")

    print(" ".join([f"{w}/{t}" for w, t in a]))
