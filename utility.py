import os
import fnmatch
import zipfile
import tempfile, shutil


def get_input():
    """

    :return:
    """
    file_path = input('Enter the zip file path')
    # C:\Users\gaura\OneDrive\Desktop\Grainger\NewTestImages.zip
    # C:\Users\gaura\OneDrive\Desktop\Grainger\NewTestImages\TestImages.zip
    num_rows = int(input('Enter number of rows'))
    num_col = int(input('Enter number of columns'))
    return file_path, num_rows, num_col


def validate_input(file_path, num_rows, num_columns):
    """

    :param num_images:
    :param num_rows:
    :param num_columns:
    :return:
    """
    session_dir = tempfile.mkdtemp(dir='static')
    print(session_dir)

    extract_files(file_path, session_dir)

    image_extension = get_file_extension(session_dir)

    num_images = get_file_count(image_extension, session_dir)
    print('num_images', num_images)
    return num_columns * num_rows == num_images


def extract_files(file_path, full_session_path):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        print('list of dir', zip_ref.namelist())

        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            # copy file (taken from zipfile's extract)
            print('member=',member)
            source = zip_ref.open(member)
            target = open(os.path.join(full_session_path, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)


def get_file_extension(full_session_path):
    """

    :param full_session_path:
    :return:
    """
    for root, dirs, files in os.walk(full_session_path):
        print(files)
        for filename in files:
            print(filename)
            if filename.endswith('.jpg'):
                image_type = 'jpg'
            elif filename.endswith('.png'):
                image_type = 'png'
            break

    image_extension = '*.' + image_type
    return image_extension


def get_file_count(image_extension, full_session_path):
    """

    :param image_extension:
    :param full_session_path:
    :return:
    """
    number_of_images_in_extracted_zip = len(fnmatch.filter(os.listdir(full_session_path), image_extension))
    return number_of_images_in_extracted_zip


if __name__ == "__main__":
    file_path, num_rows, num_col = get_input()
    print('file path', file_path)
    print('num rows', num_rows)
    print('num col', num_col)

    print(validate_input(file_path, num_rows, num_col))
