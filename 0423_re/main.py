# 正規表現(regular expressions)
#  文字列をパターンにて表現するもの。
#  そのパターンにマッチしているか、
#  否かの判定が行える。
import re

# パターンの記述には、raw stringが推奨。
# ※正規表現にて「\」が特殊文字のため、
#  pythonと喧嘩しないように。
pattern = r'これは\nrow string'
print(pattern)

pattern = 'a'
str = 'a'
# パターンマッチのチェックは、ｍatch関数、またはsearch関数を使用。
re.match(pattern, str)

# マッチ時は、マッチオブジェクトが返される。
print(re.match(pattern, str))

# ミスマッチの場合は、Noneが返される。
str = 'b'
print(re.match(pattern, str))

# パターンにマッチするかしないかは、if文で判定できる。

if re.match(pattern, 'a'):
    print('match')
else:
    print('mismatch')

if re.match(pattern, str):
    print('match')
else:
    print('mismatch')

# match は先頭からの検証が前提。
print(re.match(r'a', 'abc'))
print(re.match(r'b', 'abc'))  # miss
print(re.match(r'c', 'abc'))  # miss

# search は先頭縛りなし。
print(re.search(r'a', 'abc'))
print(re.search(r'b', 'abc'))
print(re.search(r'c', 'abc'))

# 大文字・小文字は既定では区別される。
print(re.match(r'ABC', 'abc'))  # miss
print(re.match(r'Abc', 'abc'))  # miss
print(re.match(r'Abc', 'abc', re.IGNORECASE))  # match

# 正規表現のパターンには、特殊文字がある。
print('^$. -----')
print(re.match(r'^abc', 'abc'))  # match
print(re.match(r'^abc', 'aabc'))  # miss
print(re.match(r'^.abc', 'aabc'))  # match
print(re.match(r'^.abc', 'babc'))  # match
print(re.match(r'^.abc', 'babcdef'))  # match
