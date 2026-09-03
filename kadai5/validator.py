# FighterValidator クラス
#  フォームの入力値チェック(バリデーション)を担当する。
#  チェックはすべてPython側(サーバーサイド)で行う。
#  ※JavaScriptでのチェックは行わない。
#
#  実装した4種類のチェック
#   1. 必須チェック   : name, main_char
#   2. 正規表現       : CFNコード、%、回数、LP の書式
#   3. ホワイトリスト : main_char, rank_name(選択肢の改ざん対策)
#   4. 相関チェック   : ドライブゲージ7項目の合計が約100%か
import re

# ホワイトリスト(選択肢)。フォームの表示とチェックの両方で使う。
MAIN_CHARS = [
    'Ryu', 'Ken', 'Luke', 'Jamie', 'Chun-Li', 'Guile', 'Kimberly', 'Juri',
    'Cammy', 'Zangief', 'Dee Jay', 'Manon', 'Marisa', 'Lily', 'JP', 'Blanka',
    'Dhalsim', 'E.Honda', 'Rashid', 'A.K.I.', 'Ed', 'Akuma', 'M.Bison',
    'Terry', 'Mai', 'Elena', 'Sagat',
]

RANK_NAMES = [
    'Rookie', 'Iron', 'Bronze', 'Silver', 'Gold',
    'Platinum', 'Diamond', 'Master', 'Legend',
]

# 画面表示用の項目名(エラーメッセージとフォームのラベルで共用)
LABELS = {
    'name': 'プレイヤー名',
    'cfn_code': 'CFNコード',
    'main_char': '使用キャラ',
    'rank_name': 'ランク',
    'lp': 'LP',
    'parry_pct': 'ドライブパリィ%',
    'di_pct': 'ドライブインパクト%',
    'od_arts_pct': 'オーバードライブアーツ%',
    'parry_rush_pct': 'パリィドライブラッシュ%',
    'cancel_rush_pct': 'キャンセルドライブラッシュ%',
    'reversal_pct': 'ドライブリバーサル%',
    'damage_pct': 'ダメージ%',
    'throw_landed': '投げ 決めた回数',
    'throw_received': '投げ 受けた回数',
    'di_landed': 'DI 決めた回数',
    'di_received': 'DI 受けた回数',
    'just_parry': 'ジャストパリィ回数',
    'cornering_sec': '相手を追い詰めている時間',
    'cornered_sec': '相手に追い詰められている時間',
    'note': 'メモ',
}

# 正規表現のパターン
#  \d ではなく [0-9] を使う。\d は全角数字(１２３)にもマッチしてしまい、
#  全角のままDBに入ってしまうため、半角だけに限定する。
CFN_PATTERN = r'^[0-9]{10}$'                    # CFNコード: 数字ちょうど10桁
LP_PATTERN = r'^[0-9]{1,5}$'                    # LP: 数字1〜5桁
PCT_PATTERN = r'^[0-9]{1,3}(\.[0-9]{1,2})?$'    # %: 小数第2位まで
COUNT_PATTERN = r'^[0-9]{1,2}(\.[0-9])?$'       # 回数・秒: 小数第1位まで

# %の7項目(相関チェックの対象)
GAUGE_COLUMNS = [
    'parry_pct', 'di_pct', 'od_arts_pct', 'parry_rush_pct',
    'cancel_rush_pct', 'reversal_pct', 'damage_pct',
]

# 回数の5項目
COUNT_COLUMNS = [
    'throw_landed', 'throw_received',
    'di_landed', 'di_received', 'just_parry',
]

# 壁際(秒)の2項目
WALL_COLUMNS = ['cornering_sec', 'cornered_sec']


class FighterValidator:

    def __init__(self, form):
        # request.form(送信された生の文字列)
        self.__form = form
        # DB保存用の値。未入力の項目はNoneのままにする。
        # エラーになった項目には、入力された文字列をそのまま入れておく。
        # (フォームに戻したときに、入力した内容が消えないようにするため)
        self.clean = {}
        # エラーメッセージ。{項目名: メッセージ}
        self.errors = {}

    # フォームから値を取り出す。前後の空白は削除。
    # 未送信の場合はNoneが返るため、空文字に変換する。
    def __get(self, key):
        value = self.__form.get(key)
        if value is None:
            return ''
        return value.strip()

    # チェック本体。(clean, errors)を返す。
    def validate(self):
        # まず全項目をNoneで初期化しておく
        self.clean['name'] = None
        self.clean['cfn_code'] = None
        self.clean['main_char'] = None
        self.clean['rank_name'] = None
        self.clean['lp'] = None
        for column in GAUGE_COLUMNS:
            self.clean[column] = None
        for column in COUNT_COLUMNS:
            self.clean[column] = None
        for column in WALL_COLUMNS:
            self.clean[column] = None
        self.clean['note'] = None

        self.__check_name()
        self.__check_main_char()
        self.__check_rank_name()
        self.__check_cfn_code()
        self.__check_lp()

        for column in GAUGE_COLUMNS:
            self.__check_pct(column)
        for column in COUNT_COLUMNS:
            self.__check_count(column)
        for column in WALL_COLUMNS:
            self.__check_count(column)

        self.__check_gauge_total()

        # メモは自由入力なので書式チェックはしない
        note = self.__get('note')
        if note:
            self.clean['note'] = note

        return self.clean, self.errors

    # 1. 必須チェック + 文字数
    def __check_name(self):
        name = self.__get('name')
        self.clean['name'] = name
        if not name:
            self.errors['name'] = LABELS['name'] + 'は必須です'
        elif len(name) > 32:
            self.errors['name'] = LABELS['name'] + 'は32文字以内です'

    # 1. 必須 + 3. ホワイトリスト
    def __check_main_char(self):
        main_char = self.__get('main_char')
        self.clean['main_char'] = main_char
        if not main_char:
            self.errors['main_char'] = LABELS['main_char'] + 'は必須です'
        elif main_char not in MAIN_CHARS:
            # selectの選択肢を改ざんして送信された場合はここで弾く
            self.errors['main_char'] = LABELS['main_char'] + 'の値が不正です'

    # 3. ホワイトリスト(任意項目)
    def __check_rank_name(self):
        rank_name = self.__get('rank_name')
        if not rank_name:
            return
        self.clean['rank_name'] = rank_name
        if rank_name not in RANK_NAMES:
            self.errors['rank_name'] = LABELS['rank_name'] + 'の値が不正です'

    # 2. 正規表現(任意項目)
    def __check_cfn_code(self):
        cfn_code = self.__get('cfn_code')
        if not cfn_code:
            return
        self.clean['cfn_code'] = cfn_code
        if not re.match(CFN_PATTERN, cfn_code):
            self.errors['cfn_code'] = LABELS['cfn_code'] + 'は半角数字10桁で入力してください'

    # 2. 正規表現 + 範囲チェック(任意項目)
    def __check_lp(self):
        lp = self.__get('lp')
        if not lp:
            return
        # まず文字列のまま入れておき、チェックを通ったら数値に変換する
        self.clean['lp'] = lp
        if not re.match(LP_PATTERN, lp):
            self.errors['lp'] = LABELS['lp'] + 'は半角の整数で入力してください'
        elif int(lp) > 50000:
            self.errors['lp'] = LABELS['lp'] + 'は0〜50000の範囲です'
        else:
            self.clean['lp'] = int(lp)

    # 2. 正規表現 + 範囲チェック(%・任意項目)
    def __check_pct(self, column):
        value = self.__get(column)
        if not value:
            return
        self.clean[column] = value
        if not re.match(PCT_PATTERN, value):
            self.errors[column] = LABELS[column] + 'は半角数字(小数第2位まで)で入力してください'
        elif float(value) > 100:
            self.errors[column] = LABELS[column] + 'は0〜100の範囲です'
        else:
            self.clean[column] = float(value)

    # 2. 正規表現 + 範囲チェック(回数・秒・任意項目)
    def __check_count(self, column):
        value = self.__get(column)
        if not value:
            return
        self.clean[column] = value
        if not re.match(COUNT_PATTERN, value):
            self.errors[column] = LABELS[column] + 'は0〜99.9(小数第1位まで)で入力してください'
        elif float(value) > 99.9:
            self.errors[column] = LABELS[column] + 'は0〜99.9の範囲です'
        else:
            self.clean[column] = float(value)

    # 4. 相関チェック
    #  1項目ずつは正しくても、7項目の合計が100%にならなければ
    #  入力ミスと判断する。項目をまたぐチェックが今回の工夫点。
    def __check_gauge_total(self):
        total = 0
        count = 0
        for column in GAUGE_COLUMNS:
            # すでにエラーがある項目が1つでもあれば、合計チェックはしない
            # (メッセージが二重に出るのを避けるため。またエラーのときの
            #  clean[column] は文字列なので、そのまま足すことはできない)
            if column in self.errors:
                return
            if self.clean[column] is not None:
                total += self.clean[column]
                count += 1

        # 7項目すべて未入力ならチェックしない
        if count == 0:
            return

        # 公式サイトの表示が四捨五入されているため99.0〜101.0を許容する
        if total < 99.0 or total > 101.0:
            self.errors['gauge_total'] = \
                'ドライブゲージ使用実績の合計が' + str(round(total, 2)) + '%です(合計100%になるはずです)'
