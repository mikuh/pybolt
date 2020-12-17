from pypinyin import lazy_pinyin, Style
import Levenshtein

INITIALS = {'b': '00000', 'p': '00001', 'm': '00011', 'f': '00010',
            'd': '00111', 't': '00101', 'n': '00100', 'l': '01100',
            'g': '01111', 'k': '01110', 'h': '01010',
            'j': '01001', 'q': '01000', 'x': '11000',
            'zh': '11011', 'ch': '11010', 'sh': '11110', 'r': '11111',
            'z': '11011', 'c': '11010', 's': '11110',
            'y': '11100', 'w': '10100'}

FIRST = {'a': '00000', 'ai': '00001', 'ao': '00011', 'an': '00010', 'ang': '00010',
         'i': '00111', 'ie': '00101', 'iu': '00100', 'in': '01100', 'ing': '01100',
         'o': '01111', 'ou': '01110', 'ong': '01010',
         'e': '01001', 'ei': '01000', 'er': '11000', 'en': '11001', 'eng': '11001',
         'u': '11010', 'ui': '11110', 'un': '11111',
         'v': '11100', 've': '10100', 'vn': '10101',
         '_': '00000'}

Level = ['00', '00', '01', '10', '11', '00']


def chinese_char_gray_encode(ch):
    _pys = lazy_pinyin(ch, style=Style.TONE3, neutral_tone_with_five=True)
    gray_codes = []
    for _py in _pys:
        _level = int(_py[-1])
        _py = _py[:-1]
        if _py.startswith(('zh', 'ch', 'sh')):
            _initials = _py[:2]
        else:
            _initials = _py[:1]
        _middle = '_'
        if _py[len(_initials):] not in FIRST:
            _middle = _py[len(_initials)]
            _first = _py[len(_initials) + 1:]
        else:
            _first = _py[len(_initials):]
        gray_code = f"{INITIALS[_initials]}{FIRST[_first]}{FIRST[_middle]}{Level[_level]}"
        gray_codes.append(gray_code)
    return gray_codes


def hm_sim_str(s1, s2):
    """字符串的汉明距离"""
    if len(s1) != len(s2):
        raise ValueError("Not same length:`s1`, `s2`")
    return sum(el1 == el2 for el1, el2 in zip(s1, s2)) / len(s1)


def edit_sim_str(s1, s2):
    return 1 - Levenshtein.distance(s1, s2) / len(s1)


if __name__ == '__main__':
    gray_code = chinese_char_gray_encode("毛泽东的条件是可以穷举的吗")

    print(gray_code)

    s1 = "江泽民"
    s2 = "江贼名"


    hanming_sim = hm_sim_str("".join(chinese_char_gray_encode(s1)), "".join(chinese_char_gray_encode(s2)))
    print(f"`{s1}` and `{s2}` 的发音格雷汉明相似度为: {hanming_sim}")

    edit_sim = edit_sim_str("".join(chinese_char_gray_encode(s1)), "".join(chinese_char_gray_encode(s2)))
    print(f"`{s1}` and `{s2}` 的发音格雷编辑相似度为: {edit_sim}")



    import pickle
    with open("/home/geb/PycharmProjects/pybolt/pybolt/data/four_code.pkl", 'rb') as f:
        a = pickle.load(f)
        print(a)