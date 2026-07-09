from flask import Flask

app = Flask(__name__)

@app.route('/')
# ※先頭の/は必須（ルート）
# このURLに対応する処理を
# 関数で定義する。
# 関数名はなんでもOK。(URLと不一致でもOK)
# ただし、ダブりはないこと。
def index():
    return  'hello'

# @app.route('/index2')
# def index():
#     return  'hello'
# ダブりはないこと。

# エンドポイント
# URLに紐づいた処理をエンドポイントと言う。
# 既定では関数名がエンドポイント名となる。
# 主に後述のurl_forにて利用する。
# また、app.routeで指定したURLのことをルール(rule)と言う。
# flask routes コマンドで確認可能
# ※app.pyが存在するディレクトリにて実行すること。

# エンドポイント名の変更
@app.route('/a', endpoint='b')
def a():
    return 'a'

# endpointを付与すれば、関数名のダブルOK
@app.route('/c', endpoint='c')
def a():
    return 'c'

# endpointは、関数名のダブり他、関数名が長い場合や、
# 関数の命名規則とURLの命名規則を変えたい場合に用いる。

if __name__ == '__main__':
    app.run('0.0.0.0', 5005, debug= True)

