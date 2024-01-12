'''Python3 Script for organizing large groups of unorganized photos'''
import os
import sys
import shutil
import ffmpeg
from tqdm import tqdm
from PIL import Image

DEFAULT_DEST = "MetadataNotFound"


def find_media_in_dir(files):
    '''Return all jpg files in directory'''
    photo_media = []
    video_media = []
    photo_types = ["jpg", "png"]
    video_types = ["mp4"]

    for file_name in files:
        # split and check last token, -> jpg
        tokens = file_name.split(".")
        if tokens[-1] in photo_types:
            photo_media.append(f"{file_name}")
        elif tokens[-1] in video_types:
            video_media.append(f"{file_name}")

    return photo_media, video_media


def create_dir(filepath):
    '''Create Directory if it does not exist'''
    if not os.path.exists(filepath):
        os.makedirs(filepath)


def move_media(file_dir, media_file, dest):
    '''Move media file to destination'''
    original = f"{file_dir}{media_file}"
    dest = f"{dest}/{media_file}"
    shutil.move(original, dest)


def add_record(transactions, media_file, dest):
    '''Add record to transactions'''
    val = transactions.get(dest, [])
    val.append(media_file)
    transactions[dest] = val


def pp_transactions(transactions):
    '''Pretty Print Transactions records'''
    for k, v in sorted(transactions.items()):
        msg = f"\n{k}:"
        for val in v:
            msg += f"\n    {val}"
        print(msg)


def video_copy_n_sort(videos, source_dir, transactions):
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
            tokens = video_stream['tags']['creation_time'].split("-")
            date_dir = f'{source_dir}{tokens[0]}_{tokens[1]}'
        except Exception:
            date_dir = default_dir

        create_dir(date_dir)
        move_media(source_dir, vid, date_dir)
        add_record(transactions, vid, date_dir)


def img_copy_n_sort(jpg_files, source_dir, transactions):
    '''Logic handling copying and organizing photos'''
    # Create default directory
    default_dir = f'{source_dir}{DEFAULT_DEST}'

    # Move each image and display progress
    for pic in tqdm(jpg_files):
        try:
            img_file = Image.open(f'{source_dir}{pic}')
        except Exception as e:
            print(f"Invalid Image: {e}")

        exif = img_file.getexif()
        timestamp = exif.get(306, None)
        date_dir = default_dir

        # Timestamp Metadata found, prepare date directory
        if timestamp is not None:
            time_tokens = timestamp.split()
            date = time_tokens[0].split(":")
            date_dir = f"{source_dir}{date[0]}_{date[1]}"

        create_dir(default_dir)
        move_media(source_dir, pic, date_dir)
        add_record(transactions, pic, date_dir)


def main(source_dir):
    '''Check Directory and find jpg files'''
    try:
        arr = os.listdir(source_dir)
    except Exception as e:
        print(f"Non-Valid Directory: {e}")
        return

    imgs, videos = find_media_in_dir(arr)

    # Return message if no media is found
    if len(imgs) == 0 and len(videos) == 0:
        print("No Media found in !")
        return

    msg = f"{len(imgs)} images and {len(videos)} videos found in {os.getcwd()}/{source_dir}"
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
    transactions = {}
    img_copy_n_sort(imgs, source_dir, transactions)
    video_copy_n_sort(videos, source_dir, transactions)

    pp_transactions(transactions)


if __name__ == "__main__":
    # Pass on optional filepath for jpg locations.
    try:
        # Format: ../ or DIR/
        SOURCE_DIR = str(sys.argv[1])
    except IndexError:
        print("Optional path not given, current directory used as default.")
        SOURCE_DIR = "/"

    main(SOURCE_DIR)
