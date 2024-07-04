import re
import datetime
import pathlib


def get_releasetime(value):
    if value.count('.') == 2:
        return datetime.datetime.strptime(value, '%Y.%m.%d').date()
    elif value.count('-') == 2:
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()
    elif value.count('_') == 2:
        return datetime.datetime.strptime(value, '%Y_%m_%d').date()

    raise ValueError('Invalid date format')


def get_datestamp_from_filename(filename):
    tmp = filename.split(' - ')
    year, month, day = tmp[0].split('-')

    datestamp = f"{year}-{month}-{day}"

    if datestamp[0] in [1, 2, '1', '2']:
        return datestamp

    raise ValueError('Invalid date found')


BASE_DIR = pathlib.Path('//storage/music/BBC Essential Mix Archive/2023')

ext = 'm4a'
for file in BASE_DIR.glob(f'**/*.{ext}'):
    print(file)
    old_filename = file.name
    old_filename = old_filename.replace('_www.qrip.org', '').replace('_qrip', '').replace('BBC Radio1', '').replace(' _ ', ' & ')

    if 'Essential Mix' not in old_filename:
        print('\tSkipping')
        # continue

    ds = get_datestamp_from_filename(old_filename)
    releasetime = get_releasetime(ds)

    tmp = old_filename.replace(' - Essential Mix', '', 1)[12:]

    filename_structure = tmp.replace('...', '')

    new_filename = f"{releasetime:%Y-%m-%d} - {filename_structure.strip()}".replace(' .mp3', '.mp3')
    new_filepath = file.parent.parent / new_filename

    print(new_filepath)

    if new_filepath.exists():
        raise ValueError('File already exists!')

    # print(file.rename(new_filepath))

    print('####')

