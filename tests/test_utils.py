import pytest
import numpy as np
import datetime

from systemstoolkit.utils import stk_datetime, read_file_data, parse_file_data

FILE_Q = ('data/AttitudeTimeQuaternions.a', (361, 4))
FILE_A = ('data/AttitudeTimeEulerAngles.a', (721, 3))


@pytest.mark.parametrize('input, output', [
    (np.datetime64('1986-03-04T20:45:00'), '04 Mar 1986 20:45:00.000'),
    (datetime.datetime(1986,3,4,20,45), '04 Mar 1986 20:45:00.000'),
])
def test_stk_datetime(input, output) -> None:
    assert stk_datetime(input) == output


def test_stk_datetime_invalid():
    with pytest.raises(TypeError):
        stk_datetime(None)


@pytest.mark.parametrize('file, shape', [
    FILE_Q,
    FILE_A,
])
def test_read_file_data(file, shape) -> None:
    time, data = read_file_data(file)
    assert data.shape == shape


@pytest.mark.parametrize('file, shape', [
    FILE_Q,
    FILE_A,
])
def test_parse_file_data(file, shape) -> None:
    data = read_file_data(file)
    with open(file, 'r') as f:
        text = f.read()
        time, data = parse_file_data(text)
        assert data.shape == shape
