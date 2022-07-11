import pytest
from systemstoolkit.files.builders import attitude_file, sensor_pointing_file
from systemstoolkit.utils import read_file_data

A_FILE_Q = 'data/AttitudeTimeQuaternions.a'
A_FILE_A = 'data/AttitudeTimeEulerAngles.a'
SP_FILE_AZEL = 'data/AttitudeTimeAzElAngles.sp'


@pytest.mark.parametrize('file, format, kwargs', [
    (A_FILE_Q, 'quaternions', dict()),
    (A_FILE_A, 'eulerangles', dict()),
    (A_FILE_Q, 'quaternions', dict(axes='j2000')),
    (A_FILE_Q, 'quaternions', dict(axes='temeofepoch', axes_epoch='1986-03-04 20:45')),
    (A_FILE_Q, 'quaternions', dict(epoch='1986-03-04 20:45')),
    (A_FILE_Q, 'quaternions', dict(body='earth')),
    (A_FILE_Q, 'quaternions', dict(int_method='lagrange', int_order=3)),
    (A_FILE_Q, 'quaternions', dict(deviations='rapid')),
    (A_FILE_Q, 'quaternions', dict(blocking=20)),
])
def test_afile_builder(file, format, kwargs):
    time, data = read_file_data(file)

    file = attitude_file(
        time, data, format=format, **kwargs,
    )
    print(file)


@pytest.mark.parametrize('file, format, kwargs', [
    (A_FILE_Q, 'quaternions', dict()),
    (A_FILE_A, 'eulerangles', dict()),
    (A_FILE_Q, 'quaternions', dict(axes='j2000')),
    (A_FILE_Q, 'quaternions', dict(epoch='1986-03-04 20:45')),
    (A_FILE_Q, 'quaternions', dict(body='earth')),
    (A_FILE_Q, 'quaternions', dict(deviations='rapid')),
    (SP_FILE_AZEL, 'AzElAngles', dict()),
])
def test_spfile_builder(file, format, kwargs):
    time, data = read_file_data(file)

    file = sensor_pointing_file(
        time, data, format=format, **kwargs,
    )
    print(file)
