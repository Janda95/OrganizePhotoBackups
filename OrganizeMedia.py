'''Python3 Script for organizing batches of jpg, png, and mp4 files with timestamp metadata'''
import os
import sys
from tqdm import tqdm
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


def file_copy_n_sort(files, source_dir, transactions, dir_layout):
    """Move files and record every transaction"""
    default_dir = f'{source_dir}{DEFAULT_DEST}'

    for media_file in tqdm(files):
        date_dir = media_file.generate_file_dest(dir_layout)
        if date_dir is None:
            date_dir = default_dir

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
    file_copy_n_sort(files, source_dir, transactions, dir_layout)
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
