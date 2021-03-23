import Levenshtein
from pybolt import package_path
import os
import json
import math

hanzi_file = os.path.join(package_path, "data/hanzi.json")
zi_pinyin_file = os.path.join(package_path, "data/zi_pinyin.txt")
with open(hanzi_file, 'r', encoding='utf-8') as f:
    zi = json.load(f)

zi_pinyin = {}
with open(zi_pinyin_file, 'r', encoding='utf-8') as f:
    for line in f:
        a = line.strip().split()
        zi_pinyin[a[0]] = a[1]

INITIALS = {'b': '00000', 'p': '00001', 'm': '00011', 'f': '00010',
            'd': '00111', 't': '00101', 'n': '00100', 'l': '01100',
            'g': '01111', 'k': '01110', 'h': '01010',
            'j': '01001', 'q': '01000', 'x': '11000',
            'zh': '11011', 'ch': '11010', 'sh': '11110', 'r': '11111',
            'z': '11011', 'c': '11010', 's': '11110',
            'y': '11111', 'w': '11100', '_': '10100'}

FIRST = {'a': '00000', 'ai': '00001', 'ao': '00011', 'an': '00010', 'ang': '00010',
         'i': '00111', 'ie': '00101', 'iu': '00100', 'in': '01100', 'ing': '01100',
         'o': '01111', 'ou': '01110', 'ong': '01010',
         'e': '01001', 'ei': '01000', 'er': '11000', 'en': '11001', 'eng': '11001',
         'u': '11010', 'ui': '11110', 'un': '11111',
         'v': '11100', 've': '10100', 'vn': '10101',
         '_': '10111'}
# 声调
Level = ['00', '00', '01', '10', '11', '00']

Struct = {
    "单一": "0000",
    "左右": "0001",
    "左中右": "0011",
    "上下": "0010",
    "上中下": "0110",
    "左上包围": "0111",
    "左下包围": "0101",
    "右上包围": "0100",
    "上三包围": "1100",
    "下三包围": "1101",
    "左三包围": "1111",
    "全包围": "1110",
    "镶嵌": "1010",
    "品字": "1011",
    "田字": "1001"
}

SiJiao = ["0000", "0001", "0011", ""]


def chinese_char_sound_gray_encode(ch):
    _py = zi_pinyin.get(ch, None)
    if _py is None:
        return None
    _level = int(_py[-1])
    _py = _py[:-1]
    if _py.startswith(('zh', 'ch', 'sh')):
        _initials = _py[:2]
    elif _py in FIRST:
        _initials = "_"
        _py = "_" + _py
    else:
        _initials = _py[:1]
    _middle = '_'
    if len(_py[len(_initials):]) == 0:
        _first = "_"
    elif _py[len(_initials):] not in FIRST:
        _middle = _py[len(_initials)]
        _first = _py[len(_initials) + 1:]
    else:
        _first = _py[len(_initials):]
    gray_code = f"{INITIALS[_initials]}{FIRST[_first]}{FIRST[_middle]}{Level[_level]}"
    return gray_code





def chinese_char_graph_encode(ch, struct_weight: int = 2, sijiao_weight: int = 4):
    if ch not in zi:
        return None
    if zi[ch]["四角"] is None or zi[ch]["结构"] is None or zi[ch]["总笔画"] is None:
        return None
    codes = ""
    struct = Struct[zi[ch]["结构"]]
    codes += struct * struct_weight
    sijiao = zi[ch]["四角"][:4]
    codes += sijiao * sijiao_weight
    strokes = int(zi[ch]["总笔画"])
    if strokes > 16:
        strokes = 16
    codes += "".join(["1" if i < strokes else "0" for i in range(16)])
    return codes


def hm_sim_str(s1, s2):
    """字符串的汉明距离"""
    if s1 is None or s2 is None:
        return -999.9
    if len(s1) != len(s2):
        raise ValueError("Not same length:`s1`, `s2`")
    return math.log(sum(el1 == el2 for el1, el2 in zip(s1, s2)) / len(s1))


def edit_sim_str(s1, s2):
    return 1 - Levenshtein.distance(s1, s2) / len(s1)


if __name__ == '__main__':
    # gray_code = chinese_char_gray_encode("毛泽东的条件是可以穷举的吗")

    # print(gray_code)

    s1 = "傞"
    s2 = "涿"

    hanming_sim = hm_sim_str(chinese_char_sound_gray_encode(s1), chinese_char_sound_gray_encode(s2))
    print(f"`{s1}` and `{s2}` 的发音相似度为: {hanming_sim}")

    s1 = "泽"
    s2 = "贼"

    hanming_sim = hm_sim_str(chinese_char_sound_gray_encode(s1), chinese_char_sound_gray_encode(s2))
    print(f"`{s1}` and `{s2}` 的发音相似度为: {hanming_sim}")

    s1 = "毛"
    s2 = "喵"

    hanming_sim = hm_sim_str(chinese_char_sound_gray_encode(s1), chinese_char_sound_gray_encode(s2))
    print(f"`{s1}` and `{s2}` 的发音相似度为: {hanming_sim}")

    s1 = "茶"
    s2 = "荼"
    hanming_sim = hm_sim_str(chinese_char_graph_encode(s1), chinese_char_graph_encode(s2))
    print(f"`{s1}` and `{s2}` 的字形相似度为: {hanming_sim}")

    # 汩 汨
    s1 = "汩"
    s2 = "汨"
    hanming_sim = hm_sim_str(chinese_char_graph_encode(s1), chinese_char_graph_encode(s2))
    print(f"`{s1}` and `{s2}` 的字形相似度为: {hanming_sim}")

    s = "弛驰他她施"
    import itertools

    s = list(itertools.combinations(list(s), 2))
    for (s1, s2) in s:
        hanming_sim = hm_sim_str(chinese_char_graph_encode(s1), chinese_char_graph_encode(s2))
        print(f"`{s1}` and `{s2}` 的字形相似度为: {hanming_sim}")


    s1 = "近"
    s2 = "远"
    hanming_sim = hm_sim_str(chinese_char_graph_encode(s1), chinese_char_graph_encode(s2))
    print(f"`{s1}` and `{s2}` 的字形相似度为: {hanming_sim}")

    # edit_sim = edit_sim_str("".join(chinese_char_gray_encode(s1)), "".join(chinese_char_gray_encode(s2)))
    # print(f"`{s1}` and `{s2}` 的发音格雷编辑相似度为: {edit_sim}")

    # import pickle
    # with open("/home/geb/PycharmProjects/pybolt/pybolt/data/four_code.pkl", 'rb') as f:
    #     a = pickle.load(f)
    #     print(a)
