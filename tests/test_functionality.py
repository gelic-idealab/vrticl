from .context import utility as u


def test_valid_input():
    assert u.generate_package_web_tour('tests/images_with_directory.zip',3,2, True)


def test_invalid_input():
    assert not u.generate_package_web_tour('tests/images_without_directory.zip',4,2, True)


def test_invalid_input_files():
    assert not u.generate_package_web_tour('tests/test_invalid_files.zip',2,1, True)
