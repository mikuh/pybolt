"""

"""
import math
import re
import os
import sys
from pybolt.bolt_nlp import finalseg

re_eng = re.compile('[a-zA-Z0-9]', re.U)
re_han = re.compile("([\u4E00-\u9FD5\u9FA6-\u9FEF\u3400-\u4DB5a-zA-Z0-9+\\\/]+)", re.U)
re_skip = re.compile("(\r\n|\s)", re.U)


class Tokenizer(object):

    def __init__(self, vocab: str = None):
        self.prefix_freq = {}
        self.total = 0
        self.__generate_prefix_dict(self.__load_dict(vocab))

    def __generate_prefix_dict(self, lines: iter):
        """Generate the prefix dict for cut words
        Args:
            lines: a iterator, each line is `word freq tag`
        """
        for line in lines:
            word, freq = line.strip().split()[:2]
            freq = int(freq)
            self.prefix_freq[word] = freq
            self.total += freq
            for i in range(len(word)):
                prefix_word = word[:i + 1]
                if prefix_word not in self.prefix_freq:
                    self.prefix_freq[prefix_word] = 0

    def __load_dict(self, vocab: str):
        """Load the dict for cut.
        """
        if vocab is None:
            vocab = os.path.dirname(
                sys.modules[__package__].__file__) + "/data/default_dict.txt"
        with open(vocab, 'r', encoding='utf-8') as f:
            for line in f:
                yield line

    def generate_dag(self, sentence: str) -> dict:
        """Generate DAG based on vocab
        Args:
            sentence: str, a sentence string
        Return:
            the DAG dict, like {0: [0], 1: [1,2,4], 2: [2], 3: [3,4], 4: [4], 5: [5]}
        """
        DAG = {}
        N = len(sentence)
        for k in range(N):
            _list = []
            i = k
            frag = sentence[k]
            while i < N and frag in self.prefix_freq:
                if self.prefix_freq[frag] > 0:
                    _list.append(i)
                i += 1
                frag = sentence[k:i + 1]
            if not _list:
                _list.append(k)
            DAG[k] = _list
        return DAG

    def calculate_max_pro_route(self, sentence: str, DAG: dict, route: dict):
        """Calculate the maximum probability cut path
        Args:
            sentence: str, the string to be cut
            DAG: dict, sentence cut DAG
            route: the cut route
        """
        N = len(sentence)
        route[N] = (0, 0)
        log_total = math.log(self.total)
        for idx in range(N - 1, -1, -1):
            route[idx] = max((math.log(self.prefix_freq.get(sentence[idx:x + 1]) or 1) -
                              log_total + route[x + 1][0], x) for x in DAG[idx])

    def __cut_DAG_no_HMM(self, sentence):
        DAG = self.generate_dag(sentence)
        route = {}
        self.calculate_max_pro_route(sentence, DAG, route)
        x = 0
        N = len(sentence)
        buf = ''
        while x < N:
            y = route[x][1] + 1
            l_word = sentence[x:y]
            if re_eng.match(l_word) and len(l_word) == 1:
                buf += l_word
                x = y
            else:
                if buf:
                    yield buf
                    buf = ''
                yield l_word
                x = y
        if buf:
            yield buf
            buf = ''

    def __cut_DAG(self, sentence):
        DAG = self.generate_dag(sentence)
        route = {}
        self.calculate_max_pro_route(sentence, DAG, route)
        x = 0
        buf = ''
        N = len(sentence)
        while x < N:
            y = route[x][1] + 1
            l_word = sentence[x:y]
            if y - x == 1:
                buf += l_word
            else:
                if buf:
                    if len(buf) == 1:
                        yield buf
                        buf = ''
                    else:
                        if not self.prefix_freq.get(buf):
                            recognized = finalseg.cut(buf)
                            for t in recognized:
                                yield t
                        else:
                            for elem in buf:
                                yield elem
                        buf = ''
                yield l_word
            x = y

        if buf:
            if len(buf) == 1:
                yield buf
            elif not self.prefix_freq.get(buf):
                recognized = finalseg.cut(buf)
                for t in recognized:
                    yield t
            else:
                for elem in buf:
                    yield elem

    def cut(self, sentence, HMM=True):
        """cut the sentence
        """
        if HMM:
            cut_block = self.__cut_DAG
        else:
            cut_block = self.__cut_DAG_no_HMM

        blocks = re_han.split(sentence)
        for blk in blocks:
            if not blk:
                continue
            if re_han.match(blk):
                for word in cut_block(blk):
                    yield word
            else:
                tmp = re_skip.split(blk)
                for x in tmp:
                    if re_skip.match(x):
                        yield x
                    else:
                        for xx in x:
                            yield xx


if __name__ == '__main__':


    tk = Tokenizer("/home/geb/PycharmProjects/nlp-data/taptap_dict.txt")

    print(" ".join(tk.cut("习习习习习习,习蛤蛤,蛤蛤,,习蛤蟆闹革命,傻逼")))