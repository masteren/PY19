# SQL インジェクション
#  SQL文の命令を埋め込み、意図しないSQLが実行される手法。
#  この有害なSQLを無害化することをサニタイジングという。
import sqlite3

id = 1
name = "Alice"

# インジェクション
inj_id = '1 OR 1=1--'
inj_name = ''

# よくない場合
with sqlite3.connect('0618_basic_db/sample.db') as conn:

    # カーソルを取得する。
    cursor = conn.cursor()

    # 文字列に直接埋め込んでいるので、'1 OR 1=1--' で全件ヒットしてしまう
    cursor.execute(f"SELECT COUNT(*) FROM user WHERE id = {inj_id} AND name = '{inj_name}'")
    count, = cursor.fetchone()
    print(count)

# いい場合
with sqlite3.connect('0618_basic_db/sample.db') as conn:

    # カーソルを取得する。
    cursor = conn.cursor()

    # プレースホルダーと呼ばれる機能を使う
    # サニタイジング
    sql = "SELECT COUNT(*) FROM user WHERE id=? AND name=?"

    # executeの第2引数にタプルで値を渡す
    cursor.execute(sql, (inj_id, inj_name))
    count, = cursor.fetchone()
    print(count)

    # ?ではなく、:を使った名前指定バージョンもある。
    sql = "SELECT COUNT(*) FROM user WHERE id=:id AND name=:name"

    # executeの第2引数に辞書で値を渡す
    cursor.execute(sql, {'name':name, 'id':id})
    count, = cursor.fetchone()
    print(count)

