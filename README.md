# pybolt
Fast text processing acceleration.
一个快速的文本处理工具.

当前0.0.1测试版:
- 纯python实现
- 实现了关键词查找和替换功能
- 实现了任意维的词汇共现判别
- 当前缺陷:不适用于英文词中包含更小的英文词的情况;批操作未能充分发挥多cpu性能;

## 安装pybolt
```shell script
pip install py-bolt
```

## 使用试例
### Extract keywords
```python
from pybolt import bolt_text
bolt_text.add_keywords(["清华", "清华大学"])
found_words = bolt_text.extract_keywords("我收到了清华大学的录取通知书.")
print(found_words)
# ['清华', '清华大学']
found_words = bolt_text.extract_keywords("我收到了清华大学的录取通知书.", longest_only=True)
print(found_words)
# ['清华大学']
```

### Batch extract keywords
```python
from pybolt import bolt_text
def get_lines():
    yield "我考上了清华大学"
    yield "我梦见我考上了清华大学"

bolt_text.add_keywords(["清华", "清华大学"])
for df in bolt_text.batch_extract_keywords(get_lines(), concurrency=10000000):
    for _, row in df.iterrows():
        print(row.example, row.keywords)
```

### Replace keywords
```python
from pybolt import bolt_text
bolt_text.add_replace_map({"清华大学": "北京大学"})
sentence = bolt_text.replace_keywords("我收到了清华大学的录取通知书.")
print(sentence)
# "我收到了北京大学的录取通知书."
```

### Batch replace keywords
```python
from pybolt import bolt_text

def get_lines():
    yield "我考上了清华大学"
    yield "我梦见我考上了清华大学"

bolt_text.add_replace_map({"清华大学": "北京大学"})
for df in bolt_text.batch_extract_keywords(get_lines(), concurrency=10000000):
    for _, row in df.iterrows():
        print(row.example)
```

### Co-occurrence word recognition
```python
from pybolt import bolt_text
bolt_text.add_co_occurrence_words(["小明", "清华"], "高考")
res, tag = bolt_text.is_co_occurrence("小明考上了清华大学")
print(res, tag)
# True 高考
```

### Batch text processor
```python
from pybolt import bolt_text
def get_lines():
    yield "小明考上了清华大学"
    yield "小明做梦的时候考上了清华大学"
    yield "大明做梦的时候考上了清华大学"
def my_processor(line):
    if line.startswith("小明"):
        return True
    return None

for df in bolt_text.batch_text_processor(get_lines(), my_processor):
    df = df[df["processor_result"].notna()]
    print(df.head())
```

## 性能
测试了关键词查找功能,单句速度相对[flashtext](https://github.com/vi3k6i5/flashtext)提升了30%,批操作速度相对[flashtext](https://github.com/vi3k6i5/flashtext)提升了260%.