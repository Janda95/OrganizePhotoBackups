"""Support and Factory classes for file type specific interactions"""
from abc import ABC, abstractmethod
import sys
import ffmpeg
from PIL import Image

class MediaFile(ABC):
    """Basic Media File Abstract Class"""
    def __init__(self, file_name, source_dir) -> None:
        super().__init__()
        self.source_dir = source_dir
        self.file_name = file_name


    @abstractmethod
    def generate_file_dest(self, dir_layout):
        """Implement file destination creation functionality"""


    def generate_dir(self, year, month, dir_layout):
        '''Generate correct requested date dir based on user input'''
        date_dir = ""
        source = self.source_dir

        if dir_layout == 'month':
            date_dir = f'{source}{month}'
        elif dir_layout == 'year':
            date_dir = f'{source}{year}'
        elif dir_layout == 'year_month':
            date_dir = f'{source}{year}_{month}'
        elif dir_layout == 'year/month':
            date_dir = f'{source}{year}/{month}'
        else:
            print('Invalid dir_layout provided')
            sys.exit(1)

        return date_dir


class Video(MediaFile):
    """Generic Video Datatype"""
    def generate_file_dest(self, dir_layout):
        """Generate date dir from video metadata"""
        vid_location = f'{self.source_dir}{self.file_name}'

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
            date_dir = self.generate_dir( tokens[0], tokens[1], dir_layout)
        except IndexError:
            date_dir = None

        return date_dir


class Photo(MediaFile):
    """Generic Photo Datatype"""
    def generate_file_dest(self, dir_layout):
        """Generate date dir from photo metadata"""
        try:
            img_file = Image.open(f'{self.source_dir}{self.file_name}')
        except IOError as e:
            print(f'Invalid Image: {e}')

        exif = img_file.getexif()
        timestamp = exif.get(306, None)
        date_dir = None

        # If Timestamp Metadata found, prepare date directory
        if timestamp:
            time_tokens = timestamp.split()
            date = time_tokens[0].split(':')
            date_dir = self.generate_dir( date[0], date[1], dir_layout )
            return date_dir

        return date_dir


class MediaFileFactory:
    """Media File Factory for creating available metadata media classes"""
    _file_types = {
        "mp4": Video,
        "jpg": Photo,
        "png": Photo
    }

    @classmethod
    def create(cls, file_type, file_name, source_dir):
        """Return valid class types"""
        file_class = cls._file_types.get(file_type)

        if file_class:
            return file_class(file_name, source_dir)

        # msg = str(file_name) + " data type is not supported"
        # print(msg)
        return None
