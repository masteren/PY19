#  属性 … アトリビュート。※他言語ではフィールドやプロパティとも言う。
#         その物が持つ、データのこと。※名詞
# [定義書式]
# def __init__(self):
#     コンストラクタで、selfを用いて定義していく。
#     self.アトリビュート名1 = 初期値
#     self.アトリビュート名2 = 初期値 ※必要数分記述OK

# self…自分。自身。自己。
# ということで、インスタンス化によって


class User:
    def __init__(self):
        self.id = 1
        self.name = "nanashi"
        self.age = 9
        address = "tokyo"  # self.をつけないと、ローカル変数になる。
# アトリビュート値の操作
# [利用書式]
#  インスタンス.アトリビュート名
user = User()
print(user.id)  # 1
print(user.name)  # nanashi
print(user.age)  # 9
# アトリビュート値の変更
user.id = 1
user.name = "tarou"

# 代入式で、外部から値の設定も可能。
user.id = 123
user.name = "hanako"
user.birthday = "2000-01-01"
print(user.id)  # 123
print(user.name)  # hanako
print(user.birthday)  # 2000-01-01

# アトリビュートはコンストラクタで定義が基本。
# でも、言語仕様的にはコンストラクタで無くても可。
# （保守性上、やらない方が良い）
class User:
    def a(self):
        self.id = 1
        self.name = "nanashi"
        self.birthday = "2000-01-01"
user = User()
# print(user.id)  # エラー。アトリビュートは定義されていない。
user.a()  # メソッドaを呼び出すと、アトリ
print(user.id)  # 1

# 外部からのアトリビュートの追加も可能。
user.age = 25
print(user.age)  # 25

# del文で、アトリビュートの削除も可能。
del user.age
# print(user.age)  # エラー。アトリビュートageは削除された。

# コンストラクタの引数にて初期化
class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

user1 = User(1, "nanashi")
user2 = User(2, "tarou")

# インスタンス毎に、アトリビュートは保持される。
print(user1.id, user1.name)  # 1 nanashi
print(user2.id, user2.name)  # 2 tarou

# 保存されているデータ(アトリビュート)は、
# 自分の持ち物なので、自分で使える。
# (自メソッドから操作可能。)
class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def show(self):
        print(f'{self.name}')
user = User(1, "nanashi")
user.show()  # nanashi

# アトリビュートの利用指針
#  その物が保持し続けるべきデータがある時のみ、
#  アトリビュートとする。
#  ※基本はローカル変数
