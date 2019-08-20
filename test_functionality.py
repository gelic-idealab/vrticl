from utility import utility as u


def test_valid_input():
    assert u.validate_input('tests/images_with_directory.zip',3,2, True)


def test_invalid_input():
    assert not u.validate_input('tests/images_without_directory.zip',4,2, True)


def test_invalid_input_files():
    assert not u.validate_input('tests/test_invalid_files.zip',2,1, True)
