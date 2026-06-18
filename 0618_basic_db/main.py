# SQLite
#  簡易RDB。
#  Android,macOS,Pythonではデフォルトで組み込まれている。
import sqlite3

# データベースに接続する。
# sqlite3.connect('sample.db')
conn = sqlite3.connect('0618_basic_db/sample.db')

# カーソルを取得する。
cursor = conn.cursor()

# SQL文を定義する。
sql = '''\
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING
)\
'''

# SQl実行は cursor.execute() を使用する。
cursor.execute(sql)

# commitで確定する。
conn.commit()

# DBを切断する。
conn.close()

# DBに接続する。 with構文を使用することで、withブロックを抜けると自動的に切断される。
with sqlite3.connect('0618_basic_db/sample.db') as conn:

    # カーソルを取得する。
    cursor = conn.cursor()

    # SQL文を定義する。
    sql = "INSERT INTO user(name) VALUES('Alice')"

    # SQl実行は cursor.execute() を使用する。
    cursor.execute(sql)

    # commitで確定する。
    # conn.commit()
    # rollbackでキャンセルする。
    conn.rollback()

    # データ取得は、execute後、cursorで結果を取得する。
    cursor.execute('SELECT * FROM user')
    for row in cursor:
        print(row)
    # selectはcommit/rollback不要
