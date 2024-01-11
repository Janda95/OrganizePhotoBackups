'''Python3 Script for organizing large groups of unorganized photos'''
import os
import sys
import shutil
from tqdm import tqdm
from PIL import Image


def find_jpgs_in_dir(files):
    '''Return all jpg files in directory'''
    jpgs = []
    for file_name in files:
        # split and check last token, -> jpg
        tokens = file_name.split(".")
        if tokens[-1] == "jpg":
            jpgs.append(f"{file_name}")
    return jpgs


def create_dir(filepath):
    '''Create Directory if it does not exist'''
    if not os.path.exists(filepath):
        os.makedirs(filepath)


def img_copy_n_sort(jpg_files, file_dir):
    '''Logic handling copying and organizing photos'''
    # Tracking image destinations
    transactions = {}

    # Create default directory
    default_dir = f'{file_dir}NoDateData'
    create_dir(default_dir)

    # Move each image and display progress
    for jpg in tqdm(jpg_files):
        try:
            img = Image.open(f'{file_dir}{jpg}')
        except Exception as e:
            print(f"Invalid Image: {e}")

        exif = img.getexif()
        timestamp = exif.get(306, None)

        # No Timestamp Metadata, Move image to default directory
        if timestamp is None:
            original = f"{file_dir}{jpg}"
            dest = f"{default_dir}/{jpg}"
            shutil.move(original, dest)

            # Add record
            val = transactions.get(default_dir, [])
            val.append(jpg)
            transactions[default_dir] = val
            continue

        time_tokens = timestamp.split()
        date = time_tokens[0].split(":")

        # prep paths/dir and move image
        date_dir = f"{file_dir}{date[0]}_{date[1]}"
        create_dir(date_dir)

        original = f"{file_dir}{jpg}"
        dest = f"{date_dir}/{jpg}"
        shutil.move(original, dest)

        # Add record
        val = transactions.get(date_dir, [])
        val.append(jpg)
        transactions[date_dir] = val

    return transactions


def pp_transactions(transactions):
    '''Pretty Print Transactions records'''
    for k, v in sorted(transactions.items()):
        msg = f"\n{k}:"
        for val in v:
            msg += f"\n    {val}"
        print(msg)


def main(jpg_dir):
    '''Check Directory and find jpg files'''
    try:
        arr = os.listdir(jpg_dir)
    except Exception as e:
        print(f"Non-Valid Directory: {e}")
        return

    jpgs = find_jpgs_in_dir(arr)

    # Return message if no jpgs found
    if len(jpgs) == 0:
        print("No Jpgs found!")
        return

    # confirm with user if these listed images should be moved
    msg = f"{len(jpgs)} jpgs found in {os.getcwd()}/{jpg_dir}"
    print(msg)

    valid_res = False
    # ask for confirmation until expected reponse or exit
    while valid_res is False:
        res = input("\nWould you like to sort these images? (y/n): ")
        if res.strip() == "y":
            valid_res = True
        elif res.strip() == "n":
            print("Abort recieved, no images moved.")
            return

    # Copy images into year_month dir and display transactions to user
    transactions = img_copy_n_sort(jpgs, jpg_dir)
    pp_transactions(transactions)


if __name__ == "__main__":
    # Pass on optional filepath for jpg locations.
    try:
        # Format: ../ or DIR/
        JPG_DIR = str(sys.argv[1])
    except IndexError:
        print("Optional path not given, current directory used as default.")
        JPG_DIR = "/"

    main(JPG_DIR)
