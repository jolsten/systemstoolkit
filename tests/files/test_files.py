import pytest
from dataclasses import asdict
from systemstoolkit.files.keywords import Keyword
from systemstoolkit.files.files import AttitudeFile
from systemstoolkit.files.formats import AttitudeFileFormat
from systemstoolkit.utils import read_file_data, parse_file_data


FILE_Q = 'data/attitude/AttitudeTimeQuaternions.a'


@pytest.mark.parametrize('file, format', [
    (FILE_Q, 'quaternions'),
])
def test_quaternions(file, format):
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
