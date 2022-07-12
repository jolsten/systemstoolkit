import pytest
from systemstoolkit.files.formats import AttitudeFileFormat
from systemstoolkit.files.validators import NoValidator


def test_afile_format_novalidator():
    fmt = AttitudeFileFormat.QuatAngVels
    assert isinstance(fmt.validator, NoValidator)
