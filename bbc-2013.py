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
    tmp, _ = filename.split('-', 1)
    tmp2 = tmp.split('_')
    year, month, day = tmp2[-3:]

    datestamp = f"{year}-{month}-{day}"

    if datestamp[0] in [1, 2, '1', '2']:
        return datestamp

    raise ValueError('Invalid date found')


BASE_DIR = pathlib.Path('//storage/music/BBC Essential Mix Archive/2013')

for file in BASE_DIR.glob('**/*.*'):
    print(file)
    old_filename = file.name
    old_filename = old_filename.replace('_www.qrip.org', '').replace('_qrip', '').replace('BBC Radio1', '').replace(' _ ', ' & ')

    if 'Essential Mix' not in old_filename:
        print('\tSkipping')
        continue

    ds = get_datestamp_from_filename(old_filename)
    releasetime = get_releasetime(ds)

    filename_structure = old_filename.replace('Essential Mix', '', 1).split('-', 1)

    if len(filename_structure) != 2:
        raise ValueError('filename is not in the structure we are expecting')

    tmp = filename_structure[-1]
    tmp, ext = tmp.rsplit('.', 1)

    tmp = tmp.replace('_', ' ').strip()

    new_filename = f"{releasetime:%Y-%m-%d} - {tmp.strip()}.{ext}".replace('  Celebrate 20 Years of Essential Mix', '').replace(' .mp3', '.mp3')
    new_filepath = file.parent.parent / new_filename

    print(new_filepath)

    if new_filepath.exists():
        raise ValueError('File already exists!')

    # print(file.rename(new_filepath))

    print('####')

