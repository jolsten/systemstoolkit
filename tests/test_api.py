import pytest
from stkfiles.api import attitude_file
from stkfiles.utils import read_file_data

FILE_Q = 'data/attitude/AttitudeTimeQuaternions.a'


@pytest.mark.parametrize('file, format, kwargs', [
    (FILE_Q, 'quaternions', dict()),
])
def test_afile_builder(file, format, kwargs):
    time, data = read_file_data(FILE_Q)

    afile = attitude_file(
        time, data, 'quaternions', **kwargs,
    )
    print(file)
    assert True
