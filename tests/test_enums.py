"""Enum 値の網羅テスト。"""

from __future__ import annotations

from gbizinfo.enums import (
    AverageAge,
    AverageContinuousServiceYears,
    BusinessItem,
    CorporateType,
    DesignClassification,
    FemaleWorkersProportion,
    Ministry,
    MonthAverageOvertimeHours,
    PatentClassification,
    PatentType,
    Prefecture,
    QualificationType,
    Region,
    Source,
    TrademarkClassification,
)


class TestCorporateType:
    def test_member_count(self):
        assert len(CorporateType) == 10

    def test_values(self):
        assert CorporateType.株式会社.value == "301"
        assert CorporateType.国の機関.value == "101"
        assert CorporateType.その他.value == "499"

    def test_english_alias(self):
        from gbizinfo.enums.corporate_type import KABUSHIKI_KAISHA
        assert KABUSHIKI_KAISHA is CorporateType.株式会社


class TestPrefecture:
    def test_member_count(self):
        assert len(Prefecture) == 47

    def test_values(self):
        assert Prefecture.北海道.value == "01"
        assert Prefecture.東京都.value == "13"
        assert Prefecture.沖縄県.value == "47"

    def test_english_alias(self):
        from gbizinfo.enums.prefecture import TOKYO
        assert TOKYO is Prefecture.東京都


class TestRegion:
    def test_member_count(self):
        assert len(Region) == 10

    def test_prefectures_property(self):
        assert Prefecture.東京都 in Region.関東.prefectures
        assert Prefecture.北海道 in Region.北海道.prefectures
        assert Prefecture.沖縄県 in Region.沖縄.prefectures

    def test_all_prefectures_covered(self):
        all_prefs = set()
        for region in Region:
            all_prefs.update(region.prefectures)
        assert len(all_prefs) == 47


class TestSource:
    def test_member_count(self):
        assert len(Source) == 6

    def test_values(self):
        assert Source.調達.value == "1"
        assert Source.財務.value == "6"


class TestMinistry:
    def test_member_count(self):
        assert len(Ministry) == 49

    def test_values(self):
        assert Ministry.国税庁.value == "1"
        assert Ministry.こども家庭庁.value == "49"
        assert Ministry.国立研究開発法人新エネルギー産業技術総合開発機構.value == "30"


class TestBusinessItem:
    def test_member_count(self):
        """CODE.md の全56項目（製造27+販売27+役務15+買受2 = 71ではなく、欠番含め正確な数）。"""
        # 製造: 101-124, 127-129 = 27
        # 販売: 201-224, 227-229 = 27
        # 役務: 301-315 = 15
        # 買受: 401-402 = 2
        assert len(BusinessItem) == 71

    def test_qualification_type(self):
        assert BusinessItem.衣服その他繊維製品類_製造.qualification_type == QualificationType.物品の製造
        assert BusinessItem.衣服その他繊維製品類_販売.qualification_type == QualificationType.物品の販売
        assert BusinessItem.広告宣伝.qualification_type == QualificationType.役務の提供等
        assert BusinessItem.立木竹.qualification_type == QualificationType.物品の買受け


class TestWorkplace:
    def test_average_age(self):
        assert len(AverageAge) == 4
        assert AverageAge.歳30以下.value == "A"
        assert AverageAge.歳30以下.label == "～30歳"
        assert AverageAge.歳30以下.label_en == "30 or under"

    def test_service_years(self):
        assert len(AverageContinuousServiceYears) == 4

    def test_overtime(self):
        assert len(MonthAverageOvertimeHours) == 3
        assert MonthAverageOvertimeHours.時間40以上.value == "C"

    def test_female_proportion(self):
        assert len(FemaleWorkersProportion) == 4


class TestPatent:
    def test_patent_classification_count(self):
        assert len(PatentClassification) == 131

    def test_patent_description(self):
        assert PatentClassification.農業_林業_畜産.description_ja == "農業; 林業; 畜産; 狩猟; 捕獲; 漁業"
        assert "Agriculture" in PatentClassification.農業_林業_畜産.description_en

    def test_design_classification_count(self):
        assert len(DesignClassification) == 85

    def test_design_description(self):
        assert DesignClassification.製造食品及び嗜好品.description_ja == "製造食品及び嗜好品"
        assert DesignClassification.車両.description_ja == "車両"
        assert DesignClassification.ソフトウェア.description_ja == "ソフトウェア"

    def test_trademark_classification_count(self):
        assert len(TrademarkClassification) == 45

    def test_trademark_description(self):
        assert TrademarkClassification.化学品.description_ja == "工業用、科学用又は農業用の化学品"
        assert TrademarkClassification.電気通信.description_ja == "電気通信"
        assert TrademarkClassification.冠婚葬祭_警備_法律.description_ja.startswith("冠婚葬祭")

    def test_patent_type(self):
        assert len(PatentType) == 3
        assert PatentType.特許.value == "特許"


