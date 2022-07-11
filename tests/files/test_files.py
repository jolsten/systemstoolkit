import pytest
import numpy as np
from dataclasses import asdict
from systemstoolkit.files.files import AttitudeFile
from systemstoolkit.files.formats import AttitudeFileFormat
from systemstoolkit.utils import read_file_data
from systemstoolkit.files.keywords import (
    Keyword, Coordinate, CoordinateAxes, CoordinateAxesEpoch,
)


FILE_Q = 'data/AttitudeTimeQuaternions.a'
FILE_A = 'data/AttitudeTimeEulerAngles.a'

@pytest.mark.parametrize('file, format, kwargs', [
    (FILE_Q, 'quaternions', dict()),
    (FILE_A, 'eulerangles', dict()),
    (FILE_Q, 'quaternions', dict(
        axes=Coordinate(
            CoordinateAxes('j2000'),
            None,
        ),
                                )),
    (FILE_Q, 'quaternions', dict(
        axes=Coordinate(
            CoordinateAxes('temeofepoch'),
            CoordinateAxesEpoch(np.datetime64('1986-03-04 20:45:00'))
        ),
                                )),
])
def test_quaternions(file, format, kwargs):
    time, data = read_file_data(file)

    afile = AttitudeFile(
        time,
        data,
        format = AttitudeFileFormat(format),
    )

    out = afile.to_string()

    print(out)

    assert isinstance(out, str)
    assert len(out) > 1000

    for key in asdict(afile):
        attr = getattr(afile, key)
        if isinstance(attr, Keyword):
            keyword, value =  str(attr).split(maxsplit=1)
            assert keyword in out
            assert value in out
    