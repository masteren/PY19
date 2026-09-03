# Diagnosis クラス
#  登録された数値から、そのプレイヤーの傾向コメントを作る。
#  AIは使わず、if文によるルールベースで判定する。
#  ※数値が未入力(None)の項目は、比較するとエラーになるため、
#   入力済みかどうかを先に確認してから判定する。
class Diagnosis:

    def __init__(self, fighter):
        self.__fighter = fighter

    # 該当したコメントをリストにして返す
    def results(self):
        f = self.__fighter
        messages = []

        # ルール1 投げられた回数が、投げた回数の1.5倍より多い
        if f.throw_received is not None and f.throw_landed is not None:
            if f.throw_received > f.throw_landed * 1.5:
                messages.append('投げ受けが多い。投げ抜けが課題')

        # ルール2 追い詰められている時間が、追い詰めている時間の2倍より長い
        if f.cornered_sec is not None and f.cornering_sec is not None:
            if f.cornered_sec > f.cornering_sec * 2:
                messages.append('壁際に追い込まれやすい')

        # ルール3 DIを受けた回数が、決めた回数の2倍より多い
        if f.di_received is not None and f.di_landed is not None:
            if f.di_received > f.di_landed * 2:
                messages.append('ドライブインパクトを受ける回数が多い')

        # ルール4 ジャストパリィの回数が0.5回未満
        if f.just_parry is not None:
            if f.just_parry < 0.5:
                messages.append('ジャストパリィの精度に伸びしろあり')

        # ルール5 ドライブゲージをダメージに使う割合が50%を超えている
        if f.damage_pct is not None:
            if f.damage_pct > 50:
                messages.append('ドライブゲージをダメージに使う割合が高い')

        return messages

    # 一覧画面のカード用。短い1行の要約を返す。
    def summary(self):
        messages = self.results()

        if len(messages) == 0:
            return '特筆すべき傾向なし'
        if len(messages) == 1:
            return messages[0]
        return messages[0] + ' 他' + str(len(messages) - 1) + '件'
