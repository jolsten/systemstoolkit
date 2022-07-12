import pytest
import numpy as np
from systemstoolkit.files.validators import (
    DataValidator,
    NoValidator,
    InvalidDataError,
    DataShapeValidator,
    QuaternionValidator,
    AngleValidator,
)


ONES_SAMPLE_DATA = np.ones((200, 4))
ONES_SAMPLE_TIME = np.ones(ONES_SAMPLE_DATA.shape[0])


def test_abstract_validator():
    with pytest.raises(NotImplementedError):
        validator = DataValidator()
        validator.validate(None, None)


def test_novalidator_valid():
    time, data = ONES_SAMPLE_TIME, ONES_SAMPLE_DATA
    validator = NoValidator()
    ftime, fdata = validator.validate(time, data)
    assert ftime.shape == time.shape
    assert fdata.shape == data.shape


def test_datashape_validator_valid():
    validator = DataShapeValidator(ncols=4)
    validator.validate(None, ONES_SAMPLE_DATA)


def test_datashape_validator_invalid_ncols():
    with pytest.raises(InvalidDataError):
        validator = DataShapeValidator(ncols=3)
        validator.validate(None, ONES_SAMPLE_DATA)


def test_datashape_validator_invalid_nrows():
    with pytest.raises(InvalidDataError):
        validator = DataShapeValidator(nrows=100)
        validator.validate(None, ONES_SAMPLE_DATA)


def test_quaternion_validator_valid():
    time = ONES_SAMPLE_TIME
    data = ONES_SAMPLE_DATA / np.sqrt(4)
    validator = QuaternionValidator()
    ftime, fdata = validator.validate(time, data)
    assert ftime.shape == time.shape
    assert fdata.shape == data.shape


def test_quaternion_validator_invalid_shape():
    time = ONES_SAMPLE_TIME
    data = ONES_SAMPLE_DATA[:, 0:3]
    with pytest.raises(InvalidDataError):
        validator = QuaternionValidator()
        validator.validate(time, data)


def test_quaternion_validator_invalid_values():
    time = ONES_SAMPLE_TIME
    data = ONES_SAMPLE_DATA
    with pytest.raises(InvalidDataError):
        validator = QuaternionValidator()
        validator.validate(time, data)


def test_angle_validator_invalid_values():
    time = ONES_SAMPLE_TIME
    data = ONES_SAMPLE_DATA[:, 0:3] * 500
    with pytest.raises(InvalidDataError):
        validator = AngleValidator()
        a, b = validator.validate(time, data)
