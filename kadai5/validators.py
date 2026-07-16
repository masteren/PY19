"""入力バリデーション(すべて Python 側)。

JS でのチェックは禁止のため、フォームから来た生の文字列(request.form)を
ここで検証・型変換し、(clean:保存用dict, errors:項目名->メッセージ) を返す。

実装する4種類:
  1. 必須チェック      : name, main_char
  2. 正規表現          : cfn_code(^\\d{10}$)、数値系の桁数
  3. ホワイトリスト    : main_char, rank_name(POST改ざん対策でサーバー側集合チェック)
  4. 相関チェック      : ドライブゲージ7項目の合計 ≒ 100%(99.0〜101.0)
"""
import re

from models import EDITABLE_COLUMNS, DRIVE_GAUGE_COLUMNS

# --- ホワイトリスト定義 -----------------------------------------------------
# 使用可能キャラ(SF6)。セレクトの選択肢とサーバー検証で共用。
MAIN_CHARS = [
    "Ryu", "Ken", "Luke", "Jamie", "Chun-Li", "Guile", "Kimberly", "Juri",
    "Cammy", "Zangief", "Dee Jay", "Manon", "Marisa", "Lily", "JP", "Blanka",
    "Dhalsim", "E.Honda", "Rashid", "A.K.I.", "Ed", "Akuma", "M.Bison",
    "Terry", "Mai", "Elena", "Sagat",
]

# ランク(下位→上位)。空(未設定)も許容するため必須ではない。
RANK_NAMES = [
    "Rookie", "Iron", "Bronze", "Silver", "Gold",
    "Platinum", "Diamond", "Master", "Legend",
]

# --- 正規表現 ---------------------------------------------------------------
CFN_RE = re.compile(r"^\d{10}$")            # CFNコード: 数字ちょうど10桁
PCT_RE = re.compile(r"^\d{1,3}(\.\d{1,2})?$")  # %: 0〜100想定。小数2桁まで
# 回数・秒: 0〜99.9。整数1〜2桁 + 任意で小数1桁。
COUNT_RE = re.compile(r"^\d{1,2}(\.\d)?$")

# フィールドの日本語ラベル(エラー表示・テンプレート共用)
LABELS = {
    "name": "プレイヤー名", "cfn_code": "CFNコード", "main_char": "使用キャラ",
    "rank_name": "ランク", "lp": "LP",
    # ドライブゲージ使用実績(公式表記)
    "parry_pct": "ドライブパリィ%", "di_pct": "ドライブインパクト%",
    "od_arts_pct": "オーバードライブアーツ%",
    "parry_rush_pct": "パリィドライブラッシュ%",
    "cancel_rush_pct": "キャンセルドライブラッシュ%",
    "reversal_pct": "ドライブリバーサル%", "damage_pct": "ダメージ%",
    # 回数系(過去100戦平均)
    "throw_landed": "投げ 決めた回数", "throw_received": "投げ 受けた回数",
    "throw_escaped": "投げ抜け回数",
    "di_landed": "DI 決めた回数", "di_received": "DI 受けた回数",
    "parry_success": "ドライブパリィ成功回数", "just_parry": "ジャストパリィ回数",
    # 壁際(秒)
    "cornering_sec": "相手を追い詰めている時間", "cornered_sec": "相手に追い詰められている時間",
    "note": "メモ", "screenshot": "スクリーンショット",
}


def validate_fighter(form):
    """form: request.form(の様な mapping)。

    return: (clean, errors)
      clean : DB保存用 dict(型変換済み。EDITABLE_COLUMNS を網羅)
      errors: {列名: エラーメッセージ}。空なら検証OK。
    """
    errors = {}
    clean = {c: None for c in EDITABLE_COLUMNS}

    def get(key):
        return (form.get(key) or "").strip()

    # 1. 必須チェック + 長さ(name は 1〜32) ---------------------------------
    name = get("name")
    if not name:
        errors["name"] = f"{LABELS['name']}は必須です"
    elif len(name) > 32:
        errors["name"] = f"{LABELS['name']}は32文字以内です"
    clean["name"] = name

    # 2/3. main_char: 必須 + ホワイトリスト ---------------------------------
    main_char = get("main_char")
    if not main_char:
        errors["main_char"] = f"{LABELS['main_char']}は必須です"
    elif main_char not in MAIN_CHARS:
        # セレクト改ざん対策(サーバー側集合チェック)
        errors["main_char"] = f"{LABELS['main_char']}の値が不正です"
    clean["main_char"] = main_char

    # 3. rank_name: 任意 + ホワイトリスト -----------------------------------
    rank_name = get("rank_name")
    if rank_name and rank_name not in RANK_NAMES:
        errors["rank_name"] = f"{LABELS['rank_name']}の値が不正です"
    clean["rank_name"] = rank_name or None

    # 2. cfn_code: 任意 + 正規表現(^\d{10}$) --------------------------------
    cfn = get("cfn_code")
    if cfn:
        if not CFN_RE.match(cfn):
            errors["cfn_code"] = f"{LABELS['cfn_code']}は数字10桁で入力してください"
    clean["cfn_code"] = cfn or None

    # lp: 任意 + 範囲 0〜50000(整数) ----------------------------------------
    lp = get("lp")
    if lp:
        if not re.match(r"^\d{1,5}$", lp):
            errors["lp"] = f"{LABELS['lp']}は整数で入力してください"
        elif not (0 <= int(lp) <= 50000):
            errors["lp"] = f"{LABELS['lp']}は0〜50000の範囲です"
        else:
            clean["lp"] = int(lp)

    # 2. ドライブゲージ%(7項目): 空ならスキップ。桁数(PCT_RE)と範囲0〜100を確認。
    def check_pct(col):
        raw = get(col)
        if not raw:
            return                       # 未入力はOK(任意項目)
        if not PCT_RE.match(raw):
            errors[col] = f"{LABELS[col]}は小数2桁までの数値です"
        elif not (0 <= float(raw) <= 100):
            errors[col] = f"{LABELS[col]}は0〜100の範囲です"
        else:
            clean[col] = float(raw)      # OKなら数値に変換して保存

    check_pct("parry_pct")
    check_pct("di_pct")
    check_pct("od_arts_pct")
    check_pct("parry_rush_pct")
    check_pct("cancel_rush_pct")
    check_pct("reversal_pct")
    check_pct("damage_pct")

    # 2. 回数系・壁際: 空ならスキップ。桁数(COUNT_RE)と範囲0〜99.9を確認。
    def check_count(col):
        raw = get(col)
        if not raw:
            return
        if not COUNT_RE.match(raw):
            errors[col] = f"{LABELS[col]}は0〜99.9(小数1桁)で入力してください"
        elif not (0 <= float(raw) <= 99.9):
            errors[col] = f"{LABELS[col]}は0〜99.9の範囲です"
        else:
            clean[col] = float(raw)

    check_count("throw_landed")
    check_count("throw_received")
    check_count("throw_escaped")
    check_count("di_landed")
    check_count("di_received")
    check_count("parry_success")
    check_count("just_parry")
    check_count("cornering_sec")
    check_count("cornered_sec")

    # 4. 相関チェック: ドライブゲージ7項目の合計 ≒ 100% ---------------------
    # 目玉。単項目では正しくても合計が合わなければ不正とする(JSでは書きにくい)。
    # 対象列にひとつでもエラーがある場合は合計判定をスキップ(二重表示回避)。
    gauge_has_error = any(c in errors for c in DRIVE_GAUGE_COLUMNS)
    gauge_values = [clean[c] for c in DRIVE_GAUGE_COLUMNS if clean[c] is not None]
    if not gauge_has_error and gauge_values:
        total = sum(gauge_values)
        # 公式表示は四捨五入されるため 99.0〜101.0 を許容
        if not (99.0 <= total <= 101.0):
            errors["drive_gauge_total"] = (
                f"合計が {total:.2f}% です(100%になるはずです)"
            )

    # note / screenshot はここでは素通し(screenshot はファイル処理側で確定)
    clean["note"] = get("note") or None

    return clean, errors
