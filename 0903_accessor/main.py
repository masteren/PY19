# アクセッサ
#  private(外部非公開)アトリビュートに
#  アクセスする専用のメソッド。
#  取得するメソッドをゲッター(getter)。
#  設定するメソッドをセッター(setter)という。
class User:
    def __init__(self):
        self.__id = 10000
        self.__name = 'a'

    # ゲッター
    def get_id(self):
        return self.__id

    #　セッター
    def set_id(self, id):
        self.__id = id

user = User()
# ゲッター経由で取得
print(user.get_id())

# セッター経由で設定
user.set_id(20000)
print(user.get_id())

# ゲッターのみ作成することにより、
# 読み取り専用とすることが可能。
# ※セッターのみの作成は無い。

# おまけ
# アクセッサの必要性
# オブジェクト指向のお作法として、
# アトリビュートはprivateにする。
# アクセスするにはアクセッサを用意する。

# アクセッサ、つまりメソッド化することにより、
# 以下の効能が生まれる。
# ①設定値のバリデーション(検証)を組み込むことができる。
# ②読み取り専用を実現することができる。
# ③内部的にアトリビュート名が後に変更されたとしても、
# 　公開されているのはアクセッサのメソッドのため、
# 　アクセッサ(メソッド)名の変更が掛からなければ、
#   利用サイドのプログラムに影響を及ぼさない。
# ④user.nama = の罠エラーに引っかからなくなる。

# プロパティ
#  アクセッサをメソッドの形式で
# 呼び出すのではなく、
#  アトリビュートの形式で
# 呼び出せる様にする仕組み。
#  デコレーターを使って、
# アクセッサを定義することで、
#  簡単にアクセスできる様になる。
class User:
    def __init__(self):
        self.__id = 10000
        self.__name = 'a'

    # ゲッター デコレータVer
    @property
    def id(self):
        return self.__id

    # セッター デコレータVer
    @id.setter
    def id(self, id):
        self.__id = id

user = User()
print(user.id)
user.id = 30000
