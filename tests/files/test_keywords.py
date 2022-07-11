<<<<<<< HEAD
import pytest

from systemstoolkit.files.keywords import (
    Keyword, KeywordEnum,
    MessageLevel, CentralBody, AttitudeDeviations, TimeFormat,
    Coordinate, CoordinateAxes, CoordinateAxesEpoch,
)
from systemstoolkit.units.time import TimeUnit


@pytest.mark.parametrize('cls, keyword, value, input', [
    (MessageLevel, 'MessageLevel', 'Errors', 'Errors'),
    (MessageLevel, 'MessageLevel', 'Errors', 'errors'),
    (MessageLevel, 'MessageLevel', 'Errors', 'ERRORS'),
    (CentralBody, 'CentralBody', 'Earth', 'Earth'),
    (CentralBody, 'CentralBody', 'Earth', 'earth'),
    (CoordinateAxes, 'CoordinateAxes', 'ICRF', 'icrf'),
    (CoordinateAxes, 'CoordinateAxes', 'J2000', 'j2000'),
    (CoordinateAxes, 'CoordinateAxes', 'Fixed', 'fixed'),
    (AttitudeDeviations, 'AttitudeDeviations', 'Mild', 'mild'),
])
def test_enum_keywords(cls, keyword, value, input):
    o = cls(input)
    assert str(o).split() == [keyword, value]


def test_timeformat_lowercase_valid():
    time_fmt = TimeFormat('isoymd')


def test_timeformat_invalid():
    with pytest.raises(ValueError):
        time_fmt = TimeFormat('NotAValidTimeFormat')


def test_coordinate_compound_noepoch_valid():
    coord = Coordinate(
        axes=CoordinateAxes('J2000'),
        epoch=None,
    )


def test_coordinate_compound_noepoch_invalid():
    with pytest.raises(ValueError):
        coord = Coordinate(
            axes=CoordinateAxes('J2000'),
            epoch=CoordinateAxesEpoch('1986-03-04 20:45')
        )


def test_coordinate_compound_epoch_valid():
    coord = Coordinate(
        axes=CoordinateAxes('TEMEOfEpoch'),
        epoch=CoordinateAxesEpoch('1986-03-04 20:45')
    )


def test_coordinate_compound_epoch_invalid():
    with pytest.raises(ValueError):
        coord = Coordinate(
            axes=CoordinateAxes('TEMEOfEpoch'),
            epoch=None
        )


def test_time_format():
    time_fmt = TimeFormat('isoymd')
    assert issubclass(time_fmt.value, TimeUnit)
=======
import pytest

from systemstoolkit.files.keywords import (
    Keyword, KeywordEnum,
    MessageLevel, CentralBody, AttitudeDeviations, TimeFormat,
    Coordinate, CoordinateAxes, CoordinateAxesEpoch,
)
from systemstoolkit.units.time import TimeUnit


@pytest.mark.parametrize('cls, keyword, value, input', [
    (MessageLevel, 'MessageLevel', 'Errors', 'Errors'),
    (MessageLevel, 'MessageLevel', 'Errors', 'errors'),
    (MessageLevel, 'MessageLevel', 'Errors', 'ERRORS'),
    (CentralBody, 'CentralBody', 'Earth', 'Earth'),
    (CentralBody, 'CentralBody', 'Earth', 'earth'),
    (CoordinateAxes, 'CoordinateAxes', 'ICRF', 'icrf'),
    (CoordinateAxes, 'CoordinateAxes', 'J2000', 'j2000'),
    (CoordinateAxes, 'CoordinateAxes', 'Fixed', 'fixed'),
    (AttitudeDeviations, 'AttitudeDeviations', 'Mild', 'mild'),
])
def test_enum_keywords(cls, keyword, value, input):
    o = cls(input)
    assert str(o).split() == [keyword, value]


def test_timeformat_lowercase_valid():
    time_fmt = TimeFormat('isoymd')


def test_timeformat_invalid():
    with pytest.raises(ValueError):
        time_fmt = TimeFormat('NotAValidTimeFormat')


def test_coordinate_compound_noepoch_valid():
    coord = Coordinate(
        axes=CoordinateAxes('J2000'),
        epoch=None,
    )


def test_coordinate_compound_noepoch_invalid():
    with pytest.raises(ValueError):
        coord = Coordinate(
            axes=CoordinateAxes('J2000'),
            epoch=CoordinateAxesEpoch('1986-03-04 20:45')
        )


def test_coordinate_compound_epoch_valid():
    coord = Coordinate(
        axes=CoordinateAxes('TEMEOfEpoch'),
        epoch=CoordinateAxesEpoch('1986-03-04 20:45')
    )


def test_coordinate_compound_epoch_invalid():
    with pytest.raises(ValueError):
        coord = Coordinate(
            axes=CoordinateAxes('TEMEOfEpoch'),
            epoch=None
        )


def test_time_format():
    time_fmt = TimeFormat('isoymd')
    assert issubclass(time_fmt.value, TimeUnit)
>>>>>>> 35a54389bd7199e199d4593870c92d2e6095ccf4
