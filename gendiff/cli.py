import argparse
import json


def init():
    parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()
    return generate_diff(args.first_file, args.second_file)


def generate_diff(filepath1, filepath2):
    file1 = json.load(open(filepath1))
    file2 = json.load(open(filepath2))

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


def show_diff(diff):
    result = '{\n'

    for key in sorted(diff.keys()):
        if diff[key] == 'unmodified':
            result += f'    {key}\n'
        elif diff[key] == 'added':
            result += f'  + {key}\n'
        elif diff[key] == 'deleted':
            result += f'  - {key}\n'
        elif diff[key] == 'modified':
            result += f'  - {key}\n'
            result += f'  + {key}\n'

    result += '}'
    return result
