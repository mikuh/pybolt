import os
import sys
from pybolt.utils import package_path


class CharClean(object):

    def __init__(self, **kwargs):
        self.__load_char_project(kwargs.get("char_map_file"))

    def normalize(self, sentence: str) -> str:
        return "".join(self._char_project.get(ch, ch) for ch in sentence)

    def clean(self, sentence: str) -> str:
        pass

    def __load_char_project(self, file_path: str = None):
        if file_path is None:
            file_path = os.path.join(package_path, "data", "char_project.txt")
        self._char_project = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                a = line.strip().split("\t")
                assert len(a) == 2
                self._char_project[a[0]] = a[1]
