import argparse
import os

from gendiff.parsers import get_parser


def init():
    desc = 'Compares two configuration files and shows a difference.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()
    _, ext = os.path.splitext(args.first_file)

    return generate_diff(args.first_file, args.second_file, ext[1:])


def generate_diff(filepath1, filepath2, ext) -> str:
    parse = get_parser(ext)

    with open(filepath1) as f1:
        file1 = parse(f1)
    with open(filepath2) as f2:
        file2 = parse(f2)

    keys = set(file1.keys()).union(set(file2.keys()))

    diff = {}
    # 'added' | 'deleted' | 'modified' | 'unmodified'

    for key in keys:
        if key in file1 and key in file2:
            if file1[key] == file2[key]:
                diff[key] = 'unmodified'
            else:
                diff[key] = 'modified'

        elif key in file1 and key not in file2:
            diff[key] = 'deleted'
        elif key not in file1 and key in file2:
            diff[key] = 'added'

    return show_diff(diff)


def show_diff(diff) -> str:
    formatted_diff = '{\n'

    for key in sorted(diff.keys()):
        if diff[key] == 'unmodified':
            formatted_diff += '    {k}\n'.format(k=key)
        elif diff[key] == 'added':
            formatted_diff += '  + {k}\n'.format(k=key)
        elif diff[key] == 'deleted':
            formatted_diff += '  - {k}\n'.format(k=key)
        elif diff[key] == 'modified':
            formatted_diff += '  - {k}\n'.format(k=key)
            formatted_diff += '  + {k}\n'.format(k=key)

    formatted_diff += '}'
    return formatted_diff
