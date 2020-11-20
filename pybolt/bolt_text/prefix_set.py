from itertools import combinations
from collections import Counter


class PrefixSet(object):

    def __init__(self):
        self._prefix_dic = {}
        self._replace_map = {}
        self._co_occurrence_words = {}
        self._co_dims = set()
        self.co_occurrence_counts = Counter()

    def get_keywords(self):
        return {w for w, f in self._prefix_dic.items() if f == 1}

    def get_replace_map(self):
        return {a: b for a, b in self._replace_map.items() if b is not None}

    def add_keywords_from_list(self, words: list):
        for word in words:
            self.add_keyword(word)

    def add_keyword(self, word):
        w = ""
        for ch in word:
            w += ch
            if w not in self._prefix_dic:
                self._prefix_dic[w] = 0
        self._prefix_dic[w] = 1

    def add_co_occurrence_words(self, word_list: list, tag=None, order=False):
        """
        :param word_list: like this [word1, word2]
        :param tag: co-occurrence words's tag
        :param order: whether to use the default sort
        """
        if not order:
            word_list.sort()
        for word in word_list:
            self.add_keyword(word)
        key = ",".join(word_list)
        self._co_occurrence_words[key] = tag
        self._co_dims.add(len(word_list))

    def add_co_occurrence_words_from_list(self, co_words_list: list, order=False):
        """
        :param co_words_list: just like [[word1,word2,tag],[word1,word2,None],...]
        :param order: whether to use the default sort
        """
        for word_list in co_words_list:
            self.add_co_occurrence_words(word_list=word_list[:-1], tag=word_list[-1], order=order)

    def is_co_occurrence(self, sentence: str, order: bool = False, one_return: bool = True):
        founds = self.extract_keywords(sentence)
        flag = False
        tag = None
        tags = []
        if len(founds) < 2:
            return flag, tag
        dims = list(self._co_dims)
        dims.sort()
        for dim in dims:
            groups = combinations(founds, dim)
            for group in groups:
                group = list(group)
                if not order:
                    group.sort()
                _key = ",".join(group)
                if _key in self._co_occurrence_words:
                    if one_return:
                        return True, [self._co_occurrence_words[_key]]
                    tag = self._co_occurrence_words[_key]
                    tags.append(tag)
        return flag, tags

    def get_co_occurrence_words(self, sentence: str, founds_words: list = None, order=False):
        words_index = {}
        if founds_words is None:
            founds_words = []
            _founds_words = self.extract_keywords_with_index(sentence, longest_only=True)
            for word, index in _founds_words:
                if word not in words_index:
                    words_index[word] = []
                words_index[word].append(index)
                founds_words.append(word)
        if len(founds_words) < 2:
            return {}, {}
        dims = list(self._co_dims)
        dims.sort()
        match_words = {}
        for dim in dims:
            groups = combinations(founds_words, dim)
            for group in groups:
                group = list(group)
                if not order:
                    group.sort()
                _key = ",".join(group)
                if _key in self._co_occurrence_words:
                    for w in _key.split(","):
                        match_words[w] = self._co_occurrence_words[_key]
        return match_words, words_index

    def add_keywords_replace_map_from_dict(self, source_target_map: dict):
        for a, b in source_target_map.items():
            w = ""
            for ch in a:
                w += ch
                if w not in self._replace_map:
                    self._replace_map[w] = None
            self._replace_map[a] = b

    def remove_keywords_from_list(self, words: list):
        for word in words:
            self.remove_keyword(word)

    def remove_keyword(self, word: str):
        self._prefix_dic[word] = 0

    def extract_keywords(self, sentence: str, longest_only=False) -> list:
        """Extract keywords involved in sentences
        Args:
            sentence: str, Sentences to be extracted.
            longest_only: bool,Whether to match only the longest keyword,default False;
                        for a example sentence: `category`, and keywords is ['cat', 'category'],
                        if set False, return: ['cat', 'category'],
                        if set True, return the longest only: ['category']
        """
        N = len(sentence)
        keywords = []
        for i in range(N):
            flag = sentence[i]
            j = i
            word = None
            while j < N and (flag in self._prefix_dic):
                if self._prefix_dic[flag] == 1:
                    if not longest_only:
                        keywords.append(flag)
                    else:
                        word = flag
                j += 1
                flag = sentence[i: j + 1]
            if longest_only and word:
                keywords.append(word)
        return keywords

    def extract_keywords_with_index(self, sentence: str, longest_only=False):
        N = len(sentence)
        keywords = []
        for i in range(N):
            flag, index = sentence[i], [i, i + 1]
            j = i
            word = None
            while j < N and (flag in self._prefix_dic):
                if self._prefix_dic[flag] == 1:
                    if not longest_only:
                        keywords.append((flag, index))
                    else:
                        word, _index = flag, index
                j += 1
                flag, index = sentence[i: j + 1], [i, j + 1]
            if longest_only and word:
                keywords.append((word, _index))
        return keywords

    def replace_keywords(self, sentence: str) -> str:
        """Replace word use keywords map.
        Args:
            sentence: str, Sentences that need to replace keywords.
        Return:
            the new sentence after replace keywords.
        """
        N = len(sentence)
        new_sentence = ""
        i = 0
        while i < N:
            flag = sentence[i]
            j = i
            word = None
            while j < N and (flag in self._replace_map):
                if self._replace_map[flag]:
                    word = flag
                j += 1
                flag = sentence[i: j + 1]
            if word:
                new_sentence += self._replace_map[word]
                i = j
            else:
                new_sentence += sentence[i]
                i += 1
        return new_sentence


if __name__ == '__main__':
    ps = PrefixSet()

    # ps.add_co_occurrence_words(["小明", "清华", "大学"], "Normal")
    # ps.add_co_occurrence_words(["长者", "续一秒"], "Politics")
    #
    # a, b = ps.is_co_occurrence("小明考上了清华大学")
    #
    # print(a, b)
    #
    # a, b = ps.is_co_occurrence("我要给长者续一秒", one_return=False)
    #
    # print(a, b)
    #
    # print(ps.extract_keywords_with_index("我要给长者续一秒"))
    cooc_file = "/home/geb/PycharmProjects/nlp-data/co-occurrence-words-v2.txt"
    cooc_data = []
    with open("/home/geb/PycharmProjects/nlp-data/co-occurrence-words-v2.txt", 'r', encoding='utf-8') as f:
        for line in f:
            cooc_data.append(line.strip().split())
    for x in cooc_data:
        ps.add_co_occurrence_words(x[:-1], x[-1])

    print(ps.extract_keywords_with_index("这1星评论就一直放这儿!反正官方只要查他俩角色数据指定能看出开挂痕迹!要因为充钱了就能开挂被护犊子,这评论就一直放这儿让所有玩家瞧瞧你家的态度!", longest_only=True))

    print(ps.get_co_occurrence_words("这1星评论就一直放这儿!反正官方只要查他俩角色数据指定能看出开挂痕迹!要因为充钱了就能开挂被护犊子,这评论就一直放这儿让所有玩家瞧瞧你家的态度!"))