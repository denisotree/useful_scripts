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
parser.add_argument('--size', type=int, help='Images max size both dimentions')


def resize_image(image_path):
    if isinstance(max_imagesize, int) and max_imagesize > 0:
        image = Image.open(image_path)
        image.thumbnail((max_imagesize, max_imagesize))
        image.save(os.path.join(target_dir, os.path.basename(image_path)))
    else:
        logging.error('Incorrect imagesize')


def resize_images(source_path, target_path, max_size):
    if not target_path:
        target_path = 'output_images'
        if not os.path.exists(target_path):
            os.mkdir(target_path)
    elif not os.path.exists(target_path):
        os.mkdir(target_path)

    if source_dir and os.path.isdir(source_path):
        for dirpath, dirnames, filenames in os.walk(source_path):
            files = [os.path.join(dirpath, f) for f in filenames if
                     f.endswith((".jpg", ".png")) and not re.search(r'\d+x\d+.', f)]
            with multiprocessing.Pool(8) as pool:
                r = list(tqdm.tqdm(pool.imap(resize_image, files), total=len(files)))
    else:
        logging.error('Set source folder')


if __name__ == '__main__':

    args = parser.parse_args()

    source_dir = args.source
    target_dir = args.target
    max_imagesize = args.size

    resize_images(source_dir, target_dir, max_imagesize)
