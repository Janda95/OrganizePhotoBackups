'''File Handler Supporting Library'''
import shutil
import os


def find_media_in_dir(files):
    '''Return all jpg files in directory'''
    photo_media = []
    video_media = []

    # get supported types
    photo_types = ['jpg', 'png']
    video_types = ['mp4']

    for file_name in files:
        # split and check last token, -> jpg
        tokens = file_name.split('.')
        if tokens[-1] in photo_types:
            photo_media.append(f'{file_name}')
        elif tokens[-1] in video_types:
            video_media.append(f'{file_name}')

    return photo_media, video_media


def create_dir(filepath):
    '''Create Directory if it does not exist'''
    if not os.path.exists(filepath):
        os.makedirs(filepath)


def move_file_shutil(file_dir, media_file, dest):
    '''Move file to destination if file doesn't overwrite'''
    original = f'{file_dir}{media_file}'
    dest = f'{dest}/{media_file}'

    if os.path.isfile(dest) is False:
        shutil.move(original, dest)
        return True

    return False
