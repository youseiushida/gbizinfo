"""特許・意匠・商標分類の列挙型モジュール。

特許種別、特許 FI 分類、意匠日本分類、商標類似商品・役務審査基準を定義する。
"""

from __future__ import annotations

from enum import StrEnum


class PatentType(StrEnum):
    """特許種別の列挙型。

    ``PatentInfoV2.patent_type`` フィールドの値に対応する。
    特許・意匠・商標の3種別を定義する。
    """

    特許 = "特許"
    意匠 = "意匠"
    商標 = "商標"


# PatentType 英語 alias
PATENT = PatentType.特許
DESIGN = PatentType.意匠
TRADEMARK = PatentType.商標


class PatentClassification(StrEnum):
    """特許 FI 分類の列挙型。

    IPC（国際特許分類）に基づく FI 分類のセクション・クラスを定義する。
    ``description_ja`` / ``description_en`` プロパティで日英の分類名を取得できる。
    """

    農業_林業_畜産 = "A01"
    ベイキング_生地製造 = "A21"
    屠殺_肉処理 = "A22"
    食品_食料品 = "A23"
    たばこ_喫煙具 = "A24"
    衣類 = "A41"
    頭部着用物 = "A42"
    履物 = "A43"
    小間物_貴金属宝石 = "A44"
    手持品_旅行用品 = "A45"
    ブラシ製品 = "A46"
    家具_家庭用品 = "A47"
    医学_獣医学_衛生学 = "A61"
    人命救助_消防 = "A62"
    スポーツ_ゲーム_娯楽 = "A63"
    セクションA_その他 = "A99"
    物理的化学的方法_装置 = "B01"
    破砕_粉砕 = "B02"
    固体物質の分離 = "B03"
    遠心装置 = "B04"
    霧化_噴霧 = "B05"
    機械的振動 = "B06"
    固体分離_仕分け = "B07"
    清掃 = "B08"
    固体廃棄物処理 = "B09"
    機械的金属加工 = "B21"
    鋳造_粉末冶金 = "B22"
    工作機械_金属加工 = "B23"
    研削_研磨 = "B24"
    手工具_動力工具 = "B25"
    切断手工具_切断機 = "B26"
    木材加工 = "B27"
    セメント_粘土_石材加工 = "B28"
    プラスチック加工 = "B29"
    プレス = "B30"
    紙_板紙製品の製造 = "B31"
    積層体 = "B32"
    付加製造技術 = "B33"
    印刷_タイプライター = "B41"
    製本_アルバム = "B42"
    筆記_製図用器具 = "B43"
    装飾技術 = "B44"
    車両一般 = "B60"
    鉄道 = "B61"
    路面車両 = "B62"
    船舶_水上構造物 = "B63"
    航空機_宇宙工学 = "B64"
    運搬_包装_貯蔵 = "B65"
    巻上装置_揚重装置 = "B66"
    容器開封密封_液体取扱い = "B67"
    馬具_詰め物 = "B68"
    マイクロ構造技術 = "B81"
    ナノテクノロジー = "B82"
    セクションB_その他 = "B99"
    無機化学 = "C01"
    水_廃水処理 = "C02"
    ガラス_鉱物 = "C03"
    セメント_コンクリート_セラミックス = "C04"
    肥料 = "C05"
    火薬_マッチ = "C06"
    有機化学 = "C07"
    有機高分子化合物 = "C08"
    染料_ペイント_接着剤 = "C09"
    石油_ガス_コークス工業 = "C10"
    油脂_洗浄剤 = "C11"
    生化学_微生物学 = "C12"
    糖工業 = "C13"
    皮革 = "C14"
    鉄冶金 = "C21"
    冶金_合金 = "C22"
    金属被覆_表面処理 = "C23"
    電気分解_電気泳動 = "C25"
    結晶成長 = "C30"
    コンビナトリアル技術 = "C40"
    セクションC_その他 = "C99"
    糸_繊維_紡績 = "D01"
    糸_ロープ仕上げ = "D02"
    織成 = "D03"
    組みひも_メリヤス編成 = "D04"
    縫製_刺しゅう = "D05"
    繊維処理_洗濯 = "D06"
    ロープ_ケーブル = "D07"
    製紙_セルロース = "D21"
    セクションD_その他 = "D99"
    道路_鉄道_橋りょう建設 = "E01"
    水工_基礎_土砂移送 = "E02"
    上水_下水 = "E03"
    建築物 = "E04"
    錠_鍵_金庫 = "E05"
    戸_窓_シャッタ = "E06"
    削孔_採鉱 = "E21"
    セクションE_その他 = "E99"
    機関一般_蒸気機関 = "F01"
    燃焼機関 = "F02"
    液体用機関_風力原動機 = "F03"
    容積形機械_ポンプ = "F04"
    流体圧アクチュエータ = "F15"
    機械要素 = "F16"
    ガス_液体の貯蔵分配 = "F17"
    照明 = "F21"
    蒸気発生 = "F22"
    燃焼装置 = "F23"
    加熱_レンジ_換気 = "F24"
    冷凍_冷却_ヒートポンプ = "F25"
    乾燥 = "F26"
    炉_キルン_レトルト = "F27"
    熱交換 = "F28"
    武器 = "F41"
    弾薬_爆破 = "F42"
    セクションF_その他 = "F99"
    測定_試験 = "G01"
    光学 = "G02"
    写真_映画_ホログラフイ = "G03"
    時計 = "G04"
    制御_調整 = "G05"
    計算_計数 = "G06"
    チェック装置 = "G07"
    信号 = "G08"
    教育_暗号方法_表示_広告 = "G09"
    楽器_音響 = "G10"
    情報記憶 = "G11"
    器械の細部 = "G12"
    情報通信技術_ICT = "G16"
    核物理_核工学 = "G21"
    セクションG_その他 = "G99"
    基本的電気素子 = "H01"
    電力の発電_変換_配電 = "H02"
    基本電子回路 = "H03"
    電気通信技術 = "H04"
    電気技術 = "H05"
    セクションH_その他 = "H99"

    @property
    def description_ja(self) -> str:
        """日本語の分類名を返す。

        Returns:
            日本語の分類名文字列。
        """
        return _PATENT_DESC_JA[self]

    @property
    def description_en(self) -> str:
        """英語の分類名を返す。

        Returns:
            英語の分類名文字列。
        """
        return _PATENT_DESC_EN[self]


_PATENT_DESC_JA: dict[PatentClassification, str] = {
    PatentClassification.農業_林業_畜産: "農業; 林業; 畜産; 狩猟; 捕獲; 漁業",
    PatentClassification.ベイキング_生地製造: "ベイキング; 生地製造または加工の機械あるいは設備; ベイキングの生地",
    PatentClassification.屠殺_肉処理: "屠殺; 肉処理; 家禽または魚の処理",
    PatentClassification.食品_食料品: "食品または食料品; 他のクラスに包含されないそれらの処理",
    PatentClassification.たばこ_喫煙具: "たばこ; 葉巻たばこ; 紙巻たばこ; 喫煙具",
    PatentClassification.衣類: "衣類",
    PatentClassification.頭部着用物: "頭部に着用するもの",
    PatentClassification.履物: "履物",
    PatentClassification.小間物_貴金属宝石: "小間物; 貴金属宝石類",
    PatentClassification.手持品_旅行用品: "手持品または旅行用品",
    PatentClassification.ブラシ製品: "ブラシ製品",
    PatentClassification.家具_家庭用品: "家具; 家庭用品または家庭用設備; コーヒーひき; 香辛料ひき; 真空掃除機一般",
    PatentClassification.医学_獣医学_衛生学: "医学または獣医学; 衛生学",
    PatentClassification.人命救助_消防: "人命救助; 消防",
    PatentClassification.スポーツ_ゲーム_娯楽: "スポーツ; ゲーム; 娯楽",
    PatentClassification.セクションA_その他: "このセクションの中で他に分類されない主題事項",
    PatentClassification.物理的化学的方法_装置: "物理的または化学的方法または装置一般",
    PatentClassification.破砕_粉砕: "破砕, または粉砕; 製粉のための穀粒の前処理",
    PatentClassification.固体物質の分離: "液体による, または, 風力テーブルまたはジグによる固体物質の分離; 固体物質または流体から固体物質の磁気または静電気による分離, 高圧電界による分離",
    PatentClassification.遠心装置: "物理的または化学的工程を行なうための遠心装置または機械",
    PatentClassification.霧化_噴霧: "霧化または噴霧一般; 液体または他の流動性材料の表面への適用一般",
    PatentClassification.機械的振動: "機械的振動の発生または伝達一般",
    PatentClassification.固体分離_仕分け: "固体相互の分離; 仕分け",
    PatentClassification.清掃: "清掃",
    PatentClassification.固体廃棄物処理: "固体廃棄物の処理; 汚染土壌の再生",
    PatentClassification.機械的金属加工: "本質的には材料の除去が行なわれない機械的金属加工; 金属の打抜き",
    PatentClassification.鋳造_粉末冶金: "鋳造; 粉末冶金",
    PatentClassification.工作機械_金属加工: "工作機械; 他に分類されない金属加工",
    PatentClassification.研削_研磨: "研削; 研磨",
    PatentClassification.手工具_動力工具: "手工具; 可搬型動力工具; 手工具用の柄; 作業場設備; マニプレータ",
    PatentClassification.切断手工具_切断機: "切断手工具; 切断; 切断機",
    PatentClassification.木材加工: "木材または類似の材料の加工または保存; 釘打ち機またはステープル打ち機一般",
    PatentClassification.セメント_粘土_石材加工: "セメント, 粘土, または石材の加工",
    PatentClassification.プラスチック加工: "プラスチックの加工; 可塑状態の物質の加工一般",
    PatentClassification.プレス: "プレス",
    PatentClassification.紙_板紙製品の製造: "紙，板紙または紙と同様の方法で加工される材料からなる物品の製造；紙，板紙または紙と同様の方法で加工される材料の加工",
    PatentClassification.積層体: "積層体",
    PatentClassification.付加製造技術: "付加製造技術",
    PatentClassification.印刷_タイプライター: "印刷; 線画機; タイプライター; スタンプ",
    PatentClassification.製本_アルバム: "製本; アルバム; ファイル; 特殊印刷物",
    PatentClassification.筆記_製図用器具: "筆記用または製図用の器具; 机上付属具",
    PatentClassification.装飾技術: "装飾技術",
    PatentClassification.車両一般: "車両一般",
    PatentClassification.鉄道: "鉄道",
    PatentClassification.路面車両: "鉄道以外の路面車両",
    PatentClassification.船舶_水上構造物: "船舶またはその他の水上浮揚構造物; 関連艤装品",
    PatentClassification.航空機_宇宙工学: "航空機; 飛行; 宇宙工学",
    PatentClassification.運搬_包装_貯蔵: "運搬; 包装; 貯蔵; 薄板状または線条材料の取扱い",
    PatentClassification.巻上装置_揚重装置: "巻上装置; 揚重装置; 牽引装置",
    PatentClassification.容器開封密封_液体取扱い: "びん, 広口びんまたは類似の容器の開封または密封; 液体の取扱い",
    PatentClassification.馬具_詰め物: "馬具; 詰め物, かわ張りされた物品",
    PatentClassification.マイクロ構造技術: "マイクロ構造技術",
    PatentClassification.ナノテクノロジー: "ナノテクノロジー",
    PatentClassification.セクションB_その他: "このセクションの中で他に分類されない主題事項",
    PatentClassification.無機化学: "無機化学",
    PatentClassification.水_廃水処理: "水, 廃水, 下水または汚泥の処理",
    PatentClassification.ガラス_鉱物: "ガラス; 鉱物またはスラグウール",
    PatentClassification.セメント_コンクリート_セラミックス: "セメント; コンクリート; 人造石; セラミックス; 耐火物",
    PatentClassification.肥料: "肥料; 肥料の製造",
    PatentClassification.火薬_マッチ: "火薬; マッチ",
    PatentClassification.有機化学: "有機化学",
    PatentClassification.有機高分子化合物: "有機高分子化合物; その製造または化学的加工; それに基づく組成物",
    PatentClassification.染料_ペイント_接着剤: "染料; ペイント; つや出し剤; 天然樹脂; 接着剤; 他に分類されない組成物; 他に分類されない材料の応用",
    PatentClassification.石油_ガス_コークス工業: "石油, ガスまたはコークス工業; 一酸化炭素を含有する工業ガス; 燃料; 潤滑剤; でい炭",
    PatentClassification.油脂_洗浄剤: "動物性または植物性油, 脂肪, 脂肪性物質またはろう; それに由来する脂肪酸; 洗浄剤; ろうそく",
    PatentClassification.生化学_微生物学: "生化学; ビール; 酒精; ぶどう酒; 酢; 微生物学; 酵素学; 突然変異または遺伝子工学",
    PatentClassification.糖工業: "糖工業",
    PatentClassification.皮革: "原皮; 裸皮; 生皮; なめし革",
    PatentClassification.鉄冶金: "鉄冶金",
    PatentClassification.冶金_合金: "冶金; 鉄または非鉄合金; 合金の処理または非鉄金属の処理",
    PatentClassification.金属被覆_表面処理: "金属質材料への被覆; 金属質材料による材料への被覆; 化学的表面処理; 金属質材料の拡散処理; 真空蒸着, スパッタリング, イオン注入法, または化学蒸着による被覆一般; 金属質材料の防食または鉱皮の抑制一般",
    PatentClassification.電気分解_電気泳動: "電気分解または電気泳動方法; そのための装置",
    PatentClassification.結晶成長: "結晶成長",
    PatentClassification.コンビナトリアル技術: "コンビナトリアル技術",
    PatentClassification.セクションC_その他: "このセクションの中で他に分類されない主題事項",
    PatentClassification.糸_繊維_紡績: "天然または人造の糸または繊維; 紡績",
    PatentClassification.糸_ロープ仕上げ: "糸; 糸またはロープの機械的な仕上げ; 整経またはビーム巻き取り",
    PatentClassification.織成: "織成",
    PatentClassification.組みひも_メリヤス編成: "組みひも; レース編み; メリヤス編成; 縁とり; 不織布",
    PatentClassification.縫製_刺しゅう: "縫製; 刺しゅう; タフティング",
    PatentClassification.繊維処理_洗濯: "繊維または類似のものの処理; 洗濯; 他に分類されない可とう性材料",
    PatentClassification.ロープ_ケーブル: "ロープ; 電気的なもの以外のケーブル",
    PatentClassification.製紙_セルロース: "製紙; セルロースの製造",
    PatentClassification.セクションD_その他: "このセクションの中で他に分類されない主題事項",
    PatentClassification.道路_鉄道_橋りょう建設: "道路, 鉄道または橋りょうの建設",
    PatentClassification.水工_基礎_土砂移送: "水工; 基礎; 土砂の移送",
    PatentClassification.上水_下水: "上水; 下水",
    PatentClassification.建築物: "建築物",
    PatentClassification.錠_鍵_金庫: "錠; 鍵（かぎ）; 窓または戸の付属品; 金庫",
    PatentClassification.戸_窓_シャッタ: "戸, 窓, シャッタまたはローラブラインド一般; はしご",
    PatentClassification.削孔_採鉱: "地中もしくは岩石の削孔; 採鉱",
    PatentClassification.セクションE_その他: "このセクションの中で他に分類されない主題事項",
    PatentClassification.機関一般_蒸気機関: "機械または機関一般; 機関設備一般; 蒸気機関",
    PatentClassification.燃焼機関: "燃焼機関; 熱ガスまたは燃焼生成物を利用する機関設備",
    PatentClassification.液体用機関_風力原動機: "液体用機械または機関; 風力原動機, ばね原動機, 重力原動機; 他類に属さない機械動力または反動推進力を発生するもの",
    PatentClassification.容積形機械_ポンプ: "液体用容積形機械; 液体または圧縮性流体用ポンプ",
    PatentClassification.流体圧アクチュエータ: "流体圧アクチュエータ; 水力学または空気力学一般",
    PatentClassification.機械要素: "機械要素または単位; 機械または装置の効果的機能を生じ維持するための一般的手段",
    PatentClassification.ガス_液体の貯蔵分配: "ガスまたは液体の貯蔵または分配",
    PatentClassification.照明: "照明",
    PatentClassification.蒸気発生: "蒸気発生",
    PatentClassification.燃焼装置: "燃焼装置; 燃焼方法",
    PatentClassification.加熱_レンジ_換気: "加熱; レンジ; 換気",
    PatentClassification.冷凍_冷却_ヒートポンプ: "冷凍または冷却; 加熱と冷凍との組み合わせシステム; ヒートポンプシステム; 氷の製造または貯蔵; 気体の液化または固体化",
    PatentClassification.乾燥: "乾燥",
    PatentClassification.炉_キルン_レトルト: "炉, キルン, 窯（かま）; レトルト",
    PatentClassification.熱交換: "熱交換一般",
    PatentClassification.武器: "武器",
    PatentClassification.弾薬_爆破: "弾薬; 爆破",
    PatentClassification.セクションF_その他: "このセクションの中で他に分類されない主題事項",
    PatentClassification.測定_試験: "測定; 試験",
    PatentClassification.光学: "光学",
    PatentClassification.写真_映画_ホログラフイ: "写真; 映画; 光波以外の波を使用する類似技術; 電子写真; ホログラフイ",
    PatentClassification.時計: "時計",
    PatentClassification.制御_調整: "制御; 調整",
    PatentClassification.計算_計数: "計算; 計数",
    PatentClassification.チェック装置: "チェック装置",
    PatentClassification.信号: "信号",
    PatentClassification.教育_暗号方法_表示_広告: "教育; 暗号方法; 表示; 広告; シール",
    PatentClassification.楽器_音響: "楽器; 音響",
    PatentClassification.情報記憶: "情報記憶",
    PatentClassification.器械の細部: "器械の細部",
    PatentClassification.情報通信技術_ICT: "特定の用途分野に特に適合した情報通信技術［ＩＣＴ］",
    PatentClassification.核物理_核工学: "核物理; 核工学",
    PatentClassification.セクションG_その他: "このセクションの中で他に分類されない主題事項",
    PatentClassification.基本的電気素子: "基本的電気素子",
    PatentClassification.電力の発電_変換_配電: "電力の発電, 変換, 配電",
    PatentClassification.基本電子回路: "基本電子回路",
    PatentClassification.電気通信技術: "電気通信技術",
    PatentClassification.電気技術: "他に分類されない電気技術",
    PatentClassification.セクションH_その他: "このセクションの中で他に分類されない主題事項",
}

_PATENT_DESC_EN: dict[PatentClassification, str] = {
    PatentClassification.農業_林業_畜産: "Agriculture; Forestry; Animal husbandry; Hunting; Trapping; Fishing",
    PatentClassification.ベイキング_生地製造: "Baking; Edible doughs",
    PatentClassification.屠殺_肉処理: "Butchering; Meat treatment; Processing poultry or fish",
    PatentClassification.食品_食料品: "Foods or foodstuffs; Treatment thereof",
    PatentClassification.たばこ_喫煙具: "Tobacco; Cigars; Cigarettes; Smokers' requisites",
    PatentClassification.衣類: "Wearing apparel",
    PatentClassification.頭部着用物: "Headwear",
    PatentClassification.履物: "Footwear",
    PatentClassification.小間物_貴金属宝石: "Haberdashery; Jewellery",
    PatentClassification.手持品_旅行用品: "Hand or travelling articles",
    PatentClassification.ブラシ製品: "Brushware",
    PatentClassification.家具_家庭用品: "Furniture; Domestic articles or appliances; Coffee mills; Spice mills; Suction cleaners in general",
    PatentClassification.医学_獣医学_衛生学: "Medical or veterinary science; Hygiene",
    PatentClassification.人命救助_消防: "Life-saving; Fire-fighting",
    PatentClassification.スポーツ_ゲーム_娯楽: "Sports; Games; Amusements",
    PatentClassification.セクションA_その他: "Subject matter not otherwise provided for in this section",
    PatentClassification.物理的化学的方法_装置: "Physical or chemical processes or apparatus in general",
    PatentClassification.破砕_粉砕: "Crushing, pulverising, or disintegrating; Preparatory treatment of grain for milling",
    PatentClassification.固体物質の分離: "Separation of solid materials using liquids or using pneumatic tables or jigs",
    PatentClassification.遠心装置: "Centrifugal apparatus or machines for carrying-out physical or chemical processes",
    PatentClassification.霧化_噴霧: "Spraying or atomising in general; Applying fluent materials to surfaces, in general",
    PatentClassification.機械的振動: "Generating or transmitting mechanical vibrations in general",
    PatentClassification.固体分離_仕分け: "Separating solids from solids; Sorting",
    PatentClassification.清掃: "Cleaning",
    PatentClassification.固体廃棄物処理: "Disposal of solid waste; Reclamation of contaminated soil",
    PatentClassification.機械的金属加工: "Mechanical metal-working without essentially removing material; Punching metal",
    PatentClassification.鋳造_粉末冶金: "Casting; Powder metallurgy",
    PatentClassification.工作機械_金属加工: "Machine tools; Metal-working not otherwise provided for",
    PatentClassification.研削_研磨: "Grinding; Polishing",
    PatentClassification.手工具_動力工具: "Hand tools; Portable power-driven tools; Manipulators",
    PatentClassification.切断手工具_切断機: "Hand cutting tools; Cutting; Severing",
    PatentClassification.木材加工: "Working or preserving wood or similar material",
    PatentClassification.セメント_粘土_石材加工: "Working cement, clay, or stone",
    PatentClassification.プラスチック加工: "Working of plastics; Working of substances in a plastic state in general",
    PatentClassification.プレス: "Presses",
    PatentClassification.紙_板紙製品の製造: "Making articles of paper, cardboard or material worked in a manner analogous to paper",
    PatentClassification.積層体: "Layered products",
    PatentClassification.付加製造技術: "Additive manufacturing technology",
    PatentClassification.印刷_タイプライター: "Printing; Lining machines; Typewriters; Stamps",
    PatentClassification.製本_アルバム: "Bookbinding; Albums; Files; Special printed matter",
    PatentClassification.筆記_製図用器具: "Writing or drawing implements; Bureau accessories",
    PatentClassification.装飾技術: "Decorative arts",
    PatentClassification.車両一般: "Vehicles in general",
    PatentClassification.鉄道: "Railways",
    PatentClassification.路面車両: "Land vehicles for travelling otherwise than on rails",
    PatentClassification.船舶_水上構造物: "Ships or other waterborne vessels; Related equipment",
    PatentClassification.航空機_宇宙工学: "Aircraft; Aviation; Cosmonautics",
    PatentClassification.運搬_包装_貯蔵: "Conveying; Packing; Storing; Handling thin or filamentary material",
    PatentClassification.巻上装置_揚重装置: "Hoisting; Lifting; Hauling",
    PatentClassification.容器開封密封_液体取扱い: "Opening or closing bottles, jars or similar containers; Liquid handling",
    PatentClassification.馬具_詰め物: "Saddlery; Upholstery",
    PatentClassification.マイクロ構造技術: "Microstructural technology",
    PatentClassification.ナノテクノロジー: "Nanotechnology",
    PatentClassification.セクションB_その他: "Subject matter not otherwise provided for in this section",
    PatentClassification.無機化学: "Inorganic chemistry",
    PatentClassification.水_廃水処理: "Treatment of water, waste water, sewage, or sludge",
    PatentClassification.ガラス_鉱物: "Glass; Mineral or slag wool",
    PatentClassification.セメント_コンクリート_セラミックス: "Cements; Concrete; Artificial stone; Ceramics; Refractories",
    PatentClassification.肥料: "Fertilisers; Manufacture thereof",
    PatentClassification.火薬_マッチ: "Explosives; Matches",
    PatentClassification.有機化学: "Organic chemistry",
    PatentClassification.有機高分子化合物: "Organic macromolecular compounds",
    PatentClassification.染料_ペイント_接着剤: "Dyes; Paints; Polishes; Natural resins; Adhesives",
    PatentClassification.石油_ガス_コークス工業: "Petroleum, gas or coke industries; Technical gases containing carbon monoxide; Fuels; Lubricants; Peat",
    PatentClassification.油脂_洗浄剤: "Animal or vegetable oils, fats, fatty substances or waxes; Detergents; Candles",
    PatentClassification.生化学_微生物学: "Biochemistry; Beer; Spirits; Wine; Vinegar; Microbiology; Enzymology; Mutation or genetic engineering",
    PatentClassification.糖工業: "Sugar industry",
    PatentClassification.皮革: "Skins; Hides; Pelts; Leather",
    PatentClassification.鉄冶金: "Metallurgy of iron",
    PatentClassification.冶金_合金: "Metallurgy; Ferrous or non-ferrous alloys; Treatment of alloys or non-ferrous metals",
    PatentClassification.金属被覆_表面処理: "Coating metallic material",
    PatentClassification.電気分解_電気泳動: "Electrolytic or electrophoretic processes; Apparatus therefor",
    PatentClassification.結晶成長: "Crystal growth",
    PatentClassification.コンビナトリアル技術: "Combinatorial technology",
    PatentClassification.セクションC_その他: "Subject matter not otherwise provided for in this section",
    PatentClassification.糸_繊維_紡績: "Natural or man-made threads or fibres; Spinning",
    PatentClassification.糸_ロープ仕上げ: "Yarns; Mechanical finishing of yarns or ropes; Warping or beaming",
    PatentClassification.織成: "Weaving",
    PatentClassification.組みひも_メリヤス編成: "Braiding; Lace-making; Knitting; Trimmings; Non-woven fabrics",
    PatentClassification.縫製_刺しゅう: "Sewing; Embroidering; Tufting",
    PatentClassification.繊維処理_洗濯: "Treatment of textiles or the like; Laundering; Flexible materials not otherwise provided for",
    PatentClassification.ロープ_ケーブル: "Ropes; Cables other than electric",
    PatentClassification.製紙_セルロース: "Paper-making; Production of cellulose",
    PatentClassification.セクションD_その他: "Subject matter not otherwise provided for in this section",
    PatentClassification.道路_鉄道_橋りょう建設: "Construction of roads, railways, or bridges",
    PatentClassification.水工_基礎_土砂移送: "Hydraulic engineering; Foundations; Soil-shifting",
    PatentClassification.上水_下水: "Water supply; Sewerage",
    PatentClassification.建築物: "Building",
    PatentClassification.錠_鍵_金庫: "Locks; Keys; Window or door fittings; Safes",
    PatentClassification.戸_窓_シャッタ: "Doors, windows, shutters, or roller blinds in general; Ladders",
    PatentClassification.削孔_採鉱: "Earth or rock drilling; Mining",
    PatentClassification.セクションE_その他: "Subject matter not otherwise provided for in this section",
    PatentClassification.機関一般_蒸気機関: "Machines or engines in general; Engine plants in general; Steam engines",
    PatentClassification.燃焼機関: "Combustion engines; Hot-gas or combustion-product engine plants",
    PatentClassification.液体用機関_風力原動機: "Machines or engines for liquids; Wind, spring, or weight motors; Producing mechanical power or a reactive propulsive thrust",
    PatentClassification.容積形機械_ポンプ: "Positive-displacement machines for liquids; Pumps for liquids or elastic fluids",
    PatentClassification.流体圧アクチュエータ: "Fluid-pressure actuators; Hydraulics or pneumatics in general",
    PatentClassification.機械要素: "Engineering elements or units; General measures for producing and maintaining effective functioning of machines or installations",
    PatentClassification.ガス_液体の貯蔵分配: "Storing or distributing gases or liquids",
    PatentClassification.照明: "Lighting",
    PatentClassification.蒸気発生: "Steam generation",
    PatentClassification.燃焼装置: "Combustion apparatus; Combustion processes",
    PatentClassification.加熱_レンジ_換気: "Heating; Ranges; Ventilating",
    PatentClassification.冷凍_冷却_ヒートポンプ: "Refrigeration or cooling; Combined heating and refrigeration systems; Heat pump systems; Manufacture or storage of ice; Liquefaction or solidification of gases",
    PatentClassification.乾燥: "Drying",
    PatentClassification.炉_キルン_レトルト: "Furnaces; Kilns; Ovens; Retorts",
    PatentClassification.熱交換: "Heat exchange in general",
    PatentClassification.武器: "Weapons",
    PatentClassification.弾薬_爆破: "Ammunition; Blasting",
    PatentClassification.セクションF_その他: "Subject matter not otherwise provided for in this section",
    PatentClassification.測定_試験: "Measuring; Testing",
    PatentClassification.光学: "Optics",
    PatentClassification.写真_映画_ホログラフイ: "Photography; Cinematography; Analogous techniques using waves other than optical waves; Electrography; Holography",
    PatentClassification.時計: "Horology",
    PatentClassification.制御_調整: "Controlling; Regulating",
    PatentClassification.計算_計数: "Computing; Calculating; Counting",
    PatentClassification.チェック装置: "Checking-devices",
    PatentClassification.信号: "Signalling",
    PatentClassification.教育_暗号方法_表示_広告: "Educating; Cryptography; Display; Advertising; Seals",
    PatentClassification.楽器_音響: "Musical instruments; Acoustics",
    PatentClassification.情報記憶: "Information storage",
    PatentClassification.器械の細部: "Instrument details",
    PatentClassification.情報通信技術_ICT: "Information and communication technology specially adapted for specific application fields",
    PatentClassification.核物理_核工学: "Nuclear physics; Nuclear engineering",
    PatentClassification.セクションG_その他: "Subject matter not otherwise provided for in this section",
    PatentClassification.基本的電気素子: "Electric elements",
    PatentClassification.電力の発電_変換_配電: "Generation, conversion, or distribution of electric power",
    PatentClassification.基本電子回路: "Electronic circuitry",
    PatentClassification.電気通信技術: "Electric communication technique",
    PatentClassification.電気技術: "Electric techniques not otherwise provided for",
    PatentClassification.セクションH_その他: "Subject matter not otherwise provided for in this section",
}




# PatentClassification 英語 alias
AGRICULTURE = PatentClassification.農業_林業_畜産
BAKING = PatentClassification.ベイキング_生地製造
BUTCHERING = PatentClassification.屠殺_肉処理
FOODS = PatentClassification.食品_食料品
TOBACCO_PRODUCTS = PatentClassification.たばこ_喫煙具
WEARING_APPAREL = PatentClassification.衣類
HEADWEAR = PatentClassification.頭部着用物
FOOTWEAR = PatentClassification.履物
HABERDASHERY_JEWELLERY = PatentClassification.小間物_貴金属宝石
HAND_TRAVELLING_ARTICLES = PatentClassification.手持品_旅行用品
BRUSHWARE = PatentClassification.ブラシ製品
FURNITURE_DOMESTIC = PatentClassification.家具_家庭用品
MEDICAL_VETERINARY = PatentClassification.医学_獣医学_衛生学
LIFE_SAVING_FIRE_FIGHTING = PatentClassification.人命救助_消防
SPORTS_GAMES = PatentClassification.スポーツ_ゲーム_娯楽
SECTION_A_OTHER = PatentClassification.セクションA_その他
PHYSICAL_CHEMICAL_PROCESSES = PatentClassification.物理的化学的方法_装置
CRUSHING_PULVERISING = PatentClassification.破砕_粉砕
SEPARATION_BY_LIQUIDS = PatentClassification.固体物質の分離
CENTRIFUGAL_APPARATUS = PatentClassification.遠心装置
SPRAYING_ATOMISING = PatentClassification.霧化_噴霧
MECHANICAL_VIBRATIONS = PatentClassification.機械的振動
SEPARATING_SOLIDS_SORTING = PatentClassification.固体分離_仕分け
CLEANING = PatentClassification.清掃
SOLID_WASTE_DISPOSAL = PatentClassification.固体廃棄物処理
MECHANICAL_METAL_WORKING = PatentClassification.機械的金属加工
CASTING_POWDER_METALLURGY = PatentClassification.鋳造_粉末冶金
MACHINE_TOOLS = PatentClassification.工作機械_金属加工
GRINDING_POLISHING = PatentClassification.研削_研磨
HAND_TOOLS = PatentClassification.手工具_動力工具
CUTTING_TOOLS = PatentClassification.切断手工具_切断機
WOOD_WORKING = PatentClassification.木材加工
CEMENT_CLAY_STONE = PatentClassification.セメント_粘土_石材加工
PLASTICS_WORKING = PatentClassification.プラスチック加工
PRESSES = PatentClassification.プレス
PAPER_PRODUCTS_MANUFACTURING = PatentClassification.紙_板紙製品の製造
LAYERED_PRODUCTS = PatentClassification.積層体
ADDITIVE_MANUFACTURING = PatentClassification.付加製造技術
PRINTING = PatentClassification.印刷_タイプライター
BOOKBINDING = PatentClassification.製本_アルバム
WRITING_DRAWING_IMPLEMENTS = PatentClassification.筆記_製図用器具
DECORATIVE_ARTS = PatentClassification.装飾技術
VEHICLES_GENERAL = PatentClassification.車両一般
RAILWAYS = PatentClassification.鉄道
LAND_VEHICLES = PatentClassification.路面車両
SHIPS = PatentClassification.船舶_水上構造物
AIRCRAFT_AVIATION = PatentClassification.航空機_宇宙工学
CONVEYING_PACKING_STORING = PatentClassification.運搬_包装_貯蔵
HOISTING_LIFTING = PatentClassification.巻上装置_揚重装置
BOTTLE_OPENING_LIQUID_HANDLING = PatentClassification.容器開封密封_液体取扱い
SADDLERY_UPHOLSTERY = PatentClassification.馬具_詰め物
MICROSTRUCTURAL_TECHNOLOGY = PatentClassification.マイクロ構造技術
NANOTECHNOLOGY = PatentClassification.ナノテクノロジー
SECTION_B_OTHER = PatentClassification.セクションB_その他
INORGANIC_CHEMISTRY = PatentClassification.無機化学
WATER_TREATMENT = PatentClassification.水_廃水処理
GLASS_MINERAL_WOOL = PatentClassification.ガラス_鉱物
CEMENTS_CERAMICS = PatentClassification.セメント_コンクリート_セラミックス
FERTILISERS = PatentClassification.肥料
EXPLOSIVES_MATCHES = PatentClassification.火薬_マッチ
ORGANIC_CHEMISTRY = PatentClassification.有機化学
ORGANIC_MACROMOLECULAR = PatentClassification.有機高分子化合物
DYES_PAINTS_ADHESIVES = PatentClassification.染料_ペイント_接着剤
PETROLEUM_GAS_COKE = PatentClassification.石油_ガス_コークス工業
ANIMAL_VEGETABLE_OILS = PatentClassification.油脂_洗浄剤
BIOCHEMISTRY_MICROBIOLOGY = PatentClassification.生化学_微生物学
SUGAR_INDUSTRY = PatentClassification.糖工業
SKINS_LEATHER = PatentClassification.皮革
IRON_METALLURGY = PatentClassification.鉄冶金
METALLURGY_ALLOYS = PatentClassification.冶金_合金
METALLIC_COATING = PatentClassification.金属被覆_表面処理
ELECTROLYSIS = PatentClassification.電気分解_電気泳動
CRYSTAL_GROWTH = PatentClassification.結晶成長
COMBINATORIAL_TECHNOLOGY = PatentClassification.コンビナトリアル技術
SECTION_C_OTHER = PatentClassification.セクションC_その他
THREADS_FIBRES_SPINNING = PatentClassification.糸_繊維_紡績
YARNS_ROPES = PatentClassification.糸_ロープ仕上げ
WEAVING = PatentClassification.織成
BRAIDING_KNITTING = PatentClassification.組みひも_メリヤス編成
SEWING_EMBROIDERING = PatentClassification.縫製_刺しゅう
TEXTILE_TREATMENT = PatentClassification.繊維処理_洗濯
ROPES_CABLES = PatentClassification.ロープ_ケーブル
PAPER_MAKING = PatentClassification.製紙_セルロース
SECTION_D_OTHER = PatentClassification.セクションD_その他
ROAD_RAILWAY_BRIDGE_CONSTRUCTION = PatentClassification.道路_鉄道_橋りょう建設
HYDRAULIC_ENGINEERING = PatentClassification.水工_基礎_土砂移送
WATER_SUPPLY_SEWERAGE = PatentClassification.上水_下水
BUILDING = PatentClassification.建築物
LOCKS_KEYS_SAFES = PatentClassification.錠_鍵_金庫
DOORS_WINDOWS = PatentClassification.戸_窓_シャッタ
EARTH_DRILLING_MINING = PatentClassification.削孔_採鉱
SECTION_E_OTHER = PatentClassification.セクションE_その他
ENGINES_GENERAL = PatentClassification.機関一般_蒸気機関
COMBUSTION_ENGINES = PatentClassification.燃焼機関
LIQUID_MACHINES_WIND_MOTORS = PatentClassification.液体用機関_風力原動機
PUMPS = PatentClassification.容積形機械_ポンプ
FLUID_PRESSURE_ACTUATORS = PatentClassification.流体圧アクチュエータ
ENGINEERING_ELEMENTS = PatentClassification.機械要素
GAS_LIQUID_STORAGE = PatentClassification.ガス_液体の貯蔵分配
LIGHTING = PatentClassification.照明
STEAM_GENERATION = PatentClassification.蒸気発生
COMBUSTION_APPARATUS = PatentClassification.燃焼装置
HEATING_VENTILATING = PatentClassification.加熱_レンジ_換気
REFRIGERATION_COOLING = PatentClassification.冷凍_冷却_ヒートポンプ
DRYING = PatentClassification.乾燥
FURNACES_KILNS = PatentClassification.炉_キルン_レトルト
HEAT_EXCHANGE = PatentClassification.熱交換
WEAPONS = PatentClassification.武器
AMMUNITION_BLASTING = PatentClassification.弾薬_爆破
SECTION_F_OTHER = PatentClassification.セクションF_その他
MEASURING_TESTING = PatentClassification.測定_試験
OPTICS = PatentClassification.光学
PHOTOGRAPHY_CINEMATOGRAPHY = PatentClassification.写真_映画_ホログラフイ
HOROLOGY = PatentClassification.時計
CONTROLLING_REGULATING = PatentClassification.制御_調整
COMPUTING_CALCULATING = PatentClassification.計算_計数
CHECKING_DEVICES = PatentClassification.チェック装置
SIGNALLING = PatentClassification.信号
EDUCATION_CRYPTOGRAPHY_DISPLAY = PatentClassification.教育_暗号方法_表示_広告
MUSICAL_INSTRUMENTS_ACOUSTICS = PatentClassification.楽器_音響
INFORMATION_STORAGE = PatentClassification.情報記憶
INSTRUMENT_DETAILS = PatentClassification.器械の細部
ICT_SPECIFIC_APPLICATIONS = PatentClassification.情報通信技術_ICT
NUCLEAR_PHYSICS = PatentClassification.核物理_核工学
SECTION_G_OTHER = PatentClassification.セクションG_その他
ELECTRIC_ELEMENTS = PatentClassification.基本的電気素子
ELECTRIC_POWER = PatentClassification.電力の発電_変換_配電
ELECTRONIC_CIRCUITRY = PatentClassification.基本電子回路
ELECTRIC_COMMUNICATION = PatentClassification.電気通信技術
ELECTRIC_TECHNIQUES = PatentClassification.電気技術
SECTION_H_OTHER = PatentClassification.セクションH_その他


class DesignClassification(StrEnum):
    """意匠の日本意匠分類の列挙型。

    日本意匠分類に基づく分類コードを定義する。
    ``description_ja`` プロパティで日本語の分類名を取得できる。
    """

    製造食品及び嗜好品_その他 = "A0"
    製造食品及び嗜好品 = "A1"
    衣服及び身の回り品_その他 = "B0"
    衣服 = "B1"
    服飾品 = "B2"
    身の回り品 = "B3"
    かばん_携帯用袋物 = "B4"
    履物 = "B5"
    喫煙用具_点火器 = "B6"
    化粧用具_理容用具 = "B7"
    衣服及び身の回り品_汎用部品 = "B9"
    生活用品_その他 = "C0"
    寝具_床敷物_カーテン = "C1"
    室内装飾品 = "C2"
    清掃用具_洗濯用具 = "C3"
    家庭用保健衛生用品 = "C4"
    飲食用容器_調理用容器 = "C5"
    飲食用具_調理用器具 = "C6"
    慶弔用品 = "C7"
    住宅設備用品_その他 = "D0"
    発光具_照明器具 = "D3"
    暖冷房機_空調換気機器 = "D4"
    厨房設備用品_衛生設備用品 = "D5"
    室内整理用家具_用具 = "D6"
    家具 = "D7"
    住宅設備用品_汎用部品 = "D9"
    趣味娯楽_運動競技用品_その他 = "E0"
    おもちゃ = "E1"
    遊戯娯楽用品 = "E2"
    運動競技用品 = "E3"
    楽器 = "E4"
    事務用品_販売用品_その他 = "F0"
    教習具_書画用品 = "F1"
    筆記具_事務用具 = "F2"
    事務用紙製品_印刷物 = "F3"
    包装紙_包装用容器 = "F4"
    広告用具_表示具_商品陳列用具 = "F5"
    運輸_運搬機械_その他 = "G0"
    運搬_昇降_貨物取扱い機械器具 = "G1"
    車両 = "G2"
    船舶 = "G3"
    航空機 = "G4"
    電気電子_通信機械器具_その他 = "H0"
    基本的電気素子 = "H1"
    回転電気機械_配電機械器具 = "H2"
    電子情報処理_記憶機械器具 = "H6"
    電子情報入出力機器 = "H7"
    一般機械器具_その他 = "J0"
    計量器_測定機械器具 = "J1"
    時計 = "J2"
    光学機械器具 = "J3"
    事務用機械器具 = "J4"
    自動販売機_自動サービス機 = "J5"
    保安機械器具 = "J6"
    医療機械器具 = "J7"
    産業用機械器具_その他 = "K0"
    利器_工具 = "K1"
    漁業用機械器具 = "K2"
    農業用機械器具_建設機械 = "K3"
    食料加工機械 = "K4"
    繊維機械_ミシン = "K5"
    化学機械器具 = "K6"
    金属加工機械_木材加工機械 = "K7"
    動力機械器具_ポンプ = "K8"
    産業用機械器具_汎用部品 = "K9"
    土木建築用品_その他 = "L0"
    仮設工事用品 = "L1"
    土木構造物_土木用品 = "L2"
    組立て家屋_屋外装備品 = "L3"
    建築用構成品 = "L4"
    建築用内外装材 = "L6"
    建物用構造材_枠材 = "L7"
    基礎製品_その他 = "M0"
    織物地_板_ひも = "M1"
    配線配管用管_バルブ = "M2"
    ねじ_くぎ_金物 = "M3"
    物品_その他 = "N0"
    ソフトウェア = "N1"
    ウェブサイト = "N2"
    画像_その他 = "W10"
    情報入力操作用画像 = "W11"
    機能実行操作用画像 = "W12"
    情報閲覧表示用画像 = "W13"
    複合画像 = "W14"
    画像構成部品 = "W19"

    @property
    def description_ja(self) -> str:
        """日本語の分類名を返す。

        Returns:
            日本語の分類名文字列。
        """
        return _DESIGN_DESC_JA[self]


_DESIGN_DESC_JA: dict[DesignClassification, str] = {
    DesignClassification.製造食品及び嗜好品_その他: "A1に属さないその他の製造食品及び嗜好品",
    DesignClassification.製造食品及び嗜好品: "製造食品及び嗜好品",
    DesignClassification.衣服及び身の回り品_その他: "B1～B9に属さないその他の衣服及び身の回り品",
    DesignClassification.衣服: "衣服",
    DesignClassification.服飾品: "服飾品",
    DesignClassification.身の回り品: "身の回り品",
    DesignClassification.かばん_携帯用袋物: "かばん又は携帯用袋物",
    DesignClassification.履物: "履物",
    DesignClassification.喫煙用具_点火器: "喫煙用具及び点火器",
    DesignClassification.化粧用具_理容用具: "化粧用具又は理容用具",
    DesignClassification.衣服及び身の回り品_汎用部品: "衣服及び身の回り品汎用部品及び付属品",
    DesignClassification.生活用品_その他: "C1～C7に属さないその他の生活用品",
    DesignClassification.寝具_床敷物_カーテン: "寝具、床敷物、カーテン等",
    DesignClassification.室内装飾品: "室内装飾品",
    DesignClassification.清掃用具_洗濯用具: "清掃用具、洗濯用具等",
    DesignClassification.家庭用保健衛生用品: "家庭用保健衛生用品",
    DesignClassification.飲食用容器_調理用容器: "飲食用容器又は調理用容器",
    DesignClassification.飲食用具_調理用器具: "飲食用具及び調理用器具",
    DesignClassification.慶弔用品: "慶弔用品",
    DesignClassification.住宅設備用品_その他: "D3～D9に属さないその他の住宅設備用品",
    DesignClassification.発光具_照明器具: "発光具及び照明器具",
    DesignClassification.暖冷房機_空調換気機器: "暖冷房機又は空調換気機器",
    DesignClassification.厨房設備用品_衛生設備用品: "厨房設備用品及び衛生設備用品",
    DesignClassification.室内整理用家具_用具: "室内整理用家具・用具",
    DesignClassification.家具: "家具",
    DesignClassification.住宅設備用品_汎用部品: "住宅設備用品汎用部品及び付属品",
    DesignClassification.趣味娯楽_運動競技用品_その他: "E1～E4に属さないその他の趣味娯楽用品及び運動競技用品",
    DesignClassification.おもちゃ: "おもちゃ",
    DesignClassification.遊戯娯楽用品: "遊戯娯楽用品",
    DesignClassification.運動競技用品: "運動競技用品",
    DesignClassification.楽器: "楽器",
    DesignClassification.事務用品_販売用品_その他: "F1～F5に属さないその他の事務用品及び販売用品",
    DesignClassification.教習具_書画用品: "教習具、書画用品等",
    DesignClassification.筆記具_事務用具: "筆記具、事務用具等",
    DesignClassification.事務用紙製品_印刷物: "事務用紙製品、印刷物等",
    DesignClassification.包装紙_包装用容器: "包装紙、包装用容器等",
    DesignClassification.広告用具_表示具_商品陳列用具: "広告用具、表示具及び商品陳列用具",
    DesignClassification.運輸_運搬機械_その他: "G1～G4に属さないその他の運輸又は運搬機械",
    DesignClassification.運搬_昇降_貨物取扱い機械器具: "運搬、昇降又は貨物取扱い用機械器具",
    DesignClassification.車両: "車両",
    DesignClassification.船舶: "船舶",
    DesignClassification.航空機: "航空機",
    DesignClassification.電気電子_通信機械器具_その他: "H1～H7に属さないその他の電気・電子機械器具及び通信機械器具",
    DesignClassification.基本的電気素子: "基本的電気素子",
    DesignClassification.回転電気機械_配電機械器具: "回転電気機械、配電機械器具",
    DesignClassification.電子情報処理_記憶機械器具: "電子情報処理・記憶機械器具",
    DesignClassification.電子情報入出力機器: "電子情報入出力機器",
    DesignClassification.一般機械器具_その他: "J1～J7に属さないその他の一般機械器具",
    DesignClassification.計量器_測定機械器具: "計量器、測定機械器具及び測量機械器具",
    DesignClassification.時計: "時計",
    DesignClassification.光学機械器具: "光学機械器具",
    DesignClassification.事務用機械器具: "事務用機械器具",
    DesignClassification.自動販売機_自動サービス機: "自動販売機及び自動サービス機",
    DesignClassification.保安機械器具: "保安機械器具等",
    DesignClassification.医療機械器具: "医療機械器具",
    DesignClassification.産業用機械器具_その他: "K1～K9に属さないその他の産業用機械器具",
    DesignClassification.利器_工具: "利器及び工具",
    DesignClassification.漁業用機械器具: "漁業用機械器具",
    DesignClassification.農業用機械器具_建設機械: "農業用機械器具、鉱山機械、建設機械等",
    DesignClassification.食料加工機械: "食料加工機械等",
    DesignClassification.繊維機械_ミシン: "繊維機械及びミシン",
    DesignClassification.化学機械器具: "化学機械器具",
    DesignClassification.金属加工機械_木材加工機械: "金属加工機械、木材加工機械等",
    DesignClassification.動力機械器具_ポンプ: "動力機械器具、ポンプ、圧縮機、送風機等",
    DesignClassification.産業用機械器具_汎用部品: "産業用機械器具汎用部品及び付属品",
    DesignClassification.土木建築用品_その他: "L1～L7に属さないその他の土木建築用品",
    DesignClassification.仮設工事用品: "仮設工事用品",
    DesignClassification.土木構造物_土木用品: "土木構造物及び土木用品",
    DesignClassification.組立て家屋_屋外装備品: "組立て家屋、屋外装備品等",
    DesignClassification.建築用構成品: "建築用構成品",
    DesignClassification.建築用内外装材: "建築用内外装材",
    DesignClassification.建物用構造材_枠材: "建物用構造材、枠材等",
    DesignClassification.基礎製品_その他: "M1～M3に属さないその他の基礎製品",
    DesignClassification.織物地_板_ひも: "織物地、板、ひも等",
    DesignClassification.配線配管用管_バルブ: "配線・配管用管、管継ぎ手、バルブ等",
    DesignClassification.ねじ_くぎ_金物: "ねじ、くぎ、開閉金物、係止具等",
    DesignClassification.物品_その他: "N1、N2に属さないその他の物品等",
    DesignClassification.ソフトウェア: "ソフトウェア",
    DesignClassification.ウェブサイト: "ウェブサイト",
    DesignClassification.画像_その他: "W11～W19に属さないその他の画像",
    DesignClassification.情報入力操作用画像: "情報入力操作用画像",
    DesignClassification.機能実行操作用画像: "機能実行操作用画像",
    DesignClassification.情報閲覧表示用画像: "情報閲覧表示用画像",
    DesignClassification.複合画像: "複合画像",
    DesignClassification.画像構成部品: "画像構成部品",
}




# DesignClassification 英語 alias
DESIGN_FOOD_OTHER = DesignClassification.製造食品及び嗜好品_その他
DESIGN_FOOD = DesignClassification.製造食品及び嗜好品
DESIGN_CLOTHING_ACCESSORIES_OTHER = DesignClassification.衣服及び身の回り品_その他
DESIGN_CLOTHING = DesignClassification.衣服
DESIGN_FASHION = DesignClassification.服飾品
DESIGN_PERSONAL_ITEMS = DesignClassification.身の回り品
DESIGN_BAGS = DesignClassification.かばん_携帯用袋物
DESIGN_FOOTWEAR = DesignClassification.履物
DESIGN_SMOKING = DesignClassification.喫煙用具_点火器
DESIGN_COSMETICS = DesignClassification.化粧用具_理容用具
DESIGN_CLOTHING_PARTS = DesignClassification.衣服及び身の回り品_汎用部品
DESIGN_HOUSEHOLD_OTHER = DesignClassification.生活用品_その他
DESIGN_BEDDING = DesignClassification.寝具_床敷物_カーテン
DESIGN_INTERIOR_DECOR = DesignClassification.室内装飾品
DESIGN_CLEANING = DesignClassification.清掃用具_洗濯用具
DESIGN_HEALTH_HYGIENE = DesignClassification.家庭用保健衛生用品
DESIGN_FOOD_CONTAINERS = DesignClassification.飲食用容器_調理用容器
DESIGN_TABLEWARE = DesignClassification.飲食用具_調理用器具
DESIGN_CEREMONIAL = DesignClassification.慶弔用品
DESIGN_HOME_EQUIPMENT_OTHER = DesignClassification.住宅設備用品_その他
DESIGN_LIGHTING = DesignClassification.発光具_照明器具
DESIGN_HVAC = DesignClassification.暖冷房機_空調換気機器
DESIGN_KITCHEN_SANITARY = DesignClassification.厨房設備用品_衛生設備用品
DESIGN_STORAGE_FURNITURE = DesignClassification.室内整理用家具_用具
DESIGN_FURNITURE = DesignClassification.家具
DESIGN_HOME_EQUIPMENT_PARTS = DesignClassification.住宅設備用品_汎用部品
DESIGN_HOBBY_SPORTS_OTHER = DesignClassification.趣味娯楽_運動競技用品_その他
DESIGN_TOYS = DesignClassification.おもちゃ
DESIGN_GAMES = DesignClassification.遊戯娯楽用品
DESIGN_SPORTS = DesignClassification.運動競技用品
DESIGN_MUSICAL_INSTRUMENTS = DesignClassification.楽器
DESIGN_OFFICE_SALES_OTHER = DesignClassification.事務用品_販売用品_その他
DESIGN_EDUCATIONAL_ART = DesignClassification.教習具_書画用品
DESIGN_WRITING_OFFICE = DesignClassification.筆記具_事務用具
DESIGN_PAPER_PRODUCTS = DesignClassification.事務用紙製品_印刷物
DESIGN_PACKAGING = DesignClassification.包装紙_包装用容器
DESIGN_ADVERTISING_DISPLAY = DesignClassification.広告用具_表示具_商品陳列用具
DESIGN_TRANSPORT_OTHER = DesignClassification.運輸_運搬機械_その他
DESIGN_MATERIAL_HANDLING = DesignClassification.運搬_昇降_貨物取扱い機械器具
DESIGN_VEHICLES = DesignClassification.車両
DESIGN_SHIPS = DesignClassification.船舶
DESIGN_AIRCRAFT = DesignClassification.航空機
DESIGN_ELECTRONICS_OTHER = DesignClassification.電気電子_通信機械器具_その他
DESIGN_ELECTRIC_ELEMENTS = DesignClassification.基本的電気素子
DESIGN_ELECTRICAL_MACHINES = DesignClassification.回転電気機械_配電機械器具
DESIGN_COMPUTERS = DesignClassification.電子情報処理_記憶機械器具
DESIGN_IO_DEVICES = DesignClassification.電子情報入出力機器
DESIGN_GENERAL_MACHINERY_OTHER = DesignClassification.一般機械器具_その他
DESIGN_MEASURING = DesignClassification.計量器_測定機械器具
DESIGN_CLOCKS = DesignClassification.時計
DESIGN_OPTICAL = DesignClassification.光学機械器具
DESIGN_OFFICE_MACHINES = DesignClassification.事務用機械器具
DESIGN_VENDING_MACHINES = DesignClassification.自動販売機_自動サービス機
DESIGN_SECURITY = DesignClassification.保安機械器具
DESIGN_MEDICAL = DesignClassification.医療機械器具
DESIGN_INDUSTRIAL_OTHER = DesignClassification.産業用機械器具_その他
DESIGN_TOOLS = DesignClassification.利器_工具
DESIGN_FISHING = DesignClassification.漁業用機械器具
DESIGN_AGRICULTURAL_CONSTRUCTION = DesignClassification.農業用機械器具_建設機械
DESIGN_FOOD_PROCESSING = DesignClassification.食料加工機械
DESIGN_TEXTILE_MACHINES = DesignClassification.繊維機械_ミシン
DESIGN_CHEMICAL_EQUIPMENT = DesignClassification.化学機械器具
DESIGN_METALWORKING = DesignClassification.金属加工機械_木材加工機械
DESIGN_POWER_MACHINES = DesignClassification.動力機械器具_ポンプ
DESIGN_INDUSTRIAL_PARTS = DesignClassification.産業用機械器具_汎用部品
DESIGN_CIVIL_BUILDING_OTHER = DesignClassification.土木建築用品_その他
DESIGN_TEMPORARY_CONSTRUCTION = DesignClassification.仮設工事用品
DESIGN_CIVIL_STRUCTURES = DesignClassification.土木構造物_土木用品
DESIGN_PREFAB_OUTDOOR = DesignClassification.組立て家屋_屋外装備品
DESIGN_BUILDING_COMPONENTS = DesignClassification.建築用構成品
DESIGN_BUILDING_MATERIALS = DesignClassification.建築用内外装材
DESIGN_STRUCTURAL_MATERIALS = DesignClassification.建物用構造材_枠材
DESIGN_BASIC_PRODUCTS_OTHER = DesignClassification.基礎製品_その他
DESIGN_TEXTILES_BOARDS = DesignClassification.織物地_板_ひも
DESIGN_PIPES_VALVES = DesignClassification.配線配管用管_バルブ
DESIGN_FASTENERS = DesignClassification.ねじ_くぎ_金物
DESIGN_OTHER_GOODS = DesignClassification.物品_その他
DESIGN_SOFTWARE = DesignClassification.ソフトウェア
DESIGN_WEBSITE = DesignClassification.ウェブサイト
DESIGN_IMAGES_OTHER = DesignClassification.画像_その他
DESIGN_INPUT_IMAGES = DesignClassification.情報入力操作用画像
DESIGN_FUNCTION_IMAGES = DesignClassification.機能実行操作用画像
DESIGN_DISPLAY_IMAGES = DesignClassification.情報閲覧表示用画像
DESIGN_COMPOSITE_IMAGES = DesignClassification.複合画像
DESIGN_IMAGE_COMPONENTS = DesignClassification.画像構成部品


class TrademarkClassification(StrEnum):
    """商標の類似商品・役務審査基準に基づく区分の列挙型。

    ニース国際分類に対応する第1類～第45類の区分コードを定義する。
    第1類～第34類は商品区分、第35類～第45類は役務区分に相当する。
    ``description_ja`` プロパティで日本語の区分名を取得できる。
    """

    化学品 = "1"
    塗料_着色料 = "2"
    洗浄剤_化粧品 = "3"
    工業用油_燃料 = "4"
    薬剤 = "5"
    卑金属_製品 = "6"
    加工機械_原動機 = "7"
    手動工具 = "8"
    科学用機械器具 = "9"
    医療用機械器具 = "10"
    照明_加熱_冷却装置 = "11"
    乗物_移動装置 = "12"
    火器_火工品 = "13"
    貴金属_宝飾品_時計 = "14"
    楽器 = "15"
    紙_事務用品 = "16"
    絶縁_断熱材料 = "17"
    革_旅行用品_馬具 = "18"
    建築材料 = "19"
    家具_プラスチック製品 = "20"
    家庭用器具_ガラス_磁器 = "21"
    ロープ_帆布_繊維 = "22"
    織物用の糸 = "23"
    織物_織物製カバー = "24"
    被服_履物 = "25"
    裁縫用品 = "26"
    床敷物_壁掛け = "27"
    がん具_遊戯用具_運動用具 = "28"
    動物性食品_加工野菜 = "29"
    植物性食品_調味料 = "30"
    陸産物_動植物_飼料 = "31"
    ノンアルコール飲料_ビール = "32"
    アルコール飲料 = "33"
    たばこ_喫煙用具 = "34"
    広告_事業管理 = "35"
    金融_保険_不動産 = "36"
    建設_修理 = "37"
    電気通信 = "38"
    輸送_保管_旅行手配 = "39"
    物品の加工処理 = "40"
    教育_娯楽_スポーツ = "41"
    科学技術_ソフトウェア開発 = "42"
    飲食物_宿泊施設 = "43"
    医療_美容_農林業 = "44"
    冠婚葬祭_警備_法律 = "45"

    @property
    def description_ja(self) -> str:
        """日本語の区分名を返す。

        Returns:
            日本語の区分名文字列。
        """
        return _TRADEMARK_DESC_JA[self]


_TRADEMARK_DESC_JA: dict[TrademarkClassification, str] = {
    TrademarkClassification.化学品: "工業用、科学用又は農業用の化学品",
    TrademarkClassification.塗料_着色料: "塗料、着色料及び腐食の防止用の調製品",
    TrademarkClassification.洗浄剤_化粧品: "洗浄剤及び化粧品",
    TrademarkClassification.工業用油_燃料: "工業用油、工業用油脂、燃料及び光剤",
    TrademarkClassification.薬剤: "薬剤",
    TrademarkClassification.卑金属_製品: "卑金属及びその製品",
    TrademarkClassification.加工機械_原動機: "加工機械、原動機(陸上の乗物用のものを除く。)その他の機械",
    TrademarkClassification.手動工具: "手動工具",
    TrademarkClassification.科学用機械器具: "科学用、航海用、測量用、写真用、音響用、映像用、計量用、信号用、検査用、救命用、教育用、計算用又は情報処理用の機械器具、光学式の機械器具及び電気の伝導用、電気回路の開閉用、変圧用、蓄電用、電圧調整用又は電気制御用の機械器具",
    TrademarkClassification.医療用機械器具: "医療用機械器具及び医療用品",
    TrademarkClassification.照明_加熱_冷却装置: "照明用、加熱用、蒸気発生用、調理用、冷却用、乾燥用、換気用、給水用又は衛生用の装置",
    TrademarkClassification.乗物_移動装置: "乗物その他移動用の装置",
    TrademarkClassification.火器_火工品: "火器及び火工品",
    TrademarkClassification.貴金属_宝飾品_時計: "貴金属、貴金属製品であって他の類に属しないもの、宝飾品及び時計",
    TrademarkClassification.楽器: "楽器",
    TrademarkClassification.紙_事務用品: "紙、紙製品及び事務用品",
    TrademarkClassification.絶縁_断熱材料: "電気絶縁用、断熱用又は防音用の材料及び材料用のプラスチック",
    TrademarkClassification.革_旅行用品_馬具: "革及びその模造品、旅行用品並びに馬具",
    TrademarkClassification.建築材料: "金属製でない建築材料",
    TrademarkClassification.家具_プラスチック製品: "家具及びプラスチック製品であって他の類に属しないもの",
    TrademarkClassification.家庭用器具_ガラス_磁器: "家庭用又は台所用の手動式の器具、化粧用具、ガラス製品及び磁器製品",
    TrademarkClassification.ロープ_帆布_繊維: "ロープ製品、帆布製品、詰物用の材料及び織物用の原料繊維",
    TrademarkClassification.織物用の糸: "織物用の糸",
    TrademarkClassification.織物_織物製カバー: "織物及び家庭用の織物製カバー",
    TrademarkClassification.被服_履物: "被服及び履物",
    TrademarkClassification.裁縫用品: "裁縫用品",
    TrademarkClassification.床敷物_壁掛け: "床敷物及び織物製でない壁掛け",
    TrademarkClassification.がん具_遊戯用具_運動用具: "がん具、遊戯用具及び運動用具",
    TrademarkClassification.動物性食品_加工野菜: "動物性の食品及び加工した野菜その他の食用園芸作物",
    TrademarkClassification.植物性食品_調味料: "加工した植物性の食品(他の類に属するものを除く。)及び調味料",
    TrademarkClassification.陸産物_動植物_飼料: "加工していない陸産物、生きている動植物及び飼料",
    TrademarkClassification.ノンアルコール飲料_ビール: "アルコールを含有しない飲料及びビール",
    TrademarkClassification.アルコール飲料: "ビールを除くアルコール飲料",
    TrademarkClassification.たばこ_喫煙用具: "たばこ、喫煙用具及びマッチ",
    TrademarkClassification.広告_事業管理: "広告、事業の管理又は運営及び事務処理及び小売又は卸売の業務において行われる顧客に対する便益の提供",
    TrademarkClassification.金融_保険_不動産: "金融、保険及び不動産の取引",
    TrademarkClassification.建設_修理: "建設、設置工事及び修理",
    TrademarkClassification.電気通信: "電気通信",
    TrademarkClassification.輸送_保管_旅行手配: "輸送、こん包及び保管並びに旅行の手配",
    TrademarkClassification.物品の加工処理: "物品の加工その他の処理",
    TrademarkClassification.教育_娯楽_スポーツ: "教育、訓練、娯楽、スポーツ及び文化活動",
    TrademarkClassification.科学技術_ソフトウェア開発: "科学技術又は産業に関する調査研究及び設計並びに電子計算機又はソフトウェアの設計及び開発",
    TrademarkClassification.飲食物_宿泊施設: "飲食物の提供及び宿泊施設の提供",
    TrademarkClassification.医療_美容_農林業: "医療、動物の治療、人又は動物に関する衛生及び美容並びに農業、園芸又は林業に係る役務",
    TrademarkClassification.冠婚葬祭_警備_法律: "冠婚葬祭に係る役務その他の個人の需要に応じて提供する役務(他の類に属するものを除く。)、警備及び法律事務",
}




# TrademarkClassification 英語 alias
TM_CHEMICALS = TrademarkClassification.化学品
TM_PAINTS_COATINGS = TrademarkClassification.塗料_着色料
TM_CLEANING_COSMETICS = TrademarkClassification.洗浄剤_化粧品
TM_OILS_FUELS = TrademarkClassification.工業用油_燃料
TM_PHARMACEUTICALS = TrademarkClassification.薬剤
TM_BASE_METALS = TrademarkClassification.卑金属_製品
TM_MACHINES_ENGINES = TrademarkClassification.加工機械_原動機
TM_HAND_TOOLS = TrademarkClassification.手動工具
TM_SCIENTIFIC_INSTRUMENTS = TrademarkClassification.科学用機械器具
TM_MEDICAL_INSTRUMENTS = TrademarkClassification.医療用機械器具
TM_LIGHTING_HEATING_COOLING = TrademarkClassification.照明_加熱_冷却装置
TM_VEHICLES = TrademarkClassification.乗物_移動装置
TM_FIREARMS = TrademarkClassification.火器_火工品
TM_PRECIOUS_METALS_JEWELLERY = TrademarkClassification.貴金属_宝飾品_時計
TM_MUSICAL_INSTRUMENTS = TrademarkClassification.楽器
TM_PAPER_OFFICE = TrademarkClassification.紙_事務用品
TM_INSULATING_MATERIALS = TrademarkClassification.絶縁_断熱材料
TM_LEATHER_TRAVEL = TrademarkClassification.革_旅行用品_馬具
TM_BUILDING_MATERIALS = TrademarkClassification.建築材料
TM_FURNITURE_PLASTICS = TrademarkClassification.家具_プラスチック製品
TM_HOUSEHOLD_UTENSILS = TrademarkClassification.家庭用器具_ガラス_磁器
TM_ROPES_TEXTILES = TrademarkClassification.ロープ_帆布_繊維
TM_YARNS = TrademarkClassification.織物用の糸
TM_TEXTILES_COVERS = TrademarkClassification.織物_織物製カバー
TM_CLOTHING_FOOTWEAR = TrademarkClassification.被服_履物
TM_SEWING = TrademarkClassification.裁縫用品
TM_FLOOR_WALL_COVERINGS = TrademarkClassification.床敷物_壁掛け
TM_TOYS_GAMES_SPORTS = TrademarkClassification.がん具_遊戯用具_運動用具
TM_ANIMAL_FOODS = TrademarkClassification.動物性食品_加工野菜
TM_PLANT_FOODS = TrademarkClassification.植物性食品_調味料
TM_RAW_AGRICULTURAL = TrademarkClassification.陸産物_動植物_飼料
TM_NON_ALCOHOLIC = TrademarkClassification.ノンアルコール飲料_ビール
TM_ALCOHOLIC = TrademarkClassification.アルコール飲料
TM_TOBACCO = TrademarkClassification.たばこ_喫煙用具
TM_ADVERTISING = TrademarkClassification.広告_事業管理
TM_FINANCE_INSURANCE = TrademarkClassification.金融_保険_不動産
TM_CONSTRUCTION_REPAIR = TrademarkClassification.建設_修理
TM_TELECOMMUNICATIONS = TrademarkClassification.電気通信
TM_TRANSPORT_STORAGE = TrademarkClassification.輸送_保管_旅行手配
TM_MATERIAL_TREATMENT = TrademarkClassification.物品の加工処理
TM_EDUCATION_ENTERTAINMENT = TrademarkClassification.教育_娯楽_スポーツ
TM_TECHNOLOGY_SOFTWARE = TrademarkClassification.科学技術_ソフトウェア開発
TM_FOOD_ACCOMMODATION = TrademarkClassification.飲食物_宿泊施設
TM_MEDICAL_BEAUTY = TrademarkClassification.医療_美容_農林業
TM_CEREMONIES_SECURITY_LAW = TrademarkClassification.冠婚葬祭_警備_法律
