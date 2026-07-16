"""DB アクセス層。

SQL はすべてこのファイルに閉じ込め、app.py からは Fighter / FighterRepository
のメソッド呼び出しだけを行う(オブジェクト指向設計 / 加点要素)。
標準ライブラリ sqlite3 のみ。ORM は使わない。
"""
import sqlite3
from pathlib import Path

# このファイルからの相対でDBファイルを決める(実行ディレクトリに依存しない)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "fighters.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"

# フォームで扱う列(id と created_at 以外)。
# INSERT / UPDATE / Fighter でこの1つのリストを使い回し、列の書き漏れを防ぐ。
EDITABLE_COLUMNS = [
    "name", "cfn_code", "main_char", "rank_name", "lp",
    "parry_pct", "di_pct", "od_arts_pct", "parry_rush_pct",
    "cancel_rush_pct", "reversal_pct", "damage_pct",
    "throw_landed", "throw_received", "throw_escaped",
    "di_landed", "di_received", "parry_success", "just_parry",
    "cornering_sec", "cornered_sec",
    "note", "screenshot",
]

# ドライブゲージ使用実績7項目(相関チェック・横棒グラフで使う)
DRIVE_GAUGE_COLUMNS = [
    "parry_pct", "di_pct", "od_arts_pct", "parry_rush_pct",
    "cancel_rush_pct", "reversal_pct", "damage_pct",
]


class Fighter:
    """DB の1行(1プレイヤー)を表すクラス。

    SELECT で取れた行(sqlite3.Row)を受け取り、f.name のように
    属性でアクセスできるようにする。診断(diagnosis)やテンプレートで使う。
    """

    def __init__(self, row):
        # row(DBの1行)の各列を、同じ名前の属性に1つずつ入れていく。
        self.id = row["id"]
        # 基本情報
        self.name = row["name"]
        self.cfn_code = row["cfn_code"]
        self.main_char = row["main_char"]
        self.rank_name = row["rank_name"]
        self.lp = row["lp"]
        # ドライブゲージ使用実績(%)
        self.parry_pct = row["parry_pct"]
        self.di_pct = row["di_pct"]
        self.od_arts_pct = row["od_arts_pct"]
        self.parry_rush_pct = row["parry_rush_pct"]
        self.cancel_rush_pct = row["cancel_rush_pct"]
        self.reversal_pct = row["reversal_pct"]
        self.damage_pct = row["damage_pct"]
        # 回数系
        self.throw_landed = row["throw_landed"]
        self.throw_received = row["throw_received"]
        self.throw_escaped = row["throw_escaped"]
        self.di_landed = row["di_landed"]
        self.di_received = row["di_received"]
        self.parry_success = row["parry_success"]
        self.just_parry = row["just_parry"]
        # 壁際(秒)
        self.cornering_sec = row["cornering_sec"]
        self.cornered_sec = row["cornered_sec"]
        # その他
        self.note = row["note"]
        self.screenshot = row["screenshot"]
        self.created_at = row["created_at"]

    @property
    def drive_gauge_items(self):
        """横棒グラフ用: [(ラベル, 値), ...]。値が None のものは 0 扱い。"""
        # 公式(Buckler's Boot Camp)の表記に合わせる
        labels = {
            "parry_pct": "ドライブパリィ", "di_pct": "ドライブインパクト",
            "od_arts_pct": "オーバードライブアーツ",
            "parry_rush_pct": "パリィドライブラッシュ",
            "cancel_rush_pct": "キャンセルドライブラッシュ",
            "reversal_pct": "ドライブリバーサル", "damage_pct": "ダメージ",
        }
        return [(labels[c], getattr(self, c) or 0) for c in DRIVE_GAUGE_COLUMNS]


class FighterRepository:
    """fighters テーブルへの CRUD。SQL はここだけ。"""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    # --- 接続 ---
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 列名でアクセスできるように
        return conn

    def init_db(self, with_seed=True):
        """schema.sql でテーブルを作り、必要なら seed.sql でデモ100件を投入する。

        fighters.db は Git 管理外。初回起動時にこのメソッドで自動生成する。
        """
        with self._connect() as conn:
            conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
            if with_seed and SEED_PATH.exists():
                conn.executescript(SEED_PATH.read_text(encoding="utf-8"))

    # --- 参照 ---
    def find_all(self, main_char=None, rank_name=None, order_by="created"):
        """一覧。絞り込み(main_char/rank_name)と並び替えに対応。

        値は必ずプレースホルダで渡す。ORDER BY は列名を直接埋めるため、
        外部入力を渡さずホワイトリスト(下の map)で確定した文字列だけを使う。
        """
        order_map = {
            "lp": "lp DESC",           # LP順(強い順)
            "created": "created_at DESC, id DESC",  # 登録順(新しい順)
        }
        order_sql = order_map.get(order_by, order_map["created"])

        sql = "SELECT * FROM fighters"
        conditions = []
        params = []
        if main_char:
            conditions.append("main_char = ?")
            params.append(main_char)
        if rank_name:
            conditions.append("rank_name = ?")
            params.append(rank_name)
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY " + order_sql

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [Fighter(r) for r in rows]

    def find_by_id(self, fighter_id):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM fighters WHERE id = ?", (fighter_id,)
            ).fetchone()
        return Fighter(row) if row else None

    # --- 更新系 ---
    def create(self, values):
        """values: EDITABLE_COLUMNS をキーに持つ dict。新規IDを返す。"""
        cols = ", ".join(EDITABLE_COLUMNS)
        placeholders = ", ".join("?" for _ in EDITABLE_COLUMNS)
        params = [values.get(c) for c in EDITABLE_COLUMNS]
        sql = f"INSERT INTO fighters ({cols}) VALUES ({placeholders})"
        with self._connect() as conn:
            cur = conn.execute(sql, params)
            return cur.lastrowid

    def update(self, fighter_id, values):
        assignments = ", ".join(f"{c} = ?" for c in EDITABLE_COLUMNS)
        params = [values.get(c) for c in EDITABLE_COLUMNS]
        params.append(fighter_id)
        sql = f"UPDATE fighters SET {assignments} WHERE id = ?"
        with self._connect() as conn:
            conn.execute(sql, params)

    def delete(self, fighter_id):
        with self._connect() as conn:
            conn.execute("DELETE FROM fighters WHERE id = ?", (fighter_id,))
