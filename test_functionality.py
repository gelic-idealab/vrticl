from utility import validate_input


def test_valid_input():
    assert validate_input('tests/images_with_directory.zip',3,2)


def test_invalid_input():
    assert not validate_input('tests/images_without_directory.zip',4,2)
