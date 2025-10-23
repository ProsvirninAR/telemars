from datetime import date

import polars as pl
import pytest

from telemars.filters import crosstab as cflt
from telemars.options.crosstab import Option
from telemars.params.filters.crosstab import (
    BreaksContentType,
    BreaksDistributionType,
    BreaksIssueStatusId,
    Location,
    Platform,
    PlayBackType,
)
from telemars.params.options.crosstab import BigTv, IssueType, KitId, SortOrder
from telemars.params.slices.crosstab import Slice
from telemars.params.statistics.crosstab import K7Statistic
from telemars.tasks.crosstab import CrosstabTask


@pytest.fixture(name='CROSSTAB_TASK')
def crosstab_task() -> CrosstabTask:
    return CrosstabTask(
        date_filter=cflt.DateFilter(
            date_from=(date(2024, 6, 1)),
            date_to=date(2024, 8, 31),
        ),
        basedemo_filter=[
            cflt.BaseDemoFilter(age=(25, 54)),
        ],
        platform_filter=cflt.PlatformFilter(
            platform_id=[Platform.TV, Platform.DESKTOP, Platform.MOBILE],
        ),
        playbacktype_filter=cflt.PlayBackTypeFilter(
            playback_type_id=[p for p in PlayBackType],
        ),
        break_filter=cflt.BreakFilter(
            breaks_content_type=[BreaksContentType.COMMERCIAL],
            breaks_issue_status_id=[BreaksIssueStatusId.REAL],
            breaks_distribution_type=[BreaksDistributionType.NETWORK, BreaksDistributionType.ORBITAL],
        ),
        location_filter=cflt.LocationFilter(location_id=[Location.DACHA, Location.HOME, Location.OUT_OF_HOME]),
        slices=[Slice.BREAKS_DISTRIBUTION_TYPE_NAME, Slice.TV_COMPANY_NAME],
        statistics=[K7Statistic.SPOT_BY_BREAKS_SALES_RTG_PER_AVG, K7Statistic.SPOT_BY_BREAKS_RTG_PER_AVG],
        options=Option(kit_id=KitId.BIG_TV, big_tv=BigTv.YES, issue_type=IssueType.BREAKS),
        sortings=[(Slice.BREAKS_DISTRIBUTION_TYPE_NAME, SortOrder.ASC), (Slice.TV_COMPANY_NAME, SortOrder.ASC)],
    )


@pytest.fixture(name='CROSSTAB_TASK_RESULT')
def crosstab_task_result() -> pl.DataFrame:
    return pl.DataFrame(
        [
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'ДОМАШНИЙ (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 0.7419,
                'SpotByBreaksRtgPerAvg All 25-54': 0.4266,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'ЗВЕЗДА (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 0.3815,
                'SpotByBreaksRtgPerAvg All 25-54': 0.158,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'МАТЧ ТВ (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 0.1307,
                'SpotByBreaksRtgPerAvg All 25-54': 0.0889,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'НТВ (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 1.2123,
                'SpotByBreaksRtgPerAvg All 25-54': 0.5616,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'ПЕРВЫЙ КАНАЛ (ИНТЕРНЕТ)',
                'SpotByBreaksSalesRtgPerAvg': 0.0117,
                'SpotByBreaksRtgPerAvg All 25-54': 0.0138,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'ПЕРВЫЙ КАНАЛ (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 0.4372,
                'SpotByBreaksRtgPerAvg All 25-54': 0.3977,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'ПЯТНИЦА (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 0.2963,
                'SpotByBreaksRtgPerAvg All 25-54': 0.3164,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'ПЯТЫЙ КАНАЛ (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 0.7103,
                'SpotByBreaksRtgPerAvg All 25-54': 0.6223,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'РЕН ТВ (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 0.6242,
                'SpotByBreaksRtgPerAvg All 25-54': 0.6242,
            },
            {
                'breaksDistributionTypeName': 'Орбитальный',
                'tvCompanyName': 'РОССИЯ 1 (СЕТЕВОЕ ВЕЩАНИЕ)',
                'SpotByBreaksSalesRtgPerAvg': 0.7598,
                'SpotByBreaksRtgPerAvg All 25-54': 0.2913,
            },
        ]
    )
