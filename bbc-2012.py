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
    filename = filename.replace('2012-', '2012_')
    if filename.startswith('2012'):
        tmp, _ = filename.split('-', 1)
    else:
        tmp, _ = filename.rsplit('.', 1)
    tmp2 = tmp.split('_')
    year, month, day = tmp2[-3:]

    datestamp = f"{int(year)}-{int(month)}-{int(day)}"

    if datestamp[0] in [1, 2, '1', '2']:
        return datestamp

    raise ValueError('Invalid date found')


BASE_DIR = pathlib.Path('//storage/music/BBC Essential Mix Archive/2012')

for file in BASE_DIR.glob('**/*.*'):
    print(file)
    old_filename = file.name
    old_filename = old_filename.replace('_www.qrip.org', '').replace('_qrip', '')

    if 'Essential Mix' not in old_filename or old_filename.endswith('.rtf'):
        print('\tSkipping')
        continue

    ds = get_datestamp_from_filename(old_filename)
    releasetime = get_releasetime(ds)

    index = 0
    end_index = len(old_filename)-14
    if old_filename.startswith('2012'):
        index = 11
        end_index = len(old_filename)+1

    filename_structure = old_filename[index:end_index].replace('Essential Mix', '', 1).replace('BBC Radio1', '').replace(' _ ', ' & ').strip()

    tmp = filename_structure.split(' ')
    _, ext = old_filename.rsplit('.', 1)
    if old_filename.startswith('2012'):
        tmp4 = ' '.join(tmp[4:])
    else:
        tmp4 = ' '.join(tmp[:-3])

    new_filename = f"{releasetime:%Y-%m-%d} - {filename_structure.strip()}".replace('_', '')
    new_filepath = file.parent.parent.parent / new_filename

    print(new_filepath)

    if new_filepath.exists():
        raise ValueError('File already exists!')

    # print(file.rename(new_filepath))

    print('####')

