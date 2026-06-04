# Member
#  物が持っている特性のこと。
# 以下２つがある。
#  属性 … アトリビュート。※他言語ではフィールドやプロパティとも言う。
#         その物が持つ、データのこと。※名詞
#  振る舞い … メソッド。
#         その物が持つ、処理のこと。※動詞

# 振る舞い(メソッド)
# [定義書式]
# def メソッド名(self [, 引数[, 引数…]]):
class User:
    def hello(self):
        print("hello")

# メソッド呼び出し
# [呼び出し書式]
#  インスタンス.メソッド名()

# インスタンス化
word = User()
word.hello()

# メソッド(≒関数)呼び出しは、
# 「括弧」が必要！
# メソッド呼び出し時、定義側のselfは
# 気にしない。（selfは勝手に渡る。）

# 引数

class User:
    # 第１引数はselfとする慣例。
    # 第2引数以降は、呼び出し側で渡す引数。
    def hello(self, name="nanashi"):
        print(f'hello {name}')


user = User()
user.hello()

# 戻り値
class User:
    def hello(self):
        print("hello")
    def hello2(self):
        return "hello"
# メソッドは、複数定義できる。

user = User()
result = user.hello()  # helloと表示されるが、戻り値はNone
print(result)  # Noneと表示される

result = user.hello2()
print(result)

# 同一メソッドの定義は後ほどのものが有効になる。
class User:
    def hello(self):
        print("hello")
    def hello(self):
        print("2o")

User().hello()
# 変数に入れず、直に操作することもできる。
