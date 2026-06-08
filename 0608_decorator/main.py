# デコレーター
#  関数(メソッド)の前後に任意処理を追加することができる。

# 定義例）※一般的に以下の様に書くので覚える必要はない。
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # 前処理
        print(0)
        # 実関数呼び出し
        result = func(*args, **kwargs)

        # 後処理
        print(2)

        return result
    return wrapper

# [利用書式]
# @デコレーター名
# def 関数名():
#
# 利用例）
def a():
    print('1')

a()  # 1
print('---')
