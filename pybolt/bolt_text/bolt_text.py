from pybolt.bolt_text.prefix_set import PrefixSet
import pandas as pd
from inspect import isgenerator
from pandarallel import pandarallel


class BoltText(object):

    def __init__(self):
        self.ps = PrefixSet()

    def add_keywords(self, keywords):
        if isinstance(keywords, str):
            self.ps.add_keyword(keywords)
        elif isinstance(keywords, list):
            self.ps.add_keywords_from_list(keywords)

    def add_replace_map(self, replace_dict):
        self.ps.add_keywords_replace_map_from_dict(replace_dict)

    def extract_keywords(self, sentence, longest_only):
        return self.ps.extract_keywords(sentence, longest_only)

    def replace_keywords(self, sentence):
        return self.ps.replace_keywords(sentence)

    def remove_keywords(self, keywords):
        if isinstance(keywords, str):
            return self.ps.remove_keyword(keywords)
        elif isinstance(keywords, list):
            return self.ps.remove_keywords_from_list(keywords)

    def batch_extract_keywords(self, lines, processor, concurrency=1000000, workers=None):
        if workers > 1:
            pandarallel.initialize(nb_workers=workers)
        examples = []
        if isgenerator(lines):
            n = 0
            for line in lines:
                n += 1
                examples.append(line)
                if n % concurrency == 0:
                    df = pd.DataFrame(examples, columns=["example"])
                    if workers > 1:
                        df.parallel_apply(processor)
                    else:
                        df.apply(processor)

    def __line_processor(self, line):
        found_words = self.extract_keywords(line)
        if found_words:
            return None