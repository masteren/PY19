# Fighter クラス
#  DBの1行(プレイヤー1人分)を保持するデータクラス。
#  DAOがSELECTした行(タプル)を受け取り、
#  テンプレートから f.name の形で参照できるようにする。
#  ※データを保持するだけで、SQLは持たない(DAOの役割)。
class Fighter:

    def __init__(self, row):
        # SELECT * の列順 = schema.sql の定義順。
        # 基本情報
        self.id = row[0]
        self.name = row[1]
        self.cfn_code = row[2]
        self.main_char = row[3]
        self.rank_name = row[4]
        self.lp = row[5]
        # ドライブゲージ使用実績(%)
        self.parry_pct = row[6]
        self.di_pct = row[7]
        self.od_arts_pct = row[8]
        self.parry_rush_pct = row[9]
        self.cancel_rush_pct = row[10]
        self.reversal_pct = row[11]
        self.damage_pct = row[12]
        # 回数系(過去100戦平均)
        self.throw_landed = row[13]
        self.throw_received = row[14]
        self.di_landed = row[15]
        self.di_received = row[16]
        self.just_parry = row[17]
        # 壁際(秒)
        self.cornering_sec = row[18]
        self.cornered_sec = row[19]
        # その他
        self.note = row[20]

    # 未入力(None)を0として返すだけのメソッド。
    # グラフの幅計算で None が混ざるとエラーになるため。
    def zero_if_none(self, value):
        if value is None:
            return 0
        return value

    # プロパティ(ゲッター)
    #  横棒グラフ用に (ラベル, 値) のリストを作って返す。
    #  テンプレート側は f.drive_gauge_items でループするだけでよい。
    @property
    def drive_gauge_items(self):
        return [
            ('ドライブパリィ', self.zero_if_none(self.parry_pct)),
            ('ドライブインパクト', self.zero_if_none(self.di_pct)),
            ('オーバードライブアーツ', self.zero_if_none(self.od_arts_pct)),
            ('パリィドライブラッシュ', self.zero_if_none(self.parry_rush_pct)),
            ('キャンセルドライブラッシュ', self.zero_if_none(self.cancel_rush_pct)),
            ('ドライブリバーサル', self.zero_if_none(self.reversal_pct)),
            ('ダメージ', self.zero_if_none(self.damage_pct)),
        ]
