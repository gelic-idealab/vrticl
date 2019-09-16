# from .context import utility as u
from vrticl.utility import utility as u
import os, shutil
from os.path import dirname

def test_valid_input():
    print('current working directory', dirname(os.getcwd()))
    message, session_id = u.generate_package_web_tour('images_with_directory.zip', 'Test', 3, 2, 'default')
    expected_output = u.get_html_string('Test', 3, 2, 'jpg')
    f = open(os.path.join(dirname(os.getcwd()),'session', str(session_id), 'index.html'),'r')
    boolean_output = f.read() == expected_output
    f.close()
    shutil.rmtree(os.path.join('session'), str(session_id))
    assert boolean_output


def test_invalid_input():
    message, session_id = u.generate_package_web_tour('images_without_directory.zip', 'Test', 4, 2, 'default')
    boolean_output = message == 'There was an error with the input.'
    assert boolean_output

def test_invalid_input_files():
    message, session_id = u.generate_package_web_tour('test_invalid_files.zip', 'Test', 4, 2, 'default')
    boolean_output = message == 'There was an error with the image files in the zip folder.'
    assert boolean_output
