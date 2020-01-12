import os
import fnmatch
import fileinput
import logging
import argparse


def check_factory(path_beg):
    def check_path(path):
        # print("last char :", path_beg[len(path):len(path)+1])
        return path_beg.startswith(path) and path_beg[len(path):len(path) + 1] in ('\\', '/')

    return check_path


def check_if_seen_before(path, pathlist):
    # print(path, pathlist)

    check_func = check_factory(path)
    return len(list(filter(check_func, pathlist)))


def search_name(src_dir, file_pattern):
    """
    This function will accept source folder and file name pattern
    to search for and print results to the standard output

    Args:
        src_dir: Directory where to look for
        file_pattern: File pattern to look for e.g. Somefile*.txt

    Returns:
        None
    
    Prints: 
        Result into std.out

    """
    found_anything = 0

    # This loop will walk recursively in the dir and produce tuple of found dir and files
    for path, _, file_list in os.walk(src_dir):

        # Filter and return all files that match pattern from the list
        matched_files = fnmatch.filter(file_list, file_pattern)
        if fnmatch.fnmatch(path, file_pattern) or len(matched_files):

            seen_before = check_if_seen_before(path, found_path_list)
            # print(f'seen before: {seen_before}')
            files_found = len(matched_files)
            if not seen_before:
                found_path_list.append(path)

            if not seen_before and not files_found:
                print(path)

            if len(matched_files):
                print(path)
                print('\t' + str(matched_files))

            found_anything = 1

    return found_anything


def search_text(src_dir, file_pattern, search_text_):
    """
    """
    found_anything = 0

    # This loop will walk recursively in the dir and produce tuple of all dirs and files
    for path, _, file_list in os.walk(src_dir):

        # Filter and return all files that match file name pattern from the list 
        matched_files = fnmatch.filter(file_list, file_pattern)
        if len(matched_files):
            matched_files_with_path = [os.path.join(path, file) for file in matched_files]
            # print(matched_files_with_path)
            in_file = ''
            with fileinput.input(files=matched_files_with_path) as file:
                try:
                    for line in file:
                        if fnmatch.fnmatch(line, search_text_):
                            if in_file != file.filename():
                                print('Found in file: {}'.format(file.filename()))
                                in_file = file.filename()
                            print('\tLine no:"{}" ***: {}'.format(file.lineno(), line.replace('\n', '')))
                            found_anything = 1
                except UnicodeDecodeError:
                    logger.warning("Unicode error in: {}".format(file.filename()))
                    file.nextfile()
                except PermissionError:
                    logger.warning("Dont have permission to: {}".format(file.filename()))
                    file.nextfile()

    return found_anything

# Windows
# src = 'C:\\Users\\khalid\\Documents\\SomeProj\\src'
# pattern = '*.py'
# some_value = 'hello'

# src = '/home/khalid/dev'
# pattern = '*.py'
# some_value = 'hello'


found_path_list = []
logging_level = logging.ERROR
# logging_level = logging.INFO

# Setup logger
logging.basicConfig(level=logging_level,
                    format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

if __name__ == "__main__":
    """
    This tool searches for files and a text within a file.
    Two modes possible, to search for a file name (pattern)
    or to search file for a file (with pattern) with a
    specific string
    
    Usage: 
        find_file.py [-h] --dir DIR --filename FILENAME [--text TEXT]
    
    Example:
        1)
            find_file.py --dir /home/khalid/dev --filename *.py 
        2)        
            find_file.py --dir /home/khalid/dev --filename *.py --text hello

      
    """

    # Parse arguments
    parser = argparse.ArgumentParser(description='Find files or text within files')
    parser.add_argument('--dir'
                        , required=True
                        , help='Directory to look for')
    parser.add_argument('--filename'
                        , required=True
                        , help='File name to search for i.g. *.cfg or *some*file.txt')
    parser.add_argument('--text',
                        help='Some text to search for. Can be omitted and then only search for based on file name')
    args = parser.parse_args()

    # Initialise
    src = args.dir
    pattern = args.filename
    some_value = args.text

    print('')
    print('**********************')
    print('Searching text:    {}'.format(some_value))
    print('Inside dir:        {}'.format(src))
    print('With file pattern: {}'.format(pattern))
    print('**********************')
    print('RESULT:')
    print('')

    if some_value:
        some_value = some_value.center(len(some_value) + 2, '*')
        found_anything = search_text(src, pattern, some_value)
    else:
        found_anything = search_name(src, pattern)

    if not found_anything:
        print('Nothing has found.')

    print('')
    print('****** COMPLETED ******')
