from typing import Iterable, List
from collections import Counter
import numpy as np
from pybolt.utils import default_logger as logging
import joblib
import time


class TFIDF(object):

    def __init__(self, corpus: Iterable):
        self.corpus = corpus
        self.total_doc_num = 0
        self.word_doc_count = Counter()

    def learn_idf(self):
        logging.info("Learning IDF from corpus ...")
        for text in self.corpus:
            self.total_doc_num += 1
            for word in set(text.split()):
                self.word_doc_count[word] += 1
        logging.info("Init idf successfully!")

    def load_idf(self, file: str):
        start = time.time()
        idf = joblib.load(file)
        self.total_doc_num = idf["total_doc_num"]
        self.word_doc_count = idf["word_doc_count"]
        logging.info("Loading idf cost {} seconds.".format(time.time() - start))

    def save_idf(self, file: str):
        if self.total_doc_num == 0:
            return UnboundLocalError("Word doc count not be Inited!")
        idf = {
            "total_doc_num": self.total_doc_num,
            "word_doc_count": self.word_doc_count,
        }
        joblib.dump(idf, file)

    def idf(self, word: str):
        if self.total_doc_num == 0:
            return UnboundLocalError("Word doc count not be Inited!")
        return np.log(self.total_doc_num / self.word_doc_count.get(word, 1))

    def tfidf(self, word: str, word_frequency: float):
        if self.total_doc_num == 0:
            return UnboundLocalError("Word doc count not be Inited!")
        return word_frequency * self.idf(word)

    def tfidf_sentece(self, sentence: str) -> List[float]:
        sentence = sentence.split()
        word_count = Counter(sentence)
        length = len(sentence)
        if length == 0:
            return []
        return [self.tfidf(word, word_count[word] / length) for word in sentence]


if __name__ == '__main__':
    corpus = [
        'This is the first document.',
        'This document is the second document.',
        'And this is the third one.',
        'Is this the first document?']
    tfidf = TFIDF(corpus)
    tfidf.learn_idf()

    print(tfidf.idf("This"))
    print(tfidf.idf("haha"), tfidf.tfidf("haha", 0.2))
    print(tfidf.tfidf_sentece(
        "This is the first document."))  # [0.13862943611198905, 0.05753641449035617, 0.0, 0.13862943611198905, 0.13862943611198905]

    tfidf.save_idf("text.idf")

    del tfidf

    tfidf = TFIDF(corpus)
    tfidf.load_idf("text.idf")
    print(tfidf.tfidf_sentece("This is the first document."))
