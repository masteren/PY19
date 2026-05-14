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

print(re.search(r'\d', '5')) # [0-9 ０-９]と同義
print(re.search(r'\d', '４'))
print(re.search(r'\d', 'a')) # miss

print(re.search(r'\D', '＠')) # 数字以外
print(re.search(r'\D', '5')) # miss

print(re.search(r'\s', '@')) # 空白文字（スペース、タブ、改行など）
print(re.search(r'\s', ' ')) # match
print(re.search(r'\s', '\t')) # match
print(re.search(r'\s', '\n')) # match


print(re.search(r'\S', ' ')) # miss
print(re.search(r'\S', '@')) # match

print(re.search(r'\bis\b', 'this is')) # \bで単語区切り
print(re.search(r'\bis\b', 'this')) # miss

# 単語選択
# (abc|def)   abcかdefのどちらか
print(re.search(r'(abc|def)g', 'abcg')) # match
print(re.search(r'(color|colour)', 'color'))

# グループ
# ()で括ってグループ化することにより、
# .groupや、.groupsで取得可能
print('group/groups')
print(re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})', '2026/5/7'))
match = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})', '2026/5/7')
print(match)
print(match.group(0)) # マッチ全体
print(match.group(1)) # 1番目のグループ
print(match.group(2)) # 2番目のグループ
print(match.group(3)) # 3番目のグループ
print(match.groups()) # 全てのグループをタプルで取得

# 打ち消しは [\]
print(re.search(r'\^', 'a'))
print(re.search(r'\^', 'a^')) # match
print(re.search(r'\$', 'a$')) # match
print(re.search(r'\.', 'a.')) # match
print(re.search(r'\{', 'a{')) # match
print(re.search(r'\(', 'a(')) # match
print(re.search(r'\\', '\\')) # match
print(re.search(r'[0\-9]', '-')) # 0,-,9のいずれか
print(re.search(r'[^abc]bc', 'dbc')) # [^]は否定の文字集合
print(re.search(r'[^abc]bc', 'bc')) # miss

# 最短一致
# +?...手前の文字が1回以上繰り返すが、できるだけ少ない回数でマッチする
# *?...手前の文字が0回以上繰り返すが、できるだけ少ない回数でマッチする
print('+?*?----------------')
print(re.search(r'.+', 'abc'))
print(re.search(r'.+?', 'abc'))
print(re.search(r'.*', 'abc'))
print(re.search(r'.*?', 'abc'))
print(re.search(r'aaa.*ccc', 'aaabbbcccdddccc'))
print(re.search(r'aaa.*?ccc', 'aaabbbcccdddccc'))

# マッチオブジェクト
print('match object----------------')
match = re.search(r'ccc', 'abccc')
print(match.span())
print(match.start())
print(match.end())
# searchは複数箇所マッチしない
match = re.search(r'ccc', 'abcccabccc')
print(match.span())

# 複数マッチ　findall
print('findall----------------')
match_str_list = re.findall(r'ccc', 'abcccabccc')
print(match_str_list)

# 複数マッチ　finditer イテレータで返す
print('finditer----------------')
match_iter = re.finditer(r'ccc', 'abcccabccc')
for match in match_iter:
    print(match.span())

# かぶりは考慮されない
match_iter = re.finditer(r'ccc', 'abcccccc')
for match in match_iter:
    print(match.span())

# マッチした箇所で区切ってリスト化
print('split----------------')
split_list = re.split(r'ccc', 'abcccabccc')
print(split_list)

# マッチした箇所を置換
print('sub----------------')
print(re.sub(r'ccc', 'XXX', 'abcccabccc'))

# 先読み／後読み
# (?= ) … 先読み
# (?! ) … 否定先読み
# (?<= ) … 後読み
# (?<! ) … 否定後読み
# 先頭を表す^や、末尾を表す$と同じ扱い。
# パターンマッチング(検査)はするが、
# 結果のマッチオブジェクトには含まれない。

# 先読み（右側をチェック）
print(re.search(r'python(?=flask)', 'pythonflask'))
print(re.search(r'python(?=flask)', 'pythonflas')) # miss

# 否定先読み（右側をチェック）
print(re.search(r'python(?!flask)', 'pythonflask')) # miss
print(re.search(r'python(?!flask)', 'pythonflas')) # match

# 後読み（左側をチェック）
print(re.search(r'(?<=python)flask', 'pythonflask')) # match
print(re.search(r'(?<=python)flask', 'pythoflask'))

# 否定後読み（左側をチェック）
print(re.search(r'(?<!python)flask', 'pythonflask')) # miss
print(re.search(r'(?<!python)flask', 'pythoflask'))

# 先読み/後読み + グループ
print(re.search(r'新宿(?=駅|区)', '新宿駅 '))
print(re.search(r'新宿(?=駅|区)', '新宿区 '))
print(re.search(r'新宿(?=駅|区)', '新宿町 ')) # miss

print(re.search(r'新宿(?=駅|御苑)', '新宿駅 '))
print(re.search(r'新宿(?=駅|御苑)', '新宿御苑 '))

print(re.search(r'(?<=(西|東))新宿', '西新宿 '))
# print(re.search(r'(?<=(東|東部))新宿', '東新宿 ')) # bug

# 先読み/後読み 活用例1
print(re.sub(r'日本(?=語)', '国', '日本では日本語と英語を勉強する。'))

# 先読み/後読み 活用例2 タグ取得
print(re.findall(r'(?<=#)\S+', '#aaa #bbb #ccc'))

# 先読みの手前(左)記載
print(re.search(r'(?=pythonflask)python', 'pythonflask'))
print(re.search(r'(?=pythonflask)python', 'flask')) # miss
print(re.search(r'(?=pythonflask)python', 'python')) # miss
print(re.search(r'(?=pythonflask)python', 'pythonflask'))

print(re.search(r'(?<=pythonflask)a', 'pythonflaska'))

# →あらかじめ、先読み指定パターンが存在することをチェックし、
#  存在した場合、右側のパターンを、存在した場所の先頭からチェックする。
# 後読みの場合、存在した場所の"先頭から"、にならない。
# 存在した場所より"右側から"、となる。

# 先読み/後読み 活用例3
# 任意条件今回は３数字に加え、英大文字が含まれていること。
print(re.search(r'(?=.*[A-Z]).{3}', 'Abc')) # match
print(re.search(r'(?=.*[A-Z]).{3}', 'aBc')) # match
print(re.search(r'(?=.*[A-Z]).{3}', 'abC')) # match
print(re.search(r'(?=.*[A-Z]).{3}', 'abc')) # miss
print(re.search(r'(?=.*[A-Z]).{3}', 'aB')) # miss

# 先読みを連続した場合、AND条件になる。
# 任意条件今回は３数字に加え、英小文字と英大文字が含まれていること。
print(re.search(r'(?=.*[a-z])(?=.*[A-Z]).{3}', 'Abc')) # match
print(re.search(r'(?=.*[a-z])(?=.*[A-Z]).{3}', 'AAA')) # miss
print(re.search(r'(?=.*[a-z])(?=.*[A-Z]).{3}', 'abc')) # miss

# 先読み/後読み 活用例4 パスワード
# 少なくとも５桁必要
# 小文字、大文字、数字、記号(.)の全てを含む
print(re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.])[a-zA-Z0-9_.]\S{5,}$', 'Password123!')) # match
