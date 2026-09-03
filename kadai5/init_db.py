# データベース構築用スクリプト
#  schema.sql でテーブルを作り、seed.sql でデモデータを登録する。
#  アプリを動かす前に、1回だけ実行する。
#   py init_db.py
#  ※実行するたびにテーブルを作り直す(schema.sqlのDROP TABLE)ので、
#   登録したデータは消える。
import sqlite3

# DBファイル名は fighter_dao.py で決めているものを使う(二重に書かない)
from fighter_dao import DB_NAME

with sqlite3.connect(DB_NAME) as conn:

    # SQLファイルの中身を読み込む
    with open('schema.sql', encoding='utf-8') as file:
        sql = file.read()
    # executescript は「;」で区切られた複数のSQL文をまとめて実行する
    conn.executescript(sql)
    print('schema.sql を実行しました(テーブル作成)')

    with open('seed.sql', encoding='utf-8') as file:
        sql = file.read()
    conn.executescript(sql)
    print('seed.sql を実行しました(デモデータ20件)')

    conn.commit()

print(DB_NAME + ' を作成しました')
