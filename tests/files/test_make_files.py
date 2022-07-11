<<<<<<< HEAD
<<<<<<< HEAD
from systemstoolkit.files.builders import attitude_file
import pytest
from systemstoolkit.utils import read_file_data

FILE_Q = 'data/AttitudeTimeQuaternions.a'
FILE_A = 'data/AttitudeTimeEulerAngles.a'


@pytest.mark.parametrize('file, format, kwargs', [
    (FILE_Q, 'quaternions', dict()),
    (FILE_A, 'eulerangles', dict()),
])
def test_make_attitude_file(file, format, kwargs):
    time, data = read_file_data(file)
    afile = attitude_file(time, data, format=format, **kwargs)
    with open(f'{format}.a', 'w') as fd:
        fd.write(afile)
=======
from systemstoolkit.files.builders import attitude_file
import pytest
from systemstoolkit.utils import read_file_data

FILE_Q = 'data/AttitudeTimeQuaternions.a'
FILE_A = 'data/AttitudeTimeEulerAngles.a'


@pytest.mark.parametrize('file, format, kwargs', [
    (FILE_Q, 'quaternions', dict()),
    (FILE_A, 'eulerangles', dict()),
])
def test_make_attitude_file(file, format, kwargs):
    time, data = read_file_data(file)
    afile = attitude_file(time, data, format=format, **kwargs)
    with open(f'{format}.a', 'w') as fd:
        fd.write(afile)
>>>>>>> 35a54389bd7199e199d4593870c92d2e6095ccf4
=======
from systemstoolkit.files.builders import attitude_file
import pytest
from systemstoolkit.utils import read_file_data

FILE_Q = 'data/AttitudeTimeQuaternions.a'
FILE_A = 'data/AttitudeTimeEulerAngles.a'


@pytest.mark.parametrize('file, format, kwargs', [
    (FILE_Q, 'quaternions', dict()),
    (FILE_A, 'eulerangles', dict()),
])
def test_make_attitude_file(file, format, kwargs):
    time, data = read_file_data(file)
    afile = attitude_file(time, data, format=format, **kwargs)
    with open(f'{format}.a', 'w') as fd:
        fd.write(afile)
>>>>>>> 35a54389bd7199e199d4593870c92d2e6095ccf4
