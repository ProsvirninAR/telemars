import polars as pl
import pytest
from polars.testing import assert_frame_equal

from telemars.tasks.crosstab import CrosstabTask


@pytest.mark.asyncio
@pytest.mark.api
async def test_crosstab_task(CROSSTAB_TASK: CrosstabTask, CROSSTAB_TASK_RESULT: pl.DataFrame) -> None:
    result: pl.DataFrame = await CROSSTAB_TASK.execute()
    result_head: pl.DataFrame = result.head(len(CROSSTAB_TASK_RESULT))
    assert_frame_equal(result_head, CROSSTAB_TASK_RESULT)
