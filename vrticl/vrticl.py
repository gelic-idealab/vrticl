import aframetour.aframetour as aft

def get_input():
    """
    Fetch input from command line. Requests user input for number of rows, columns and zip file path.
    :return:
    """
    # C:\Users\gaura\OneDrive\Desktop\Grainger\vrticl_issues\vrticl\vrticl\tests\images_with_directory.zip
    file_path = input('Enter the zip file path: ')
    title = input('Enter the title for the web tour: ')
    num_rows = int(input('Enter number of rows: '))
    num_col = int(input('Enter number of columns: '))
    return file_path, title, num_rows, num_col


    
if __name__ == "__main__":
    file_path, title, num_rows, num_col = get_input()
    message, session_identifier = aft.generate_package_web_tour(file_path, title, num_rows, num_col, 'default')
