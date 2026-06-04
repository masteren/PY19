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
