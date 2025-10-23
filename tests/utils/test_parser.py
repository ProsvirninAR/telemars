import pytest

from telemars.filters.general import BaseDemoFilter
from telemars.params.filters import general as gval
from telemars.utils.parser import parse_audience


class TestParser:
    @pytest.mark.parametrize(
        'audience, expected',
        [
            # Базовые случаи.
            ('M 18+', BaseDemoFilter(sex=gval.Sex.MALE, age=(18, 99))),
            ('M 30+', BaseDemoFilter(sex=gval.Sex.MALE, age=(30, 99))),
            ('M 25-45', BaseDemoFilter(sex=gval.Sex.MALE, age=(25, 45))),
            ('W 18+', BaseDemoFilter(sex=gval.Sex.FEMALE, age=(18, 99))),
            ('W 45+', BaseDemoFilter(sex=gval.Sex.FEMALE, age=(45, 99))),
            ('W 30-55', BaseDemoFilter(sex=gval.Sex.FEMALE, age=(30, 55))),
            ('All 18+', BaseDemoFilter(age=(18, 99))),
            ('All 25-30', BaseDemoFilter(age=(25, 30))),
            ('All 30+', BaseDemoFilter(age=(30, 99))),
            # Проверка регистронезависимости и обработки пробелов.
            ('m 18+', BaseDemoFilter(sex=gval.Sex.MALE, age=(18, 99))),
            (' W  45+ ', BaseDemoFilter(sex=gval.Sex.FEMALE, age=(45, 99))),
            ('all 30-50', BaseDemoFilter(age=(30, 50))),
            ('all 30 - 50', BaseDemoFilter(age=(30, 50))),
            (' all 30 - 50', BaseDemoFilter(age=(30, 50))),
        ],
    )
    def test_base_audience(self, audience: str, expected: BaseDemoFilter) -> None:
        filter: BaseDemoFilter = parse_audience(audience)
        assert filter.age == expected.age

    @pytest.mark.parametrize(
        'audience, expected',
        [
            # Один уровень дохода.
            ('All 18+ IL 1', BaseDemoFilter(age=(18, 99), inc_level=[gval.IncLevel._1])),
            ('All 18+ IL 2', BaseDemoFilter(age=(18, 99), inc_level=[gval.IncLevel._2])),
            ('All 18+ IL 3', BaseDemoFilter(age=(18, 99), inc_level=[gval.IncLevel._3])),
            ('All 18+ IL 4', BaseDemoFilter(age=(18, 99), inc_level=[gval.IncLevel._4])),
            ('All 18+ IL 5', BaseDemoFilter(age=(18, 99), inc_level=[gval.IncLevel._5])),
            ('All 18+ IL 6', BaseDemoFilter(age=(18, 99), inc_level=[gval.IncLevel._6])),
            # Диапазон уровней дохода.
            (
                'All 18+ IL 1-3',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._1,
                        gval.IncLevel._2,
                        gval.IncLevel._3,
                    ],
                ),
            ),
            (
                'All 18+ IL 2-4',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._2,
                        gval.IncLevel._3,
                        gval.IncLevel._4,
                    ],
                ),
            ),
            (
                'All 18+ IL 3-5',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._3,
                        gval.IncLevel._4,
                        gval.IncLevel._5,
                    ],
                ),
            ),
            (
                'All 18+ IL 4-6',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._4,
                        gval.IncLevel._5,
                        gval.IncLevel._6,
                    ],
                ),
            ),
            (
                'All 18+ IL 1-6',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._1,
                        gval.IncLevel._2,
                        gval.IncLevel._3,
                        gval.IncLevel._4,
                        gval.IncLevel._5,
                        gval.IncLevel._6,
                    ],
                ),
            ),
            # Особые случаи.
            (
                'All 18+ IL 1,2',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._1,
                        gval.IncLevel._2,
                    ],
                ),
            ),
            (
                'All 18+ IL 1,3',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._1,
                        gval.IncLevel._3,
                    ],
                ),
            ),
            (
                'All 18+ IL 1,2,3',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._1,
                        gval.IncLevel._2,
                        gval.IncLevel._3,
                    ],
                ),
            ),
            (
                'All 18+ IL 1,2,3,6',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._1,
                        gval.IncLevel._2,
                        gval.IncLevel._3,
                        gval.IncLevel._6,
                    ],
                ),
            ),
            (
                'All 18+ IL 1-4,6',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._1,
                        gval.IncLevel._2,
                        gval.IncLevel._3,
                        gval.IncLevel._4,
                        gval.IncLevel._6,
                    ],
                ),
            ),
            # Разный порядок уровней.
            (
                'All 18+ IL 4,3,1,2,6',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_level=[
                        gval.IncLevel._4,
                        gval.IncLevel._3,
                        gval.IncLevel._1,
                        gval.IncLevel._2,
                        gval.IncLevel._6,
                    ],
                ),
            ),
        ],
    )
    def test_audience_inc_level(self, audience: str, expected: BaseDemoFilter) -> None:
        filter: BaseDemoFilter = parse_audience(audience)
        assert filter.age == expected.age

    @pytest.mark.parametrize(
        'audience, expected',
        [
            # Базовые случаи.
            (
                'All 18+ A',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.A,
                    ],
                ),
            ),
            (
                'All 18+ B',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.B,
                    ],
                ),
            ),
            (
                'All 18+ C',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.C,
                    ],
                ),
            ),
            (
                'All 18+ AB',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.A,
                        gval.IncomeGroupRussia.B,
                    ],
                ),
            ),
            (
                'All 18+ BA',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.B,
                        gval.IncomeGroupRussia.A,
                    ],
                ),
            ),
            (
                'All 18+ AC',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.A,
                        gval.IncomeGroupRussia.C,
                    ],
                ),
            ),
            (
                'All 18+ CB',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.C,
                        gval.IncomeGroupRussia.B,
                    ],
                ),
            ),
            (
                'All 18+ ABC',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.A,
                        gval.IncomeGroupRussia.B,
                        gval.IncomeGroupRussia.C,
                    ],
                ),
            ),
            (
                'All 18+ ACB',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.A,
                        gval.IncomeGroupRussia.C,
                        gval.IncomeGroupRussia.B,
                    ],
                ),
            ),
            (
                'All 18+ BCA',
                BaseDemoFilter(
                    age=(18, 99),
                    inc_group=[
                        gval.IncomeGroupRussia.B,
                        gval.IncomeGroupRussia.C,
                        gval.IncomeGroupRussia.A,
                    ],
                ),
            ),
        ],
    )
    def test_audience_inc_group(self, audience: str, expected: BaseDemoFilter) -> None:
        filter: BaseDemoFilter = parse_audience(audience)
        assert filter.age == expected.age

    @pytest.mark.parametrize(
        'audience, expected',
        [
            # Базовые случаи.
            ('', BaseDemoFilter()),
        ],
    )
    @pytest.mark.xfail()
    def test_audience_kids_age(self, audience: str, expected: BaseDemoFilter) -> None:
        filter: BaseDemoFilter = parse_audience(audience)
        assert filter.age == expected.age

    @pytest.mark.parametrize(
        'audience, expected',
        [
            # Базовые случаи.
            ('', BaseDemoFilter()),
        ],
    )
    @pytest.mark.xfail()
    def test_audience_kids_num(self, audience: str, expected: BaseDemoFilter) -> None:
        filter: BaseDemoFilter = parse_audience(audience)
        assert filter.age == expected.age
