# FighterDAO クラス
#  DAO(Data Access Object) = DBアクセス専用のクラス。
#  SQLはすべてこのファイルに閉じ込め、app.pyからは
#  メソッド呼び出しだけを行う(オブジェクト指向設計)。
import sqlite3

from fighter import Fighter

DB_NAME = 'fighters.db'


class FighterDAO:

    def __init__(self, db_name=DB_NAME):
        self.__db_name = db_name

    # 一覧を取得する(登録が新しい順)
    def find_all(self):
        with sqlite3.connect(self.__db_name) as conn:
            cursor = conn.execute(
                'SELECT * FROM fighters ORDER BY created_at DESC, id DESC')
            rows = cursor.fetchall()

        # 取得した行(タプル)をFighterに詰め替えて返す
        fighters = []
        for row in rows:
            fighters.append(Fighter(row))
        return fighters

    # 1件を取得する。見つからなければ None を返す。
    def find_by_id(self, fighter_id):
        with sqlite3.connect(self.__db_name) as conn:
            # 値は必ずプレースホルダ(?)で渡す(SQLインジェクション対策)
            cursor = conn.execute(
                'SELECT * FROM fighters WHERE id = ?', (fighter_id,))
            row = cursor.fetchone()

        if row is None:
            return None
        return Fighter(row)

    # INSERTとUPDATEで渡す値は同じなので、1つのメソッドにまとめる。
    # 引数のdは validator.py が作ったdict。
    def __to_params(self, d):
        return (
            d['name'], d['cfn_code'], d['main_char'], d['rank_name'], d['lp'],
            d['parry_pct'], d['di_pct'], d['od_arts_pct'],
            d['parry_rush_pct'], d['cancel_rush_pct'],
            d['reversal_pct'], d['damage_pct'],
            d['throw_landed'], d['throw_received'],
            d['di_landed'], d['di_received'], d['just_parry'],
            d['cornering_sec'], d['cornered_sec'],
            d['note'],
        )

    # 新規登録(INSERT)。登録した行のidを返す。
    def insert(self, d):
        sql = '''\
            INSERT INTO fighters(
                name, cfn_code, main_char, rank_name, lp,
                parry_pct, di_pct, od_arts_pct, parry_rush_pct,
                cancel_rush_pct, reversal_pct, damage_pct,
                throw_landed, throw_received, di_landed, di_received,
                just_parry, cornering_sec, cornered_sec,
                note
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\
        '''
        with sqlite3.connect(self.__db_name) as conn:
            cursor = conn.execute(sql, self.__to_params(d))
            conn.commit()
            return cursor.lastrowid

    # 更新(UPDATE)
    def update(self, fighter_id, d):
        sql = '''\
            UPDATE fighters SET
                name = ?, cfn_code = ?, main_char = ?, rank_name = ?, lp = ?,
                parry_pct = ?, di_pct = ?, od_arts_pct = ?,
                parry_rush_pct = ?, cancel_rush_pct = ?,
                reversal_pct = ?, damage_pct = ?,
                throw_landed = ?, throw_received = ?,
                di_landed = ?, di_received = ?, just_parry = ?,
                cornering_sec = ?, cornered_sec = ?,
                note = ?
            WHERE id = ?\
        '''
        # 更新条件のidを、値のうしろに足す
        params = self.__to_params(d) + (fighter_id,)

        with sqlite3.connect(self.__db_name) as conn:
            conn.execute(sql, params)
            conn.commit()

    # 削除(DELETE)
    def delete(self, fighter_id):
        with sqlite3.connect(self.__db_name) as conn:
            conn.execute('DELETE FROM fighters WHERE id = ?', (fighter_id,))
            conn.commit()
