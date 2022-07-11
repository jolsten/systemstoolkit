<<<<<<< HEAD
<<<<<<< HEAD
import pytest
from systemstoolkit.files.formats import AttitudeFileFormat
from systemstoolkit.files.validators import NoValidator


def test_afile_format_novalidator():
    fmt = AttitudeFileFormat.QuatAngVels
    assert isinstance(fmt.validator, NoValidator)
=======
import pytest
from systemstoolkit.files.formats import AttitudeFileFormat
from systemstoolkit.files.validators import NoValidator


def test_afile_format_novalidator():
    fmt = AttitudeFileFormat.QuatAngVels
    assert isinstance(fmt.validator, NoValidator)
>>>>>>> 35a54389bd7199e199d4593870c92d2e6095ccf4
=======
import pytest
from systemstoolkit.files.formats import AttitudeFileFormat
from systemstoolkit.files.validators import NoValidator


def test_afile_format_novalidator():
    fmt = AttitudeFileFormat.QuatAngVels
    assert isinstance(fmt.validator, NoValidator)
>>>>>>> 35a54389bd7199e199d4593870c92d2e6095ccf4
