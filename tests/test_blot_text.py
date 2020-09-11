import pytest
from pybolt import bolt_text


class TestBoltText(object):

    def test_add_keywords(self):
        assert bolt_text.keywords == set()
        bolt_text.add_keywords("清华大学")
        assert bolt_text.keywords == {"清华大学"}
        bolt_text.add_keywords(["清华大学", "隔壁大学"])
        assert bolt_text.keywords != {"清华大学"}
        assert bolt_text.keywords == {"清华大学", "隔壁大学"}

    def test_add_replace_map(self):
        assert bolt_text.replace_map == {}
        bolt_text.add_replace_map({"清华大学": "北京大学"})
        assert bolt_text.replace_map == {"清华大学": "北京大学"}
        sentence = bolt_text.replace_keywords("我收到了清华大学的录取通知书.")
        assert sentence == "我收到了北京大学的录取通知书."
        sentence = bolt_text.replace_keywords("我收到了隔壁大学的录取通知书.")
        assert sentence == "我收到了隔壁大学的录取通知书."

    def test_extract_keywords(self):
        bolt_text.add_keywords("清华大学")
        found_words = bolt_text.extract_keywords("我收到了清华大学的录取通知书.")
        assert found_words == ['清华大学']
        bolt_text.add_keywords(["清华", "清华大学"])
        found_words = bolt_text.extract_keywords("我收到了清华大学的录取通知书.")
        assert found_words == ['清华', '清华大学']
        found_words = bolt_text.extract_keywords("我收到了清华大学的录取通知书.", longest_only=True)
        assert found_words == ['清华大学']

    def test_batch_extract_keywords(self):
        def get_lines(file):
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    yield line.strip()

        bolt_text.add_keywords(["邓公", "英国女王", "政治"])
        for df in bolt_text.batch_extract_keywords(get_lines("./data/test.corpus")):
            for index, row in df.iterrows():
                assert row.keywords[0] in bolt_text.keywords

    def test_batch_replace_keywords(self):
        def get_lines(file):
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    yield line.strip()

        bolt_text.add_replace_map({"英女王": "美国女王"})
        for df in bolt_text.batch_replace_keywords(get_lines("./data/test.corpus")):
            df = df.loc[df.example.str.contains("美国女王")]
            assert df.shape[0] == 2


if __name__ == "__main__":
    pytest.main(["-s", "test_blot_text.py"])
