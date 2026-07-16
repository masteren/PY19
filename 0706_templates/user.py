# データクラス
#  データを保持するだけのクラス。
#  データの受け渡しがシンプルになり、
#  保守性が向上する。
class User:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

    # プロパティ(ゲッター)定義
    # これにより、.idにてidデータを
    # 取得することが出来るようになる。
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
