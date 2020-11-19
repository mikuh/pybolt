import os
import re
from pybolt.utils import package_path


class CharClean(object):
    default_pattern = re.compile("([^\u4E00-\u9FD5\u9FA6-\u9FEF\u3400-\u4DB5a-zA-Z0-9+]+)",
                                 re.U)  # #&\.：:,，/\\\,。！;!?？%\-

    def __init__(self, **kwargs):
        self.__load_char_project(kwargs.get("char_map_file"))

    def normalize(self, sentence: str) -> str:
        return "".join(self._char_project.get(ch, ch) for ch in sentence)

    def clean(self, sentence: str, my_pattern: str = None, pattern_replace: str = "", normalize: bool = True,
              crc_cut: int = 0, num_normal: bool = False) -> str:
        if normalize:
            sentence = self.normalize(sentence)
        sentence = re.sub(r" +", " ", sentence)
        if my_pattern:
            sentence = re.sub(my_pattern, pattern_replace, sentence)
        else:
            sentence = re.sub(self.default_pattern, pattern_replace, sentence)
        if crc_cut:
            sentence = re.sub(r'(.)\1{3,}', r'\1\1\1', sentence)
        if num_normal:
            sentence = re.sub(r'\d+', '▁', sentence)
        return sentence

    def clean_with_index(self, sentence: str, my_pattern: str = None, pattern_replace: str = "", normalize: bool = True,
                         crc_cut: int = 0, num_normal: bool = False):
        # index2char = list(sentence)
        _sentence = sentence
        if normalize:
            _sentence = self.normalize(_sentence)
        char2index = {}
        for i, ch in enumerate(_sentence):
            if ch not in char2index:
                char2index[ch] = []
            char2index[ch].append(i)
        _sentence = re.sub(r" +", " ", _sentence)
        if my_pattern:
            _sentence = re.sub(my_pattern, pattern_replace, _sentence)
        else:
            _sentence = re.sub(self.default_pattern, pattern_replace, _sentence)
        if crc_cut > 0:
            _sentence = re.sub(r'(.)\1{3,}', r'\1\1\1', _sentence)
        if num_normal:
            _sentence = re.sub(r'\d+', '▁', _sentence)
        _index = []
        last_index = -1
        for ch in _sentence:
            if ch not in char2index or len(char2index[ch]) == 0:
                last_index += 1
                _index.append(last_index)
            else:
                last_index = char2index[ch].pop(0)
                _index.append(last_index)
        return _sentence, _index

    def __load_char_project(self, file_path: str = None):
        if file_path is None:
            file_path = os.path.join(package_path, "data", "char_project.txt")
        self._char_project = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                a = line.strip().split("\t")
                assert len(a) == 2
                self._char_project[a[0]] = a[1]
