class PrefixSet(object):

    def __init__(self):
        self._prefix_dic = {}
        self._replace_map = {}

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
    ps.add_keywords_from_list(["清华", "清华大学"])

    from flashtext import KeywordProcessor

    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_list(["清华", "清华大学"])
    words = ps.extract_keywords("我收到了清华大学的录取通知书.")
    words2 = keyword_processor.extract_keywords("我收到了清华大学的录取通知书.")
    words3 = ps.extract_keywords("我收到了清华大学的录取通知书.", longest_only=True)
    print(words)
    print(words2)
    print(words3)

    ps.add_keywords_replace_map_from_dict({"清华": "北京", "清华大学": "清华隔壁"})
    new_sentence = ps.replace_keywords("我收到了清华大学的录取通知书.")
    print(new_sentence)
