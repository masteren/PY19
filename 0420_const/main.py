import my_module
import my_module

# インポートされたモジュールすべてのメンバ(変数/関数/クラス)が使える。
print(my_module.a)
my_module.my_func()

# from を使っても同じように全てが実行される。
from my_module2 import my_func
my_func()

# 変数も読み込める
from my_module2 import a
print(a)
