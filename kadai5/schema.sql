-- ファイターカルテ: テーブル定義
-- SQLite3。マスタ(fighters) 1テーブル構成。
-- バトル傾向の数値は「過去100戦平均」のスナップショットとして
-- プレイヤー本体と1:1で持つため、あえて別テーブルに分けない。

DROP TABLE IF EXISTS fighters;

CREATE TABLE fighters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 基本情報
    name            TEXT NOT NULL,      -- 多言語・記号あり。長さのみアプリ側で検証(1〜32)
    cfn_code        TEXT,               -- 任意。^\d{10}$ をアプリ側で検証
    main_char       TEXT NOT NULL,      -- ホワイトリスト検証(validators.py)
    rank_name       TEXT,               -- ホワイトリスト検証
    lp              INTEGER,            -- 0〜50000

    -- ドライブゲージ使用実績(%。小数2桁。7項目の合計≒100をアプリ側で相関チェック)
    parry_pct       REAL,
    di_pct          REAL,
    od_arts_pct     REAL,
    parry_rush_pct  REAL,
    cancel_rush_pct REAL,
    reversal_pct    REAL,
    damage_pct      REAL,

    -- 回数系(過去100戦平均。小数1桁。0〜99.9)
    throw_landed    REAL,
    throw_received  REAL,
    di_landed       REAL,
    di_received     REAL,
    just_parry      REAL,

    -- 壁際(秒。小数1桁。0〜99.9)
    cornering_sec   REAL,
    cornered_sec    REAL,

    note            TEXT,               -- 任意メモ(相手の癖など)
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
