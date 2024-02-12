'''Python3 Script for organizing batches of jpg, png, and mp4 files with timestamp metadata'''
import os
import sys
import ffmpeg
from tqdm import tqdm
from PIL import Image
import FileHandlerUtil as fhutil


DEFAULT_DEST = 'Timestamp_Unavailable'


def add_record(transactions, media_file, dest, is_file_moved):
    '''Add record to transactions'''
    if is_file_moved is False:
        dest = "Files Not Moved (File already existed at destination)"

    val = transactions.get(dest, [])
    val.append(media_file)
    transactions[dest] = val


def pp_transactions(transactions):
    '''Pretty Print Transactions records'''
    for k, v in sorted(transactions.items()):
        msg = f'\n{k}:'
        for val in v:
            msg += f'\n    {val}'
        print(msg)


def generate_date_dir(source_dir, year, month, dir_layout):
    '''Generate correct requested date dir based on user input'''
    date_dir = ""

    if dir_layout == 'month':
        date_dir = f'{source_dir}{month}'
    elif dir_layout == 'year':
        date_dir = f'{source_dir}{year}'
    elif dir_layout == 'year_month':
        date_dir = f'{source_dir}{year}_{month}'
    elif dir_layout == 'year/month':
        date_dir = f'{source_dir}{year}/{month}'
    else:
        print('Invalid dir_layout provided')
        sys.exit(1)

    return date_dir


def video_copy_n_sort(videos, source_dir, transactions, dir_layout):
    '''Logic handling copying and organizing video files'''
    default_dir = f'{source_dir}{DEFAULT_DEST}'

    for vid in tqdm(videos):

        vid_location = f'{source_dir}{vid}'

        try:
            probe = ffmpeg.probe(vid_location)
        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)
            sys.exit(1)

        video_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
            None)
        if video_stream is None:
            print('No video stream found', file=sys.stderr)
            sys.exit(1)

        try:
            tokens = video_stream['tags']['creation_time'].split('-')
            date_dir = generate_date_dir(source_dir, tokens[0], tokens[1], dir_layout)
        except IndexError:
            date_dir = default_dir

        fhutil.create_dir(date_dir)
        is_file_moved = fhutil.move_file_shutil(source_dir, vid, date_dir)
        add_record(transactions, vid, date_dir, is_file_moved)

    # did not move these files, would replace file with same name
    

def img_copy_n_sort(jpg_files, source_dir, transactions, dir_layout):
    '''Logic handling copying and organizing photos'''
    # Create default directory
    default_dir = f'{source_dir}{DEFAULT_DEST}'

    # Move each image and display progress
    for pic in tqdm(jpg_files):
        try:
            img_file = Image.open(f'{source_dir}{pic}')
        except IOError as e:
            print(f'Invalid Image: {e}')

        exif = img_file.getexif()
        timestamp = exif.get(306, None)
        date_dir = default_dir

        # Timestamp Metadata found, prepare date directory
        if timestamp is not None:
            time_tokens = timestamp.split()
            date = time_tokens[0].split(':')
            date_dir = generate_date_dir(source_dir, date[0], date[1], dir_layout)

        fhutil.create_dir(date_dir)
        is_file_moved = fhutil.move_file_shutil(source_dir, pic, date_dir)

        add_record(transactions, pic, date_dir, is_file_moved)


def move_files(source_dir):
    '''Check Directory and find jpg files'''
    try:
        arr = os.listdir(source_dir)
    except Exception as e:
        print(f"Non-Valid Directory: {e}")
        return

    imgs, videos = fhutil.find_media_in_dir(arr)

    # Return message if no media is found
    if len(imgs) == 0 and len(videos) == 0:
        print(f'No Media found in {os.getcwd()}/{source_dir}!')
        sys.exit(1)

    msg = f'{len(imgs)} images and {len(videos)} videos found in {os.getcwd()}/{source_dir}'
    print(msg)

    valid_res = False
    # ask for confirmation until expected reponse or exit
    while valid_res is False:
        res = input('\nWould you like to sort these images? (y/n): ')
        if res.strip() == 'y':
            valid_res = True
        elif res.strip() == 'n':
            print('Abort recieved, no images moved.')
            sys.exit(1)

    dir_layout = None
    # ask for confirmation regarding dir layout
    while dir_layout is None:
        res = input(
            '''\nWhich directory layout would you prefer?:
            year (y), month (m), year_month? (y_m), or year/month (y/m): ''')
        if res.strip() == 'y':
            dir_layout = 'year'
        elif res.strip() == 'm':
            dir_layout = 'month'
        elif res.strip() == 'y_m':
            dir_layout = 'year_month'
        elif res.strip() == 'y/m':
            dir_layout = 'year/month'
        else:
            print('Invalid input, please try again.')

    transactions = {}
    img_copy_n_sort(imgs, source_dir, transactions, dir_layout)
    video_copy_n_sort(videos, source_dir, transactions, dir_layout)

    pp_transactions(transactions)


if __name__ == "__main__":
    # Pass on optional filepath for jpg locations.
    try:
        # Format: ../ or DIR/
        SOURCE_DIR = str(sys.argv[1])
    except IndexError:
        print('Optional path not given, current directory used as default.')
        SOURCE_DIR = '/'

    move_files(SOURCE_DIR)
