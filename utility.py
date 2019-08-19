import os
import fnmatch
import zipfile
import tempfile, shutil


def get_input():
    """
    Fetch input from command line. Requests user input for number of rows, columns and zip file path.
    :return:
    """
    file_path = input('Enter the zip file path: ')
    num_rows = int(input('Enter number of rows: '))
    num_col = int(input('Enter number of columns: '))
    return file_path, num_rows, num_col


def validate_input(file_path, num_rows, num_columns, is_test):
    """
    Calls methods to extract files from the zip folder, gets the file count, matches with user input and returns a boolean.
    :param num_images:
    :param num_rows:
    :param num_columns:
    :return: A boolean that indicates if the input is valid
    """
    session_dir = tempfile.mkdtemp(dir='static')
    print(session_dir)

    extract_files(file_path, session_dir)

    image_extension = get_file_extension(session_dir)

    num_images = get_file_count(image_extension, session_dir)
    print('num_images', num_images)

    is_input_valid = num_columns * num_rows == num_images

    if is_test or not is_input_valid:
        shutil.rmtree(session_dir)

    return num_columns * num_rows == num_images


def extract_files(file_path, full_session_path):
    """
    Extract files from a given zip file and stores in a given local folder
    :param file_path: Path where the zip file is stored
    :param full_session_path: Path where the zip file is extracted
    :return:
    """
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        print('list of dir', zip_ref.namelist())

        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            source = zip_ref.open(member)
            target = open(os.path.join(full_session_path, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)


def get_file_extension(full_session_path):
    """
    Gets the type of image file contained in the extracted folder
    :param full_session_path: Local file path where the zip file is stored
    :return: Returns a string value with image type as jpg, png and so on.
    """
    for root, dirs, files in os.walk(full_session_path):
        for filename in files:
            if filename.endswith('.jpg'):
                image_type = 'jpg'
            elif filename.endswith('.png'):
                image_type = 'png'
            break

    image_extension = '*.' + image_type
    return image_extension


def get_file_count(image_extension, full_session_path):
    """
    Counts the number of files in the extracted zip folder
    :param image_extension: Type of file stored in the zip folder
    :param full_session_path: Location of the extracted zip file
    :return:
    """
    number_of_images_in_extracted_zip = len(fnmatch.filter(os.listdir(full_session_path), image_extension))
    return number_of_images_in_extracted_zip


if __name__ == "__main__":
    file_path, num_rows, num_col = get_input()
    print(validate_input(file_path, num_rows, num_col, False))
