import pytest
from systemstoolkit.files.builders import attitude_file
from systemstoolkit.utils import read_file_data

FILE_Q = 'data/attitude/AttitudeTimeQuaternions.a'
FILE_A = 'data/attitude/AttitudeTimeEulerAngles.a'


@pytest.mark.parametrize('file, format, kwargs', [
    (FILE_Q, 'quaternions', dict()),
    (FILE_A, 'eulerangles', dict()),
    (FILE_Q, 'quaternions', dict(axes='j2000')),
    (FILE_Q, 'quaternions', dict(axes='temeofepoch', axes_epoch='1986-03-04 20:45')),
    (FILE_Q, 'quaternions', dict(epoch='1986-03-04 20:45')),
    (FILE_Q, 'quaternions', dict(body='earth')),
    (FILE_Q, 'quaternions', dict(int_method='lagrange', int_order=3)),
    (FILE_Q, 'quaternions', dict(deviations='rapid')),
    (FILE_Q, 'quaternions', dict(blocking=20)),
])
def test_afile_builder(file, format, kwargs):
    time, data = read_file_data(file)

    afile = attitude_file(
        time, data, format=format, **kwargs,
    )
    print(afile)
