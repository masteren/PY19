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
print(re.search(r'^abc', 'abc'))  # match
print(re.search(r'^abc', 'aabc'))  # miss
print(re.search(r'^.abc', 'aabc'))  # match
print(re.search(r'^.abc', 'babc'))  # match
print(re.search(r'^.abc', 'babcdef'))  # match

print(re.search(r'^abc$', 'abc'))  # match
print(re.search(r'abc$', 'xxxabc'))
print(re.search(r'...abc$', 'xxxxabc'))
print(re.search(r'...abc$', 'xxabc'))  # miss
print(re.search(r'^...abc$', 'xxxxabc'))  # miss

# 繰り返し指定のメタ文字
#  「直前の文字が」何回繰り返すかを
#  指定することができる。
#  + … 1回以上
#  * … 0回以上
#  ? … 0回か、1回
#  {m}   … m回
#  {m,n} … m回以上、n回以下
#  {m,}  … m回以上
#  {,n}  … n回以下
print('+*?{m}{m,n}{m,}{,n}---------------------')
print(re.search(r'a+bc', 'abc'))
print(re.search(r'a+bc', 'aabc'))
print(re.search(r'a+bc', 'aaabc'))
print(re.search(r'a+bc', 'bc'))  # miss

print(re.search(r'a*bc', 'abc'))
print(re.search(r'a*bc', 'aaabc'))
print(re.search(r'a*bc', 'bc'))
print(re.search(r'a*bc', 'xbc'))

print(re.search(r'a?bc', 'abc'))
print(re.search(r'a?bc', 'bc'))
print(re.search(r'a?bc', 'aabc'))
print(re.search(r'^a?bc', 'aabc'))  # miss

print(re.search(r'a{3}bc', 'aaabc'))
print(re.search(r'a{3}bc', 'aabc'))
print(re.search(r'a{3}bc', 'aaaabc'))

print(re.search(r'a{2,3}bc', 'aabc'))
print(re.search(r'a{2,3}bc', 'aaabc'))
print(re.search(r'a{2,3}bc', 'abc'))  # miss
print(re.search(r'a{2,3}bc', 'aaaabc'))
print(re.search(r'^a{2,3}bc', 'aaaabc'))  # miss

print(re.search(r'a{2,}bc', 'aabc'))
print(re.search(r'a{2,}bc', 'aaaaabc'))
print(re.search(r'a{2,}bc', 'abc'))  # miss
print(re.search(r'^a{2,}bc', 'aaaaabc'))

print(re.search(r'a{,2}bc', 'bc'))
print(re.search(r'a{,2}bc', 'abc'))
print(re.search(r'a{,2}bc', 'aabc'))
print(re.search(r'a{,2}bc', 'aaabc'))
print(re.search(r'^a{,2}bc', 'aaabc'))

# 文字集合
# 何れか いずれか  []
print('[]----------------')
print(re.search(r'[abc]bc', 'abc'))
print(re.search(r'[abc]bc', 'bbc'))
print(re.search(r'[abc]bc', 'cbc'))
print(re.search(r'[abc]bc', 'dbc'))  # miss
print(re.search(r'[abc]bc', 'bc'))  # miss

print(re.search(r'[0123456789]', '5'))
print(re.search(r'[0123456789]', 'a'))  # miss
print(re.search(r'[0123456789]', 'AA5'))
print(re.search(r'[0123456789]', '５'))  # miss
print(re.search(r'[0123456789６]', '６'))
# []内の「ー」は範囲を示す特殊文字
print(re.search(r'[0-9]', '5'))
print(re.search(r'[a-z]', 'c'))
print(re.search(r'[a-zA-Z]', 'Y'))










