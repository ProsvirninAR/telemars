import polars as pl
import pytest
from polars.testing import assert_frame_equal

from telemars.tasks.simple import SimpleTask


@pytest.mark.asyncio
@pytest.mark.api
async def test_simple_task(SIMPLE_TASK: SimpleTask, SIMPLE_TASK_RESULT: pl.DataFrame) -> None:
    result: pl.DataFrame = await SIMPLE_TASK.execute()
    result_head: pl.DataFrame = result.head(len(SIMPLE_TASK_RESULT))
    assert_frame_equal(result_head, SIMPLE_TASK_RESULT)
