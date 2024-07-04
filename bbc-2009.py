"""

Reformats BBC Radio 1 Essential Mix Archive from

2009-01-10 - EM - Funkgenda (MP2)/2009-01-10 - EM - Funkgenda.mp2

to

2007-05-27 - Carl Cox.mp3

I then used mp3tag to fix title, artist...etc

"""
import re
import datetime
import pathlib


def get_releasetime(value):
    if value.count('.') == 2:
        return datetime.datetime.strptime(value, '%Y.%m.%d').date()
    elif value.count('-') == 2:
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()

    raise ValueError('Invalid date format')


def get_datestamp_from_filename(filename):
    tmp = filename.split(' - ')
    datestamp = tmp[0]

    if datestamp[0] in [1, 2, '1', '2']:
        return datestamp

    raise ValueError('Invalid date found')


BASE_DIR = pathlib.Path('//storage/music/BBC Essential Mix Archive/2009')

for file in BASE_DIR.glob('**/*.*'):
    print(file)
    old_filename = file.name

    if ' em ' not in old_filename.lower():
        print('\tSkipping')
        continue

    ds = get_datestamp_from_filename(old_filename)
    releasetime = get_releasetime(ds)

    filename_structure = old_filename.split(' - EM - ')

    if len(filename_structure) != 2:
        raise ValueError('filename is not in the structure we are expecting')

    new_filename = f"{releasetime:%Y-%m-%d} - {filename_structure[-1].strip()}"
    new_filepath = file.parent.parent / new_filename

    print(new_filepath)

    if new_filepath.exists():
        raise ValueError('File already exists!')

    # print(file.rename(new_filepath))

    print('####')

