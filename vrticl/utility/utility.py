import fnmatch
import zipfile
import shutil, uuid, pathlib, glob, os
from os.path import dirname


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


def validate_input(image_extension, num_rows, num_columns, session_dir):
    """
    Calls methods to extract files from the zip folder, gets the file count, matches with user input and returns a boolean.
    :param num_images:
    :param num_rows:
    :param num_columns:
    :return: A boolean that indicates if the input is valid
    """
    if image_extension!=None:
        num_images = get_file_count(image_extension, session_dir)
        print('num_images', num_images)

        is_input_valid = num_columns * num_rows == num_images
    else:
        is_input_valid = False

    return is_input_valid


def extract_files(file_path, session_dir):
    """
    Extract files from a given zip file and stores in a given local folder
    :param file_path: Path where the zip file is stored
    :param session_dir: Path where the zip file is extracted
    :return:
    """
    full_session_path = pathlib.Path(session_dir,'static','images')
    print('full_session_path = ',full_session_path)
    os.makedirs(full_session_path)
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        print('list of dir', zip_ref.namelist())

        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            print("Trying to open: %s" % (os.path.join(full_session_path, filename)))
            source = zip_ref.open(member)
            target = open(os.path.join(full_session_path, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
    return full_session_path


def get_file_extension(full_session_path):
    """
    Gets the type of image file contained in the extracted folder
    :param full_session_path: Local file path where the zip file is stored
    :return: Returns a string value with image type as jpg, png and so on.
    """
    image_type=''
    for root, dirs, files in os.walk(full_session_path):
        for filename in files:
            if filename.endswith('.jpg'):
                image_type = 'jpg'
            elif filename.endswith('.png'):
                image_type = 'png'
            break

    if image_type=='':
        return None
    else:
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


def rename_images(grid_row, grid_column, folderPath, image_extension):
    """
    Refactor images extracted from zip folder in a sequential manner based on the grid rows and columns
    :param grid_row: number of rows input by user
    :param grid_column: number of columns input by user
    :param folderPath: directory where the images are stored
    :param image_extension: type of image (jpg, png)
    :return:
    """
    row_counter = 1
    column_counter = 1
    is_incrementing = True
    for pathAndFilename in glob.iglob(os.path.join(folderPath, image_extension)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        # print('path and file name',pathAndFilename)
        # print('Test title and ext',title, ext)
        if row_counter <= int(grid_row):
            if column_counter <= int(grid_column):
                os.rename(pathAndFilename,
                          os.path.join(folderPath, str(row_counter) + '_' + str(column_counter) + ext))
            if is_incrementing:
                if row_counter < int(grid_row):
                    row_counter += 1
                else:
                    column_counter += 1
                    is_incrementing = False
                    continue
            else:
                if row_counter > 1:
                    row_counter -= 1
                else:
                    column_counter += 1
                    is_incrementing = True
                    continue


def get_html_string(title, num_rows, num_col, image_extension):
    return """
    <!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<title>"""+title+"""</title>
<meta name='description' content='360&deg; Image - A-Frame'>
<script src='https://aframe.io/releases/0.9.2/aframe.min.js'></script>
<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script>
<script src='static/assignImageObject.js' type='text/javascript'></script>
<script src='static/setImage.js' type='text/javascript'></script>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

</head>
<body onload="loadImages("""+str(num_rows)+""","""+str(num_col)+""",'static/images','"""+image_extension+"""')">


<a-scene>

  <a-assets>
    <img id='arrow-thumb' crossorigin='anonymous' src='static/arrow.png'>
    <img id='this-image' crossorigin='anonymous' >

    <audio id='click-sound' crossorigin='anonymous' src='https://cdn.aframe.io/360-image-gallery-boilerplate/audio/click.ogg'></audio>

    <!-- Image link template to be reused. -->
    <script id='link' type='text/html'>
      <a-entity class='link'
        geometry='primitive: plane; height: 0.5; width: 1'
        material='shader: flat; src: ${thumb}; alphaTest: 0.5; opacity: 0.6'
        event-set__1='_event: mousedown; scale: 1 1 1'
        event-set__2='_event: mouseup; scale: 1.2 1.2 1'
        event-set__3='_event: mouseenter; scale: 1.2 1.2 1'
        event-set__4='_event: mouseleave; scale: 1 1 1'
        set-image='on: click; target: #image-current; src: ${src}'
        sound='on: click; src: #click-sound'></a-entity>
    </script>
  </a-assets>

<a-sky id='image-current' src='#this-image'></a-sky>

<!-- Image links. -->
 <a-entity id='goRightLink' layout='type: line; margin: 1.5' position='6 -1.2 0' rotation='0 270 0' scale='' visible='visible'>
  <a-entity template='src: #link' data-src='#arrow-right' data-thumb='#arrow-thumb'  >
      <a-entity class='link' geometry='primitive: plane; height: 0.5; width: 1' material='shader: flat; src: #arrow-thumb; alphaTest: 0.5; opacity: 0.6' event-set__1='_event: mousedown; scale: 1 1 1' event-set__2='_event: mouseup; scale: 1.2 1.2 1' event-set__3='_event: mouseenter; scale: 1.2 1.2 1' event-set__4='_event: mouseleave; scale: 1 1 1' set-image='on: click; target: #image-current; src: #arrow-right' sound='on: click; src: #click-sound'  ></a-entity>
  </a-entity>
</a-entity>
<a-entity id='goLeftLink' layout='type: line; margin: 1.5' position='-6 -1.2 0' rotation='0 90 0' scale='' visible=''>
    <a-entity template='src: #link' data-src='#arrow-left' data-thumb='#arrow-thumb'  >
        <a-entity class='link' geometry='primitive: plane; height: 0.5; width: 1' material='shader: flat; src: #arrow-thumb; alphaTest: 0.5; opacity: 0.6' event-set__1='_event: mousedown; scale: 1 1 1' event-set__2='_event: mouseup; scale: 1.2 1.2 1' event-set__3='_event: mouseenter; scale: 1.2 1.2 1' event-set__4='_event: mouseleave; scale: 1 1 1' set-image='on: click; target: #image-current; src: #arrow-left' sound='on: click; src: #click-sound'  ></a-entity>
    </a-entity>
  </a-entity>
  <a-entity id='goForwardLink' layout='type: line; margin: 1.5' position='0 -1.2 -6' rotation='0 0 0' visible='' scale=''>
    <a-entity template='src: #link' data-src='#arrow-forward' data-thumb='#arrow-thumb'  >
        <a-entity class='link' geometry='primitive: plane; height: 0.5; width: 1' material='shader: flat; src: #arrow-thumb; alphaTest: 0.5; opacity: 0.6' event-set__1='_event: mousedown; scale: 1 1 1' event-set__2='_event: mouseup; scale: 1.2 1.2 1' event-set__3='_event: mouseenter; scale: 1.2 1.2 1' event-set__4='_event: mouseleave; scale: 1 1 1' set-image='on: click; target: #image-current; src: #arrow-forward' sound='on: click; src: #click-sound'  ></a-entity>
    </a-entity>
  </a-entity>
  <a-entity id='goBackwardLink' layout='type: line; margin: 1.5' position='0 -1.2 6' rotation='0 180 0' visible='visible' scale=''>
    <a-entity template='src: #link' data-src='#arrow-backward' data-thumb='#arrow-thumb'  >
        <a-entity class='link' geometry='primitive: plane; height: 0.5; width: 1' material='shader: flat; src: #arrow-thumb; alphaTest: 0.5; opacity: 0.6' event-set__1='_event: mousedown; scale: 1 1 1' event-set__2='_event: mouseup; scale: 1.2 1.2 1' event-set__3='_event: mouseenter; scale: 1.2 1.2 1' event-set__4='_event: mouseleave; scale: 1 1 1' set-image='on: click; target: #image-current; src: #arrow-backward' sound='on: click; src: #click-sound'  ></a-entity>
    </a-entity>
  </a-entity>
<a-camera>
    <a-cursor id='cursor' event-set__1='_event: mouseenter; color: springgreen' event-set__2='_event: mouseleave; color: black' fuse='true' raycaster='objects: .link'   material='' line='' cursor='' geometry=''></a-cursor>
  </a-camera>
</a-scene>

</body>
</html>
"""


def generate_index_html(file_path, title, num_rows, num_col, image_extension):
    """
    Generates an aframe HTML with the required parameters
    :param file_path: session path
    :param title: title of the html to be generated
    :param num_rows: number of rows input
    :param num_col: number of columns input
    :param image_extension: type of image (jpg, png)
    :return:
    """
    print('current directory = ',os.path.basename(os.getcwd()))
    if os.path.basename(os.getcwd()) == 'vrticl':
        src_files = os.listdir(os.path.join(os.getcwd(),'utility','static'))
    else:
        src_files = os.listdir(os.path.join(dirname(os.getcwd()),'utility','static'))

    for file_name in src_files:
        full_file_name = os.path.join('static', file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, os.path.join(file_path,'static'))

    f = open(os.path.join(file_path,'index.html'), 'w')

    message = get_html_string(title, num_rows, num_col, image_extension)

    f.write(message)
    f.close()


def generate_package_web_tour(file_path, title, num_rows, num_col, package_path):
    """
    Makes function calls to generate the package for web tour based on user inputs
    :param file_path: input file path where the file is present
    :param title: title of the web tour to be generated
    :param num_rows: number of rows input by user
    :param num_col: number of columns input by user
    :param is_test: flag to indicate if the function is called for testing purpose or not
    :return:
    """

    validation_result = False

    # Generate a unique session identifier
    session_identifier = uuid.uuid4()

    # Create a local folder with this unique session identifier
    if package_path == 'default':
        if os.path.basename(os.getcwd()) == 'vrticl':
            session_dir = os.path.join(os.getcwd(),'session',str(session_identifier))
        else:
            session_dir = os.path.join(dirname(os.getcwd()), 'session', str(session_identifier))

    # session_dir = os.path.join(dirname(os.getcwd()), 'session', str(session_identifier))
    os.makedirs(os.path.join(session_dir), exist_ok=True)

    # Extract files to the session identifier directory
    extracted_images_path = extract_files(file_path, session_dir)
    print('extracted_images_path = ', extracted_images_path)

    # Get the image file extension
    image_extension = get_file_extension(session_dir)
    print('extension=', image_extension)

    # Check if user input is valid
    if image_extension is not None:
        validation_result = validate_input(image_extension, num_rows, num_col, extracted_images_path)
        print('validate result', validation_result)

        if validation_result:
            rename_images(num_rows, num_col, extracted_images_path, image_extension)
            generate_index_html(session_dir, title, num_rows, num_col, image_extension.split('.')[1])
            shutil.make_archive(session_dir, 'zip', session_dir)
            return '', session_identifier
        else:
            shutil.rmtree(session_dir)
            return "There was an error with the input.", session_identifier

    # Delete files if created for testing or invalid image input
    else:
        shutil.rmtree(session_dir)
        return "There was an error with the image files in the zip folder.", session_identifier


if __name__ == "__main__":
    file_path, title, num_rows, num_col = get_input()
    message, session_identifier = generate_package_web_tour(file_path, title, num_rows, num_col, 'default')
