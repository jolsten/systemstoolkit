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
