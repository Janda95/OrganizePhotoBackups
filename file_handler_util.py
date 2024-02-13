'''File Handler Supporting Library'''
import shutil
import os
from file_classes import MediaFileFactory as mff


def find_media_in_dir(source_dir):
    '''Return all jpg files in directory'''

    try:
        files = os.listdir(source_dir)
    except Exception as e:
        print(f"Non-Valid Directory: {e}")
        return

    supported_files = []
    filetype_count = {}
    for file_name in files:
        # split and check last token, -> jpg
        tokens = file_name.split('.')
        file_type = tokens[-1]
        media_file = mff.create(file_type, file_name, source_dir)

        if media_file:
            filetype_count[file_type] = filetype_count.get(file_type, 0) + 1
            supported_files.append(media_file)

    return supported_files, filetype_count


def create_dir(filepath):
    '''Create Directory if it does not exist'''
    if not os.path.exists(filepath):
        os.makedirs(filepath)


def move_file_shutil(file_dir, media_file, dest):
    '''Move file to destination if file doesn't overwrite'''
    create_dir(dest)
    original = f'{file_dir}{media_file}'
    destination = f'{dest}/{media_file}'

    if os.path.isfile(destination) is False:
        shutil.move(original, dest)
        return True

    return False
