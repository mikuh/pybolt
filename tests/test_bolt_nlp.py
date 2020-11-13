import pytest
from pybolt.bolt_nlp import WordDiscover


class TestBoltNlp(object):

    def test_word_discover(self):
        wd = WordDiscover()
        wd.word_discover(["/home/geb/PycharmProjects/pybolt/tests/data/examples.txt"])


if __name__ == "__main__":
    pytest.main(["-s", "test_blot_nlp.py"])
