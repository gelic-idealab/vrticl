import aframetour.aframetour as aft
import sys


def get_input():
    """
    Fetch input from command line. Requests user input for number of rows, columns and zip file path.
    :return:
    """
    # C:/Users/gaura/OneDrive/Desktop/Grainger/vrticl/vrticl/vrticl/tests/images_with_directory.zip
    file_path = input('Enter the zip file path: ')
    title = input('Enter the title for the web tour: ')
    num_rows = int(input('Enter number of rows: '))
    num_col = int(input('Enter number of columns: '))
    return file_path, title, num_rows, num_col

    
if __name__ == "__main__":
    # file_path, title, num_rows, num_col = get_input()
    cmd_line_args = sys.argv
    print('Number of arguments:', len(cmd_line_args), 'arguments.')
    print('Argument List:', str(cmd_line_args))
    if len(cmd_line_args) == 5:
        title = cmd_line_args[1]
        num_rows = int(cmd_line_args[2])
        num_col = int(cmd_line_args[3])
        file_path = cmd_line_args[4]
        message, image_extension, session_identifier = aft.generate_package_web_tour(file_path, title, num_rows, num_col, 'default')
        print(message, image_extension, session_identifier)
    else:
        print('Invalid Input! Enter input as title, number of rows, number of columns and file path.')
