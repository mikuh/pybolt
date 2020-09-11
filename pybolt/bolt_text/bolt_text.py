from pybolt.bolt_text.prefix_set import PrefixSet
import pandas as pd
from pandarallel import pandarallel
from multiprocessing import cpu_count
from typing import Iterable


class BoltText(object):

    def __init__(self, workers: int = cpu_count()):
        """
        Args:
        workers: int, cpu count use in batch operation.
        """
        self.ps = PrefixSet()
        pandarallel.initialize(nb_workers=workers)

    @property
    def keywords(self):
        return self.ps.get_keywords()

    @property
    def replace_map(self):
        return self.ps.get_replace_map()

    def add_keywords(self, keywords):
        if isinstance(keywords, str):
            self.ps.add_keyword(keywords)
        elif isinstance(keywords, list):
            self.ps.add_keywords_from_list(keywords)

    def add_replace_map(self, replace_dict: dict):
        self.ps.add_keywords_replace_map_from_dict(replace_dict)

    def extract_keywords(self, sentence, longest_only=False):
        return self.ps.extract_keywords(sentence, longest_only)

    def replace_keywords(self, sentence):
        return self.ps.replace_keywords(sentence)

    def remove_keywords(self, keywords):
        if isinstance(keywords, str):
            return self.ps.remove_keyword(keywords)
        elif isinstance(keywords, list):
            return self.ps.remove_keywords_from_list(keywords)

    def batch_extract_keywords(self, lines: Iterable[str], concurrency: int = 1000000):
        examples = []
        if isinstance(lines, Iterable):
            n = 0
            for line in lines:
                n += 1
                examples.append(line)
                if n % concurrency == 0:
                    yield self.__df_filter(examples)
                    examples.clear()
            if examples:
                yield self.__df_filter(examples)
        else:
            raise TypeError("Argument: `lines` should be a Iterable.")

    def batch_replace_keywords(self, lines: Iterable[str], concurrency: int = 1000000):
        examples = []
        if isinstance(lines, Iterable):
            n = 0
            for line in lines:
                n += 1
                examples.append(line)
                if n % concurrency == 0:
                    yield self.__df_replace(examples)
                    examples.clear()
            if examples:
                yield self.__df_replace(examples)

    def __line_extract_processor(self, line: str):
        found_words = self.extract_keywords(line)
        if found_words:
            return found_words
        return None

    def __line_replace_keywords_processor(self, line: str):
        return self.replace_keywords(line)

    def __df_filter(self, examples: Iterable[str]):
        df = pd.DataFrame(examples, columns=["example"])
        df["keywords"] = df.example.parallel_apply(self.__line_extract_processor)
        df = df[df["keywords"].notna()]
        return df

    def __df_replace(self, examples: Iterable[str]):
        df = pd.DataFrame(examples, columns=["example"])
        df["example"] = df.example.parallel_apply(self.__line_replace_keywords_processor)
        return df
