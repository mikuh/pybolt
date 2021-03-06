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

    def test_extract_keywords_with_index(self):
        bolt_text.clear_keywords()
        bolt_text.add_keywords("清华大学")
        sentence = "我收到了清华大学的录取通知书"
        found_words = bolt_text.extract_keywords_with_index(sentence)
        assert len(found_words) == 1
        for word, index in found_words:
            assert word == sentence[index[0]: index[1]]
        bolt_text.clear_keywords()
        bolt_text.add_keywords(["清华", "清华大学"])
        sentence = "我收到了清华大学的录取通知书"
        found_words = bolt_text.extract_keywords_with_index(sentence)
        assert len(found_words) == 2
        for word, index in found_words:
            assert word == sentence[index[0]: index[1]]
        found_words = bolt_text.extract_keywords_with_index(sentence, longest_only=True)
        assert len(found_words) == 1
        for word, index in found_words:
            assert word == sentence[index[0]: index[1]]

    def test_is_co_occurrence(self):
        bolt_text.add_co_occurrence_words(["小明", "清华", "大学"], "Normal")
        a = bolt_text.is_co_occurrence("小明考上了清华大学")
        assert a == (True, ['Normal'])
        bolt_text.add_co_occurrence_words(["小明", "大学"], "Normal")
        a = bolt_text.is_co_occurrence("小明考上了清华大学")
        assert a == (True, ['Normal'])
        bolt_text.add_co_occurrence_words_from_list([["中国", "人民", "nb", "Normal"], ["美国人", "nb", "Normal"]])
        a = bolt_text.is_co_occurrence("中国人民是不是比美国人民nb呀")
        assert a == (True, ['Normal'])

    def test_bath_text_processor(self):
        def get_lines(file):
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    yield line.strip()

        def processor(sentence):
            a, b = bolt_text.is_co_occurrence(sentence)
            if a:
                return b
            return None

        bolt_text.add_co_occurrence_words(["长者", "续一秒"], "Politics")
        for df in bolt_text.batch_text_processor(get_lines("./data/test.corpus"), processor=processor):
            df = df[df["processor_result"].notna()]
            for index, row in df.iterrows():
                assert True == ("长者" in row.example and "续一秒" in row.example)

    def test_alpha_keywords_extract(self):
        bolt_text.add_keywords(["js", "java"])
        found_words = bolt_text.extract_keywords("javascript的简称是js.")
        print(found_words)

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

    def test_bolt_char_clean(self):
        import re
        assert "0角无" == bolt_text.normalize("⓪⻆🈚")
        assert "aa" == bolt_text.clean("a     a")
        _pattern = re.compile("([^\u4E00-\u9FD5\u9FA6-\u9FEF\u3400-\u4DB5a-zA-Z0-9 +]+)", re.U)
        assert "aaa+++abcadf ga a" == bolt_text.clean("aaaaa+++++.....abcadf    ga   a", my_pattern=_pattern,
                                                      pattern_replace="", normalize=True, crc_cut=3)

        assert "asd▁ad▁我艹▁" == bolt_text.clean("asd11111ad123我艹45687761", my_pattern=_pattern,
                                               pattern_replace="", normalize=True, crc_cut=3, num_normal=True)

    def test_bolt_char_clean_index(self):
        with open("data/examples.txt", 'r', encoding='utf-8') as f:
            for line in f:
                sentence1 = bolt_text.clean(line)
                sentence2, index = bolt_text.clean_with_index(line)
                assert sentence1 == sentence2
                assert sentence2 == bolt_text.clean("".join([line[i] for i in index]))


if __name__ == "__main__":
    pytest.main(["-s", "test_blot_text.py"])
