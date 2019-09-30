import sys
import aframetour.aframetour as aft

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