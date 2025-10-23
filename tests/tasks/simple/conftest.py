from datetime import date

import polars as pl
import pytest

from telemars.filters import general as gflt
from telemars.filters import simple as sflt
from telemars.options.simple import Option
from telemars.params.filters.simple import AdIssueStatusId, AdTypeId, Platform, PlayBackType
from telemars.params.options.simple import BigTv, KitId, SortOrder
from telemars.params.slices.simple import Slice
from telemars.params.statistics.simple import K7Statistic
from telemars.tasks.simple import SimpleTask


@pytest.fixture(name='SIMPLE_TASK')
def simple_task() -> SimpleTask:
    """Возвращает Simple задачу.

    Параметры задачи:
    - Дата: 2025-05-12
    - Целевая аудитория: All 25-50
    - Рекламодатель: 194557
    - Статистики: RtgPer
    - Срезы: ResearchDate, AdSpotId
    - Платформа: TV
    """
    return SimpleTask(
        date_filter=gflt.DateFilter(
            date_from=(date(2025, 5, 12)),
            date_to=date(2025, 5, 12),
        ),
        basedemo_filter=[
            gflt.BaseDemoFilter(age=(25, 50)),
        ],
        ad_filter=sflt.AdFilter(
            advertiser_id=[194557],
            ad_issue_status_id=[AdIssueStatusId.REAL],
            ad_type_id=[AdTypeId.SPOT],
        ),
        platform_filter=sflt.PlatformFilter(
            platform_id=[Platform.TV],
        ),
        playbacktype_filter=sflt.PlayBackTypeFilter(
            playback_type_id=[p for p in PlayBackType],
        ),
        slices=[
            Slice.RESEARCH_DATE,
            Slice.AD_SPOT_ID,
        ],
        statistics=[K7Statistic.RTG_PER],
        options=Option(
            kit_id=KitId.BIG_TV,
            big_tv=BigTv.YES,
        ),
        sortings=[
            (Slice.RESEARCH_DATE, SortOrder.ASC),
            (Slice.AD_SPOT_ID, SortOrder.ASC),
        ],
    )


@pytest.fixture(name='SIMPLE_TASK_RESULT')
def simple_task_result() -> pl.DataFrame:
    return pl.DataFrame(
        [
            {'researchDate': '2025-05-12', 'adSpotId': '6313910486', 'RtgPer All 25-50': 0.3282},
            {'researchDate': '2025-05-12', 'adSpotId': '6313910548', 'RtgPer All 25-50': 0.7255},
            {'researchDate': '2025-05-12', 'adSpotId': '6313910583', 'RtgPer All 25-50': 0.7468},
            {'researchDate': '2025-05-12', 'adSpotId': '6313910616', 'RtgPer All 25-50': 0.6683},
            {'researchDate': '2025-05-12', 'adSpotId': '6313934018', 'RtgPer All 25-50': 0.8406},
            {'researchDate': '2025-05-12', 'adSpotId': '6313934090', 'RtgPer All 25-50': 0.9747},
            {'researchDate': '2025-05-12', 'adSpotId': '6313934121', 'RtgPer All 25-50': 0.7069},
            {'researchDate': '2025-05-12', 'adSpotId': '6313953009', 'RtgPer All 25-50': 0.1471},
            {'researchDate': '2025-05-12', 'adSpotId': '6313953074', 'RtgPer All 25-50': 0.2029},
            {'researchDate': '2025-05-12', 'adSpotId': '6313953103', 'RtgPer All 25-50': 0.2727},
        ]
    )
