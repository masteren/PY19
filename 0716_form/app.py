from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return  render_template('index.html')

# postを受け取るには、methodsの指定が必須。
@app.route('/confirm', methods=['post'])
def confirm():
    # Formデータは、request.formから取得する

    # 単一値の取得 方法その1
    id = request.form.get('id')
    print(id)

    # 取得できない場合はNone
    id2 = request.form.get('id2')
    print(id2)

    # Noneの場合の既定値設定も可能
    id3 = request.form.get('id3', default='def')
    print(id3)

    # ちゃんとしたチェック処理を作ってみると
    id4 = request.form.get('id4')
    if not id4:
        # エラー処理。こんかいは簡易処理
        print('id4は必須です。')

    # 単一値の取得 方法その2
    id = request.form['id']
    print(id)

    # この場合、存在しないと、エラー
    # id = request.form['id2']

    # 複数値の取得
    checks = request.form.getlist('check')
    print(checks)

    # 空チェック
    if not checks:
        print('１つもチェックされず。')
    # 存在しない場合は空のリスト
    checks2 = request.form.getlist('check2')
    print(checks2)

    return  render_template('confirm.html')

if __name__ == '__main__':
    app.run('0.0.0.0', 5005, debug= True)

