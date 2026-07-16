"""診断ロジック(ルールベース。AI は使わない)。

models.py とは別クラスに切る。ルールは「(判定関数, メッセージ)」のリストで
定義し、行を1つ足すだけでルールを追加できる構造にする。
判定に必要な数値が未入力(None)のルールは自動でスキップする。
"""


class Diagnosis:
    """1人の Fighter に対して該当する傾向コメントを返す。"""

    # ルール定義。cond は Fighter を受け取り真偽を返す関数。
    # None が絡む比較で落ちないよう、値の取り出しは _num() を通す。
    RULES = [
        (
            lambda f: Diagnosis._num(f.throw_received)
            > Diagnosis._num(f.throw_landed) * 1.5,
            "投げ受けが多い。投げ抜けが課題",
        ),
        (
            lambda f: Diagnosis._num(f.cornered_sec)
            > Diagnosis._num(f.cornering_sec) * 2,
            "壁際に追い込まれやすい",
        ),
        (
            lambda f: Diagnosis._num(f.di_received)
            > Diagnosis._num(f.di_landed) * 2,
            "DIを受ける回数が多い",
        ),
        (
            lambda f: Diagnosis._num(f.just_parry) < 0.5,
            "ジャストパリィの精度に伸びしろ",
        ),
        (
            lambda f: Diagnosis._num(f.damage_pct) > 50,
            "ドライブゲージをダメージに使う割合が高い",
        ),
    ]

    # 各ルールが参照する列(どれか一つでも None なら評価をスキップするため)
    RULE_FIELDS = [
        ("throw_received", "throw_landed"),
        ("cornered_sec", "cornering_sec"),
        ("di_received", "di_landed"),
        ("just_parry",),
        ("damage_pct",),
    ]

    def __init__(self, fighter):
        self.fighter = fighter

    @staticmethod
    def _num(v):
        return v if v is not None else 0

    def results(self):
        """該当したコメントの文字列リストを返す。"""
        messages = []
        for (cond, msg), fields in zip(self.RULES, self.RULE_FIELDS):
            # ルールが必要とする列がすべて入力済みのときだけ評価する
            if any(getattr(self.fighter, col) is None for col in fields):
                continue
            if cond(self.fighter):
                messages.append(msg)
        return messages

    def summary(self):
        """一覧カード用の短い要約(1件だけ or 「特筆なし」)。"""
        r = self.results()
        if not r:
            return "特筆すべき傾向なし"
        if len(r) == 1:
            return r[0]
        return f"{r[0]} 他{len(r) - 1}件"
