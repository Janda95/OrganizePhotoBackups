'''Python3 script organizing batches of jpg, png, and mp4 files by timestamp metadata'''
import os
import sys
from tqdm import tqdm
import file_handler_util as fhutil

DEFAULT_DEST = 'Timestamp_Unavailable'


def add_record(transactions, media_file, dest, is_file_moved):
    '''Add record to transactions'''
    if is_file_moved is False:
        # overide intended destination with error msg
        dest = "File not moved, destination already exists"

    val = transactions.get(dest, [])
    val.append(media_file)
    transactions[dest] = val


def pp_transactions(transactions):
    '''Pretty Print Transactions records'''
    for k, v in sorted(transactions.items()):
        msg = f'\n{k}:'
        # tab indent styling
        for val in v:
            msg += f'\n    {val}'
        print(msg)


def file_copy_n_sort(files, source_dir, transactions, dir_layout):
    """Move files and record every transaction"""
    default_dir = f'{source_dir}{DEFAULT_DEST}'

    for media_file in tqdm(files):
        date_dir = media_file.generate_file_dest(dir_layout)
        if date_dir is None:
            date_dir = default_dir

        # record status, add to transactions
        is_file_moved = fhutil.move_file_shutil(
            media_file.source_dir, media_file.file_name, date_dir)
        add_record(transactions, media_file.file_name, date_dir, is_file_moved)


def move_files(source_dir):
    '''Check Directory and find jpg files'''
    files, file_records = fhutil.find_media_in_dir(source_dir)

    # Return message if no media is found
    if len(files) == 0:
        print(f'No Media found in {os.getcwd()}/{source_dir}!')
        sys.exit(1)

    msg = f"\nFiles found in {os.getcwd()}/{source_dir}:"
    # tab indent styling
    for k, v in file_records.items():
        msg += f'\n    {k}: {v}'
    print(msg)

    valid_res = False
    # ask for confirmation until expected reponse or exit
    while valid_res is False:
        res = input('\nWould you like to sort these images? (y/n): ')
        if res.strip() == 'y':
            valid_res = True
        elif res.strip() == 'n':
            print('Abort recieved, no images have been relocated.')
            sys.exit(1)
        else:
            valid_res = False
            print("Invalid input, please try again. /n")

    dir_layout = None
    # request dir layout sorting style
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
            dir_layout = None
            print('Invalid input, please try again.')

    transactions = {}
    file_copy_n_sort(files, source_dir, transactions, dir_layout)
    pp_transactions(transactions)


if __name__ == "__main__":
    # Pass on optional filepath for jpg locations.
    try:
        # Format: ../ or DIR/
        SOURCE_DIR = str(sys.argv[1])
    except IndexError:
        print('No Path Provided: Current directory will be used.')
        SOURCE_DIR = '/'

    move_files(SOURCE_DIR)
