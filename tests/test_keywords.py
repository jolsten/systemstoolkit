import pytest

from stkfiles.keywords import MessageLevel, CentralBody, CoordinateAxes, AttitudeDeviations


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
