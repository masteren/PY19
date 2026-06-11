# カプセル化
#  オブジェクト指向３大要素の内の一つ。
# 次の２つの意味合いがある。
# ①属性と振る舞いを一つのまとまりとして管理することができる。
#  例）属性としてidとnameがあり、振る舞いとしてhelloがある。
#     これらをまとめてUserとする。
#  ※おまけ：オブジェクト指向でない場合、データと処理は分離される。
# ②メンバ(アトリビュート＆メソッド)を隠蔽する。

# [隠蔽書式]
#  各々の定義名称の開始をアンダーバー２つとする。
#  例）アトリビュート → __アトリビュート名
#      メソッド → __メソッド名

class User:
    def __init__(self):
        self.id = 0
        self.name = '名無し'
        self.__age = 99
        self.__address = '不明'
    def a(self):
        print(self.__age)
        print(self.__b)
    def __b(self):
        print('b')

user = User()
print(user.id)  # 0
print(user.name)  # '名無し'
# print(user.__age)  # AttributeError: 'User' object has no attribute '__age'
user.a()  # 99

# おまけ。
# 一般的な言語には情報の公開範囲を制御するアクセス修飾子なるものが存在する。
# 例）public…外部公開 private…外部非公開
# ※pythonには無い。

# おまけ
# Double underscoreを略してDunder(ダンダー)と言う。

# ポイント
# 　極力隠蔽し、不必要な情報を外部に公開しないこと。
# 　　→保守性向上
