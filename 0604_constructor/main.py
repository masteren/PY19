# コンストラクタ
#  インスタンス化の際に動作するメソッド。
#  初期化の用途にて利用される。
# [定義書式]
# def __init__(self):
class User:
    def __init__(self):
        print("コンストラクタ動作")
User()

# コンストラクタは、インスタンス化の際に動作する。

# コンストラクタ＆引数
class User:
    def __init__(self, name):
        print(name)

User("abc")

# コンストラクタ＆戻り値
class User:
    def __init__(self):
        # コンストラクタは、実体を返すため、戻り値はNoneでなければならない。
        #return 0
        return None

user = User()
print(user)
