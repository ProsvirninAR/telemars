from datetime import date, timedelta
from typing import Any, Optional, Sequence

import pytest

from telemars.filters import general as gflt
from telemars.params.filters import general as gval


class TestDateFilter:
    @pytest.mark.parametrize(
        'date_from, date_to, expected',
        [
            # Базовые сценарии.
            (date(2025, 1, 1), date(2025, 1, 31), [('2025-01-01', '2025-01-31')]),
            (date(2025, 2, 1), date(2025, 2, 28), [('2025-02-01', '2025-02-28')]),
            (date(2025, 3, 1), date(2025, 3, 7), [('2025-03-01', '2025-03-07')]),
            # Строка даты в ISO формате. Нежелательно, но допустимо.
            ('2025-05-01', '2025-05-31', [('2025-05-01', '2025-05-31')]),
            ('2025-07-07', '2025-07-31', [('2025-07-07', '2025-07-31')]),
            ('2025-01-01', '2025-01-01', [('2025-01-01', '2025-01-01')]),
        ],
    )
    def test_date_filter(self, date_from: date, date_to: date, expected: list[tuple[str, str]]) -> None:
        """Тест проверяет формирование выражения фильтра по дате для запроса к API."""
        assert gflt.DateFilter(date_from=date_from, date_to=date_to).expr == expected

    @pytest.mark.parametrize(
        'date_from, date_to',
        [
            (None, None),
            (date(2025, 1, 31), date(2025, 1, 1)),
            (date.today(), date.today() + timedelta(days=1)),
        ],
    )
    def test_date_filter_incorrect(self, date_from: Optional[date], date_to: Optional[date]) -> None:
        """Тест проверяет, что при передачи невалидных параметров в фильтр, поднимается исключение.

        Тестируемые сценарии:
        - Переданы пустые значения.
        - Дата начала периода позже даты окончания.
        - Дата окончания периода позже текущей даты.
        """
        with pytest.raises(ValueError):
            gflt.DateFilter(date_from=date_from, date_to=date_to)


class TestWeekdayFilter:
    @pytest.mark.parametrize(
        'research_week_day, expected',
        [
            (None, None),
            ([gval.Weekday.MONDAY], 'researchWeekDay = 1'),
            ([gval.Weekday.MONDAY, gval.Weekday.WEDNESDAY], 'researchWeekDay IN (1, 3)'),
            ([gval.Weekday.FRIDAY, gval.Weekday.SUNDAY], 'researchWeekDay IN (5, 7)'),
            ([gval.Weekday.TUESDAY, gval.Weekday.THURSDAY, gval.Weekday.SATURDAY], 'researchWeekDay IN (2, 4, 6)'),
        ],
    )
    def test_weekday_filter(self, research_week_day: Optional[Sequence[gval.Weekday]], expected: str) -> None:
        """Тест проверяет формирование выражения фильтра по дням недели для запроса к API."""
        assert gflt.WeekdayFilter(research_week_day=research_week_day).expr == expected

    @pytest.mark.parametrize(
        'research_week_day',
        [
            [],
            [None, 8, 9, 10],
            [gval.Weekday.MONDAY, gval.Weekday.MONDAY],
        ],
    )
    def test_weekday_filter_incorrect(self, research_week_day: Any) -> None:
        """Тест проверяет, что при передачи невалидных параметров в фильтр, поднимается исключение.

        Тестируемые сценарии:
        - Передан пустой список.
        - Передан список с недопустимыми значениями.
        - Переден список с дублирующимися значениями.
        """
        with pytest.raises(ValueError):
            gflt.WeekdayFilter(research_week_day=research_week_day)


class TestDaytypeFilter:
    @pytest.mark.parametrize(
        'research_day_type, expected',
        [
            ([gval.DayType.WEEKDAY], 'researchDayType = W'),
            ([gval.DayType.WEEKDAY, gval.DayType.WEEKEND], 'researchDayType IN (W, E)'),
            ([gval.DayType.WEEKEND, gval.DayType.HOLIDAY], 'researchDayType IN (E, H)'),
            ([gval.DayType.WEEKDAY, gval.DayType.MOURNING_DAY], 'researchDayType IN (W, F)'),
        ],
    )
    def test_daytype_filter(self, research_day_type: Optional[Sequence[gval.DayType]], expected: str) -> None:
        """Тест проверяет формирование выражения фильтра по типу дня для запроса к API."""
        assert gflt.DaytypeFilter(research_day_type=research_day_type).expr == expected

    @pytest.mark.parametrize(
        'research_day_type',
        [
            [],
            [None, 5, 6, 7],
            [gval.DayType.WEEKDAY, gval.DayType.WEEKDAY],
        ],
    )
    def test_daytype_filter_incorrect(self, research_day_type: Any) -> None:
        """Тест проверяет, что при передачи невалидных параметров в фильтр, поднимается исключение.

        Тестируемые сценарии:
        - Передан пустой список.
        - Передан список с недопустимыми значениями.
        - Переден список с дублирующимися значениями.
        """
        with pytest.raises(ValueError):
            gflt.DaytypeFilter(research_day_type=research_day_type)


class TestLocationFilter:
    @pytest.mark.parametrize(
        'location_id, expected',
        [
            (None, None),
            ([gval.Location.HOME], 'locationId = 1'),
            ([gval.Location.DACHA], 'locationId = 2'),
            ([gval.Location.OUT_OF_HOME], 'locationId = 4'),
            ([gval.Location.HOME, gval.Location.DACHA], 'locationId IN (1, 2)'),
            ([gval.Location.HOME, gval.Location.OUT_OF_HOME], 'locationId IN (1, 4)'),
        ],
    )
    def test_location_filter(self, location_id: Optional[Sequence[gval.Location]], expected: Optional[str]) -> None:
        """Тест проверяет формирование выражения фильтра по месту просмотра для запроса к API."""
        assert gflt.LocationFilter(location_id=location_id).expr == expected

    @pytest.mark.parametrize(
        'location_id',
        [
            [],
            [None, 0, 5, 6],
            [gval.Location.HOME, gval.Location.HOME],
        ],
    )
    def test_location_filter_incorrect(self, location_id: Any) -> None:
        """Тест проверяет, что при передачи невалидных параметров в фильтр, поднимается исключение."""
        with pytest.raises(ValueError):
            gflt.LocationFilter(location_id=location_id)


class TestCompanyFilter:
    @pytest.mark.parametrize(
        'tv_company_id, expected',
        [
            (None, None),
            ([1], 'tvCompanyId = 1'),
            ([1, 2], 'tvCompanyId IN (1, 2)'),
            ([5, 10, 15], 'tvCompanyId IN (5, 10, 15)'),
        ],
    )
    def test_tv_company_id_filter(self, tv_company_id: Optional[Sequence[int]], expected: Optional[str]) -> None:
        assert gflt.CompanyFilter(tv_company_id=tv_company_id).expr == expected

    @pytest.mark.parametrize(
        'tv_company_id',
        [
            [],
            [None, 'A', 'B', 'C'],
            [1, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        ],
    )
    def test_tv_company_id_filter_incorrect(self, tv_company_id: Any) -> None:
        with pytest.raises(ValueError):
            gflt.CompanyFilter(tv_company_id=tv_company_id)

    @pytest.mark.parametrize(
        'tv_thematic_id, expected',
        [
            (None, None),
            ([gval.TvThematicId.ADVERTISING], 'tvThematicId = 19'),
            ([gval.TvThematicId.ADVERTISING, gval.TvThematicId.ENTERTAINING], 'tvThematicId IN (19, 8)'),
        ],
    )
    def test_tv_thematic_id_filter(
        self, tv_thematic_id: Optional[Sequence[gval.TvThematicId]], expected: Optional[str]
    ) -> None:
        assert gflt.CompanyFilter(tv_thematic_id=tv_thematic_id).expr == expected

    @pytest.mark.parametrize(
        'tv_thematic_id',
        [
            [],
            [None, 'A'],
            [gval.TvThematicId.ADVERTISING, gval.TvThematicId.ADVERTISING],
        ],
    )
    def test_tv_thematic_id_filter_incorrect(self, tv_thematic_id: Any) -> None:
        with pytest.raises(ValueError):
            gflt.CompanyFilter(tv_thematic_id=tv_thematic_id)

    @pytest.mark.parametrize(
        'tv_net_id, expected',
        [
            (None, None),
            ([gval.TvNetId.DOMASHNIY], 'tvNetId = 257'),
            ([gval.TvNetId.PERVY_KANAL, gval.TvNetId.ROSSIYA_1], 'tvNetId IN (1, 2)'),
        ],
    )
    def test_tv_net_id_filter(self, tv_net_id: Optional[Sequence[gval.TvNetId]], expected: Optional[str]) -> None:
        assert gflt.CompanyFilter(tv_net_id=tv_net_id).expr == expected

    @pytest.mark.parametrize(
        'tv_net_id',
        [
            [],
            [None, 'A'],
            [gval.TvNetId.AD_CHANNELS, gval.TvNetId.AD_CHANNELS],
        ],
    )
    def test_tv_net_id_filter_incorrect(self, tv_net_id: Any) -> None:
        with pytest.raises(ValueError):
            gflt.CompanyFilter(tv_net_id=tv_net_id)

    @pytest.mark.parametrize(
        'region_id, expected',
        [
            (None, None),
            ([gval.RegionId.MOSCOW], 'regionId = 1'),
            ([gval.RegionId.MOSCOW, gval.RegionId.SAINT_PETERSBURG], 'regionId IN (1, 2)'),
        ],
    )
    def test_region_id_filter(self, region_id: Optional[Sequence[gval.RegionId]], expected: Optional[str]) -> None:
        assert gflt.CompanyFilter(region_id=region_id).expr == expected

    @pytest.mark.parametrize(
        'region_id',
        [
            [],
            [None, 'A'],
            [gval.RegionId.MOSCOW, gval.RegionId.MOSCOW],
        ],
    )
    def test_region_id_filter_incorrect(self, region_id: Any) -> None:
        with pytest.raises(ValueError):
            gflt.CompanyFilter(region_id=region_id)

    @pytest.mark.parametrize(
        'tv_company_holding_id, expected',
        [
            (None, None),
            ([gval.TvCompanyHoldingId.GAZPROM_MEDIA], 'tvCompanyHoldingId = 1000042'),
            ([gval.TvCompanyHoldingId.VIASAT], 'tvCompanyHoldingId = 1000014'),
        ],
    )
    def test_tv_company_holding_id_filter(
        self, tv_company_holding_id: Optional[Sequence[gval.TvCompanyHoldingId]], expected: Optional[str]
    ) -> None:
        assert gflt.CompanyFilter(tv_company_holding_id=tv_company_holding_id).expr == expected

    @pytest.mark.parametrize(
        'tv_company_holding_id',
        [
            [],
            [None, 'A'],
            [gval.TvCompanyHoldingId.GAZPROM_MEDIA, gval.TvCompanyHoldingId.GAZPROM_MEDIA],
        ],
    )
    def test_tv_company_holding_id_filter_incorrect(self, tv_company_holding_id: Any) -> None:
        with pytest.raises(ValueError):
            gflt.CompanyFilter(tv_company_holding_id=tv_company_holding_id)

    @pytest.mark.parametrize(
        'tv_company_media_holding_id, expected',
        [
            (None, None),
            ([gval.TvCompanyMediaHoldingId.GAZPROM_MEDIA], 'tvCompanyMediaHoldingId = 8'),
            ([gval.TvCompanyMediaHoldingId.MEDIA_1], 'tvCompanyMediaHoldingId = 1'),
        ],
    )
    def test_tv_company_media_holding_id_filter(
        self, tv_company_media_holding_id: Optional[Sequence[gval.TvCompanyMediaHoldingId]], expected: Optional[str]
    ) -> None:
        assert gflt.CompanyFilter(tv_company_media_holding_id=tv_company_media_holding_id).expr == expected

    @pytest.mark.parametrize(
        'tv_company_media_holding_id',
        [
            [],
            [None, 'A'],
            [gval.TvCompanyMediaHoldingId.VIASAT, gval.TvCompanyMediaHoldingId.VIASAT],
        ],
    )
    def test_tv_company_media_holding_id_filter_incorrect(self, tv_company_media_holding_id: Any) -> None:
        with pytest.raises(ValueError):
            gflt.CompanyFilter(tv_company_media_holding_id=tv_company_media_holding_id)


class TestBaseDemoFilter:
    @pytest.mark.parametrize(
        'sex, expected',
        [
            (None, None),
            (gval.Sex.MALE, 'sex = 1'),
            (gval.Sex.FEMALE, 'sex = 2'),
        ],
    )
    def test_sex_filter(self, sex: Optional[Sequence[gval.Sex]], expected: Optional[str]) -> None:
        assert gflt.BaseDemoFilter(sex=sex).expr == expected

    @pytest.mark.parametrize(
        'age, expected',
        [
            ((18, 25), 'age >= 18 AND age <= 25'),
            ((25, 50), 'age >= 25 AND age <= 50'),
            ((18, 99), 'age >= 18 AND age <= 99'),
        ],
    )
    def test_age_filter(self, age: Optional[Sequence[int]], expected: Optional[str]) -> None:
        assert gflt.BaseDemoFilter(age=age).expr == expected

    @pytest.mark.parametrize(
        'basedemo_filter, expected',
        [
            (gflt.BaseDemoFilter(), None),
            # Возраст.
            (gflt.BaseDemoFilter(age=(25, 45)), 'All 25-45'),
            (gflt.BaseDemoFilter(age=(18, 99)), 'All 18+'),
            # Пол.
            (gflt.BaseDemoFilter(sex=gval.Sex.MALE, age=(25, 45)), 'M 25-45'),
            (gflt.BaseDemoFilter(sex=gval.Sex.FEMALE, age=(25, 50)), 'W 25-50'),
            # Уровень дохода.
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[1]), 'All 25-50 IL 1'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[2]), 'All 25-50 IL 2'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[3]), 'All 25-50 IL 3'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[4]), 'All 25-50 IL 4'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[5]), 'All 25-50 IL 5'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[6]), 'All 25-50 IL 6'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[1, 2]), 'All 25-50 IL 1,2'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[1, 3]), 'All 25-50 IL 1,3'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[1, 2, 3]), 'All 25-50 IL 1-3'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[1, 2, 3, 6]), 'All 25-50 IL 1-3,6'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[1, 2, 3, 4, 6]), 'All 25-50 IL 1-4,6'),
            (gflt.BaseDemoFilter(age=(25, 50), inc_level=[1, 2, 3, 4, 5, 6]), 'All 25-50 IL 1-6'),
            # Группа дохода.
            (gflt.BaseDemoFilter(age=(25, 50), income_group_russia=[1]), 'All 25-50 A'),
            (gflt.BaseDemoFilter(age=(25, 50), income_group_russia=[2]), 'All 25-50 B'),
            (gflt.BaseDemoFilter(age=(25, 50), income_group_russia=[3]), 'All 25-50 C'),
            (gflt.BaseDemoFilter(age=(25, 50), income_group_russia=[2, 3]), 'All 25-50 BC'),
            (gflt.BaseDemoFilter(age=(25, 50), income_group_russia=[1, 2]), 'All 25-50 AB'),
            (gflt.BaseDemoFilter(age=(25, 50), income_group_russia=[1, 3]), 'All 25-50 AC'),
            (gflt.BaseDemoFilter(age=(25, 50), income_group_russia=[1, 2, 3]), 'All 25-50 ABC'),
            (gflt.BaseDemoFilter(age=(25, 50), income_group_russia=[4]), 'All 25-50'),
            # Возраст детей.
            (gflt.BaseDemoFilter(age=(18, 99), kids_age1=[gval.KidsAge1.YES]), 'All 18+ NO KIDS'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_age2=[gval.KidsAge2.YES]), 'All 18+ KIDS AGE 0'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_age3=[gval.KidsAge3.YES]), 'All 18+ KIDS AGE 1'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_age4=[gval.KidsAge4.YES]), 'All 18+ KIDS AGE 2-3'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_age5=[gval.KidsAge5.YES]), 'All 18+ KIDS AGE 4-6'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_age6=[gval.KidsAge6.YES]), 'All 18+ KIDS AGE 7-11'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_age7=[gval.KidsAge7.YES]), 'All 18+ KIDS AGE 12-15'),
            # Возраст детей - комбинированные варианты.
            (
                gflt.BaseDemoFilter(
                    age=(18, 99),
                    kids_age2=[gval.KidsAge2.YES],
                    kids_age3=[gval.KidsAge3.YES],
                ),
                'All 18+ KIDS AGE 0-1',
            ),
            (
                gflt.BaseDemoFilter(
                    age=(18, 99),
                    kids_age4=[gval.KidsAge4.YES],
                    kids_age5=[gval.KidsAge5.YES],
                ),
                'All 18+ KIDS AGE 2-6',
            ),
            (
                gflt.BaseDemoFilter(
                    age=(18, 99),
                    kids_age4=[gval.KidsAge4.YES],
                    kids_age5=[gval.KidsAge5.YES],
                    kids_age6=[gval.KidsAge6.YES],
                ),
                'All 18+ KIDS AGE 2-11',
            ),
            # Количество детей.
            (gflt.BaseDemoFilter(age=(18, 99), kids_num=[gval.KidsNum.NO_KIDS]), 'All 18+ NO KIDS'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_num=[gval.KidsNum.ONE_KID]), 'All 18+ ONE KID'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_num=[gval.KidsNum.TWO_KIDS]), 'All 18+ TWO KIDS'),
            (gflt.BaseDemoFilter(age=(18, 99), kids_num=[gval.KidsNum.THREE_OR_MORE_KIDS]), 'All 18+ THREE+ KIDS'),
        ],
    )
    def test_name(self, basedemo_filter: gflt.BaseDemoFilter, expected: Optional[str]) -> None:
        assert basedemo_filter.name == expected
