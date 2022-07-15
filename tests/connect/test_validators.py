import pytest
import systemstoolkit.connect.validators as validators


@pytest.mark.parametrize('name', [
    'ObjectName',
    'Object_Name',
    'Object123',
    '123_Object',
])
def test_valid_names(name):
    validators.name(name)
    assert True


@pytest.mark.parametrize('name', [
    'A'*100,
    'This Name Has a Space',
    'ThisN@meH@sSpec1alCharacters',
    '_Default',
    'End',
    'end',
    'END',
])
def test_invalid_names(name):
    with pytest.raises(ValueError):
        validators.name(name)


@pytest.mark.parametrize('value, min, max', [
    (0, None, None),
    (10, 0, None),
    (0, None, 90),
    (90, 0, 180),
])
def test_value_valid(value, min, max):
    validators.value(value, min, max)


@pytest.mark.parametrize('value, min, max', [
    (-10, 0, 180),
    (270, 0, 180),
])
def test_value_invalid(value, min, max):
    with pytest.raises(ValueError):
        validators.value(value, min, max)
