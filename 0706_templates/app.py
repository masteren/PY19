# テンプレートエンジン
#  HTMLを中心に、動的なページを作成する仕組み。
#  Flaskでは、Jinja2というテンプレートエンジンを利用。
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Jinja2経由にて、テンプレートファイルを読み込み、返却する。
    return  render_template('index.html')

# テンプレート(HTML)ファイルは、「templates」フォルダに配置する必要がある。
# MVTモデル
#  M(Model)…業務ロジックを担当
#  V(View)…入力を受け取り、ModelとTemplateの制御を担当
#  T(Template)…入出力画面を担当
# ちなみに、当ファイルはVになる。
# おまけ。MVCと対応すると、V=C, T=Vになる。

# View(app.py)から、テンプレートファイルに、データを受け渡すことができる。
@app.route('/pass_data')
def pass_data():
    from user import User
    user = User(456, 'def')

    # 第2引数以降にキーワード引数で受け渡す。
    return render_template('pass_data.html', id=123, name='<h1>abc</h1>', user=user)

if __name__ == '__main__':
    app.run('0.0.0.0', 5005, debug= True)

