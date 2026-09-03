# SF6 ファイターカルテ
#  ルーティング(View)を担当するファイル。
#  MVTモデルのV。SQLはfighter_dao.py、入力チェックはvalidator.py、
#  診断はdiagnosis.pyに分けているため、ここにはSQLを書かない。
from flask import Flask, render_template, request, redirect, url_for

from fighter_dao import FighterDAO
from validator import (FighterValidator, MAIN_CHARS, RANK_NAMES, LABELS,
                       GAUGE_COLUMNS, COUNT_COLUMNS, WALL_COLUMNS)
from diagnosis import Diagnosis

app = Flask(__name__)

dao = FighterDAO()


# 登録・編集フォームを表示する。
# 新規/編集、GET/エラー時 のどの場合も渡すデータが同じなので関数にまとめる。
#  mode  : 'new' か 'edit'
#  f     : フォームに表示する値(Fighter または dict)
#  errors: エラーメッセージのdict
def show_form(mode, f, errors, status_code=200):
    html = render_template('form.html',
                           mode=mode,
                           f=f,
                           errors=errors,
                           main_chars=MAIN_CHARS,
                           rank_names=RANK_NAMES,
                           labels=LABELS,
                           gauge_columns=GAUGE_COLUMNS,
                           count_columns=COUNT_COLUMNS,
                           wall_columns=WALL_COLUMNS)
    return html, status_code


# --- 一覧画面 --------------------------------------------------------------
@app.route('/')
def index():
    fighters = dao.find_all()

    # 1人ずつ診断して、(Fighter, 要約コメント) のリストを作る
    cards = []
    for fighter in fighters:
        diagnosis = Diagnosis(fighter)
        cards.append((fighter, diagnosis.summary()))

    return render_template('index.html', cards=cards)


# --- 詳細画面 --------------------------------------------------------------
@app.route('/fighter/<int:fighter_id>')
def detail(fighter_id):
    fighter = dao.find_by_id(fighter_id)
    if fighter is None:
        return '該当するプレイヤーが見つかりません', 404

    diagnosis = Diagnosis(fighter)
    return render_template('detail.html',
                           f=fighter,
                           messages=diagnosis.results())


# --- 新規登録(INSERT) ------------------------------------------------------
@app.route('/fighter/new', methods=['get', 'post'])
def create():
    if request.method == 'POST':
        validator = FighterValidator(request.form)
        clean, errors = validator.validate()

        if errors:
            # 入力した内容を残したままフォームに戻す
            return show_form('new', clean, errors, 400)

        new_id = dao.insert(clean)
        # 登録後はリダイレクトする(再読み込みでの二重登録を防ぐ)
        return redirect(url_for('detail', fighter_id=new_id))

    # GET のときは空のフォームを表示する
    return show_form('new', {}, {})


# --- 編集(UPDATE) ----------------------------------------------------------
@app.route('/fighter/<int:fighter_id>/edit', methods=['get', 'post'])
def edit(fighter_id):
    fighter = dao.find_by_id(fighter_id)
    if fighter is None:
        return '該当するプレイヤーが見つかりません', 404

    if request.method == 'POST':
        validator = FighterValidator(request.form)
        clean, errors = validator.validate()

        if errors:
            # フォームの action にidが必要なので入れておく
            clean['id'] = fighter_id
            return show_form('edit', clean, errors, 400)

        dao.update(fighter_id, clean)
        return redirect(url_for('detail', fighter_id=fighter_id))

    # GET のときは今の値を入れたフォームを表示する
    return show_form('edit', fighter, {})


# --- 削除(DELETE) ----------------------------------------------------------
# POSTでのみ受け付ける(URLを開いただけでデータが消えないようにするため)
@app.route('/fighter/<int:fighter_id>/delete', methods=['post'])
def delete(fighter_id):
    # 存在しないIDならDELETEせずに404を返す
    if dao.find_by_id(fighter_id) is None:
        return '該当するプレイヤーが見つかりません', 404

    dao.delete(fighter_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0', 5005, debug=True)
