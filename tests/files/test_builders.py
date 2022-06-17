import pytest
from systemstoolkit.files.builders import attitude_file
from systemstoolkit.utils import read_file_data

FILE_Q = 'data/attitude/AttitudeTimeQuaternions.a'
FILE_A = 'data/attitude/AttitudeTimeEulerAngles.a'


@pytest.mark.parametrize('file, format, kwargs', [
    (FILE_Q, 'quaternions', dict()),
    (FILE_A, 'eulerangles', dict()),
])
def test_afile_builder(file, format, kwargs):
    time, data = read_file_data(file)

    afile = attitude_file(
        time, data, format=format, **kwargs,
    )
    print(afile)
    assert True
