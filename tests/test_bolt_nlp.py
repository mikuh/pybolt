import pytest
from pybolt.bolt_nlp import WordDiscover
from pybolt.bolt_nlp.naive_bayes_classification.utils import get_data_set_test
from pybolt.bolt_nlp import BernoulliClassifier
from pybolt.bolt_nlp import Tokenizer

class TestBoltNlp(object):

    def test_word_discover(self):
        wd = WordDiscover()
        wd.word_discover(["/home/geb/PycharmProjects/pybolt/tests/data/examples.txt"])

    def test_bernoulli_nb(self):
        inputs, targets = get_data_set_test([("./data/adv.cut", 'Ad'),
                                             ("./data/not_adv.cut", 'Normal')])
        bc = BernoulliClassifier()
        bc.fit(inputs, targets)
        assert round(bc.accuracy, 16) == 0.9959251101321586

    def test_tokenizer(self):
        tk = Tokenizer("/home/geb/PycharmProjects/nlp-data/default_dict.txt")
        assert " ".join(tk.cut("你刺客攻击没我萨满高hhh,可以加\/吗")) == "你 刺客 攻击 没 我 萨满 高 hhh , 可以 加\/ 吗"


if __name__ == "__main__":
    pytest.main(["-s", "test_blot_nlp.py"])
