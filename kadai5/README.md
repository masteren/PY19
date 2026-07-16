# SF6 ファイターカルテ

ストリートファイター6 の「過去100戦平均のバトルの傾向」を手入力で記録し、
ルールベースで簡単な診断を出す Flask アプリ。

## 構成

| ファイル | 役割 |
| --- | --- |
| `app.py` | ルーティングのみ（SQL は書かない） |
| `models.py` | DB アクセス層（SQL はここに集約 / `Fighter`・`FighterRepository`） |
| `validators.py` | 入力バリデーション（必須・正規表現・ホワイトリスト・相関チェック） |
| `diagnosis.py` | 診断ロジック（ルールベース） |
| `schema.sql` | テーブル定義 |
| `seed.sql` | デモ用データ 100 件 |
| `templates/`, `static/` | 画面（CSS 手書き・JS 不使用） |

## セットアップと起動

```bash
# Flask が未インストールなら
pip install flask

# 起動（初回はDBが無ければ schema.sql + seed.sql から自動生成される）
cd kadai5
python app.py
```

ブラウザで <http://localhost:5001> を開く。
（macOS では 5000 番を AirPlay Receiver が使うため 5001 番で起動）

## メモ

- `fighters.db` と `static/uploads/` は Git 管理外。
  DB は初回起動時に自動生成され、`uploads/` も起動時に自動作成される。
- データを作り直したいときは `fighters.db` を削除して再起動すれば、
  `seed.sql` のデモ 100 件が入り直る。
- 画像アップロードは拡張子とマジックナンバー（先頭バイト）の両方を検証し、
  UUID でリネームして保存する。
