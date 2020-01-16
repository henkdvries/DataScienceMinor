import os
import numpy as np


def read_raw(path: str, transpose: bool) -> list:
    result = list()
    header = None
    matrix = np.zeros((3, 3))
    with open(path, 'r') as f:
        index = 0
        for line in f:
            contents = line.split()
            if len(contents) < 1:  # skip is line is empty
                continue

            if len(contents) > 3:  # header length is longer due to the sensor number
                header = contents
                continue

            matrix[index] = contents
            index += 1

            if index == 3:
                if transpose:
                    matrix = matrix.transpose()
                result.append([header, matrix])
                header = None
                matrix = np.zeros((3, 3))
                index = 0

    return result


def walk_dir(dir: str, ext: str) -> list:
    """
    Walk through the given directory and look
    for the given extension

    :param str dir: Directory to look in
    :param str ext: File extension to look for
    :return: Path to the files and the warning occured
    :rtype: tuple
    """
    paths = list()

    for fd in os.listdir(dir):
        _path = os.path.join(dir, fd)
        if os.path.isdir(_path):
            paths.extend(walk_dir(_path, ext))

        if fd.endswith(ext) and os.path.isfile(_path):
            paths.append(_path)

    return paths


def touch_dir(path: str):
    """
    Create directory if not exist

    :param str path: path to directory
    """
    if not os.path.exists(path):
        os.makedirs(path)  # mkdir -p <path>


if __name__ == '__main__':
    for file in walk_dir('/home/yuqi/Downloads/raw_data/cat_4', 'txt'):
        sub, fn = file.split('/')[-2:]
        raw = read_raw(file, transpose=True)
        out = '/home/yuqi/out/%s' % sub
        path = '%s/%s' % (out, fn)
        touch_dir(out)

        with open(path, 'w') as f:
            for line in raw:
                header = '{0}     {1}   {2}   {3} \n'.format(*line[0])
                content = '      {0}   {1}   {2} \n' \
                          '      {3}   {4}   {5} \n' \
                          '      {6}   {7}   {8} \n'.format(*line[1][0], *line[1][1], *line[1][2])

                f.write(header)
                f.write(content)
                f.write('\n')
