import pytest
import numpy as np
import datetime

from systemstoolkit.utils import stk_datetime


@pytest.mark.parametrize('input, output', [
    (np.datetime64('1986-03-04T20:45:00'), '04 Mar 1986 20:45:00.000'),
    (datetime.datetime(1986,3,4,20,45), '04 Mar 1986 20:45:00.000'),
])
def test_stk_datetime(input, output) -> None:
    assert stk_datetime(input) == output
