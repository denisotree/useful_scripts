import os
import argparse
import re
import logging
import multiprocessing
from logging.config import dictConfig

from PIL import Image
import tqdm

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(name)-24s %(levelname)-8s %(message)s'
        },
    },
    'handlers': {
        'default_stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default_stdout'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

dictConfig(LOGGING)

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--source', type=str, help='Images source folder')
parser.add_argument('-t', '--target', type=str, help='Images target folder')
parser.add_argument('--size', type=int, help='Images max size both dimensions')


class ImageResize:

    def __init__(
            self,
            source_path: str,
            max_image_size: int,
            target_path: str
    ):
        self._source_path = source_path
        self._target_path = target_path
        self._max_image_size = max_image_size

    def _resize_image(self, image_path):
        if isinstance(self._max_image_size, int) and self._max_image_size > 0:
            image = Image.open(image_path)
            image.thumbnail((self._max_image_size, self._max_image_size))
            image.save(os.path.join(self._target_path, os.path.basename(image_path)), quality=50, optimize=True)
        else:
            logging.error('Incorrect imagesize')

    def resize_images(self):
        if not self._target_path:
            self._target_path = 'output_images'
        if not os.path.exists(self._target_path):
            os.mkdir(self._target_path)

        if self._source_path and os.path.exists(self._source_path):
            for dirpath, dirnames, filenames in os.walk(self._source_path):
                files = [os.path.join(dirpath, f) for f in filenames if
                         f.endswith((".jpg", ".png")) and not re.search(r'\d+x\d+.', f)]
                with multiprocessing.Pool(8) as pool:
                    list(tqdm.tqdm(pool.imap(self._resize_image, files), total=len(files)))
        else:
            logging.error('Set source folder')


if __name__ == '__main__':

    args = parser.parse_args()

    source_dir = args.source
    target_dir = args.target
    max_size = args.size

    resizer = ImageResize(
        source_path=source_dir,
        max_image_size=max_size,
        target_path=target_dir
    )

    resizer.resize_images()
