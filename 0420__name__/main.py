# __name__ 自動で作成される変数。
# その値は、呼び出される方法によって異なる。
# ①実行ファイルとして読み込まれた。
# 　例）py main.py
# ②モジュールとして読み込まれた。
# 　例）import my_module

# ①実行ファイルとして読み込まれた。
#  → __name__ == '__main__'
print(__name__)

import my_module
