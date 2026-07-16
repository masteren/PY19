"""ルーティングのみ。SQL は models.py、検証は validators.py、
診断は diagnosis.py に委譲し、ここには SQL を一切書かない。
"""
import uuid
from pathlib import Path

from flask import (
    Flask, render_template, request, redirect, url_for, flash, abort,
)

from models import FighterRepository
from validators import (
    validate_fighter, MAIN_CHARS, RANK_NAMES, LABELS,
)
from diagnosis import Diagnosis

app = Flask(__name__)
app.secret_key = "sf6-fighter-karte-dev-key"  # flash 用(デモ用途)

# アップロード保存先(static/uploads)。
UPLOAD_DIR = Path(app.root_path) / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

repo = FighterRepository()

# 画像の許可拡張子とマジックナンバー(先頭バイト)。両方を検証する。
ALLOWED_EXT = {"jpg", "jpeg", "png", "gif"}
MAGIC_NUMBERS = {
    b"\xff\xd8\xff": "jpg",          # JPEG
    b"\x89PNG\r\n\x1a\n": "png",     # PNG
    b"GIF87a": "gif",
    b"GIF89a": "gif",
}


def _detect_image_type(head):
    """先頭バイト列から画像種別を返す。未知なら None。"""
    for magic, kind in MAGIC_NUMBERS.items():
        if head.startswith(magic):
            return kind
    return None


def _save_upload(file_storage):
    """アップロード画像を検証して保存し、(保存ファイル名 or None, error)。

    拡張子とマジックナンバーの両方を検証。uuid でリネームして保存する。
    """
    if not file_storage or not file_storage.filename:
        return None, None  # 画像なしは正常

    name = file_storage.filename
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext == "jpeg":
        ext = "jpg"
    if ext not in ALLOWED_EXT:
        return None, "画像は jpg / png / gif のみ対応です"

    head = file_storage.stream.read(16)
    file_storage.stream.seek(0)
    kind = _detect_image_type(head)
    if kind is None:
        return None, "画像ファイルとして不正です(中身が画像ではありません)"

    # uuid でリネーム(元名は保存しない)。DB にはこのファイル名のみ入れる。
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_storage.save(UPLOAD_DIR / filename)
    return filename, None


def _delete_file(filename):
    """アップロード画像を物理削除(存在すれば)。"""
    if not filename:
        return
    path = UPLOAD_DIR / filename
    if path.exists():
        path.unlink()


# --- 一覧 -------------------------------------------------------------------
@app.route("/")
def index():
    # 絞り込み・並び替えは GET パラメータ(JS 不使用)
    main_char = request.args.get("main_char") or None
    rank_name = request.args.get("rank_name") or None
    order_by = request.args.get("order", "created")

    fighters = repo.find_all(
        main_char=main_char, rank_name=rank_name, order_by=order_by,
    )
    # 各カードの診断要約を作る
    cards = [(f, Diagnosis(f).summary()) for f in fighters]

    return render_template(
        "index.html",
        cards=cards,
        main_chars=MAIN_CHARS,
        rank_names=RANK_NAMES,
        cur_main=main_char, cur_rank=rank_name, cur_order=order_by,
    )


# --- 詳細 -------------------------------------------------------------------
@app.route("/fighter/<int:fighter_id>")
def detail(fighter_id):
    fighter = repo.find_by_id(fighter_id)
    if fighter is None:
        abort(404)
    return render_template(
        "detail.html",
        f=fighter,
        diagnosis=Diagnosis(fighter).results(),
    )


# --- 新規登録 ---------------------------------------------------------------
@app.route("/fighter/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        clean, errors = validate_fighter(request.form)

        # 画像処理(検証OKでも失敗し得るのでエラーに合流)
        filename, img_err = _save_upload(request.files.get("screenshot"))
        if img_err:
            errors["screenshot"] = img_err

        if errors:
            # 他項目のエラーで差し戻す場合、保存済みの画像は孤児ファイルになるため削除
            _delete_file(filename)
            # リダイレクトせず入力値を保持したままフォームに戻す
            return render_template(
                "form.html", mode="new", f=clean, errors=errors,
                main_chars=MAIN_CHARS, rank_names=RANK_NAMES, labels=LABELS,
            ), 400

        clean["screenshot"] = filename
        new_id = repo.create(clean)
        flash("登録しました", "success")
        return redirect(url_for("detail", fighter_id=new_id))  # PRG

    # GET: 空フォーム
    return render_template(
        "form.html", mode="new", f={}, errors={},
        main_chars=MAIN_CHARS, rank_names=RANK_NAMES, labels=LABELS,
    )


# --- 編集 -------------------------------------------------------------------
@app.route("/fighter/<int:fighter_id>/edit", methods=["GET", "POST"])
def edit(fighter_id):
    fighter = repo.find_by_id(fighter_id)
    if fighter is None:
        abort(404)

    if request.method == "POST":
        clean, errors = validate_fighter(request.form)

        new_filename, img_err = _save_upload(request.files.get("screenshot"))
        if img_err:
            errors["screenshot"] = img_err

        if errors:
            # 他項目のエラーで差し戻す場合、保存済みの新画像は孤児ファイルになるため削除
            _delete_file(new_filename)
            # 既存の画像名は保持して表示(未確定の new_filename は使わない)
            clean["screenshot"] = fighter.screenshot
            clean["id"] = fighter_id
            return render_template(
                "form.html", mode="edit", f=clean, errors=errors,
                main_chars=MAIN_CHARS, rank_names=RANK_NAMES, labels=LABELS,
            ), 400

        # チェックボックス「画像を削除する」が ON か
        remove_image = request.form.get("remove_screenshot") == "1"

        if new_filename:
            # 画像差し替え: 新規保存に成功したので古いファイルを物理削除
            old = fighter.screenshot
            clean["screenshot"] = new_filename
            repo.update(fighter_id, clean)
            _delete_file(old)
        elif remove_image:
            # 画像だけ削除(レコードは残す): DB を先に NULL 化 → ファイル物理削除
            old = fighter.screenshot
            clean["screenshot"] = None
            repo.update(fighter_id, clean)
            _delete_file(old)
        else:
            clean["screenshot"] = fighter.screenshot  # 変更なし
            repo.update(fighter_id, clean)

        flash("更新しました", "success")
        return redirect(url_for("detail", fighter_id=fighter_id))  # PRG

    # GET: 既存値でフォームを埋める
    return render_template(
        "form.html", mode="edit", f=fighter, errors={},
        main_chars=MAIN_CHARS, rank_names=RANK_NAMES, labels=LABELS,
    )


# --- 削除(POST のみ。GET でのデータ破壊は不可) ----------------------------
@app.route("/fighter/<int:fighter_id>/delete", methods=["POST"])
def delete(fighter_id):
    fighter = repo.find_by_id(fighter_id)
    if fighter is None:
        abort(404)
    # 削除順は DB → ファイル(逆だと整合性が壊れる)
    repo.delete(fighter_id)
    _delete_file(fighter.screenshot)
    flash("削除しました", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # 初回のみ: DB が無ければ schema + seed(デモ100件)を投入して作成
    if not repo.db_path.exists():
        repo.init_db()
    # macOS では 5000 番を AirPlay Receiver が使うため 5001 番で起動
    app.run(debug=True, port=5001)
