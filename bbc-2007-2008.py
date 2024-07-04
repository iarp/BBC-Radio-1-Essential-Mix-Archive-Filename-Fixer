"""

Reformats BBC Radio 1 Essential Mix Archive from

Carl Cox EM 2007-05-27.mp3

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
    tmp = filename.split('.')

    filename_without_ext = tmp[-2]

    if filename_without_ext.count('+') > 1:
        tmp2 = filename_without_ext.split('+')
        datestamp = tmp2[-1]
    else:
        tmp3 = filename_without_ext.split(' ')
        datestamp = tmp3[-1]

    if datestamp[0] in [1, 2, '1', '2']:
        return datestamp

    raise ValueError(f'Invalid date found {datestamp}')


BASE_DIR = pathlib.Path('//storage/music/BBC Essential Mix Archive/2008')

for file in BASE_DIR.glob('*.*'):
    print(file)
    old_filename = file.name
    if old_filename.count('+') > 1:
        old_filename = old_filename.replace('+', ' ')

    if ' em ' not in old_filename.lower():
        print('\tSkipping')
        continue

    ds = get_datestamp_from_filename(old_filename)
    releasetime = get_releasetime(ds)

    filename_structure = old_filename.split(' EM ')
    _, ext = old_filename.rsplit('.', 1)

    if len(filename_structure) != 2:
        raise ValueError('filename is not in the structure we are expecting')

    new_filename = f"{releasetime:%Y-%m-%d} - {filename_structure[0].strip()}.{ext}"
    new_filepath = file.parent / new_filename

    print(new_filepath)

    if new_filepath.exists():
        raise ValueError('File already exists!')

    # print(file.rename(new_filepath))

    print('####')

