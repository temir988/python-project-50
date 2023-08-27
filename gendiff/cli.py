import argparse
import os
import json
from pprint import pprint

from gendiff.parsers import get_parser
from gendiff.stylish import show_diff


def init():
    desc = 'Compares two configuration files and shows a difference.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()
    _, ext = os.path.splitext(args.first_file)

    return generate_diff(args.first_file, args.second_file, ext[1:])


def get_plain_children(tree, depth=1):
    result = {}
    for key in tree:
        result[key] = {}
        result[key]['status'] = 'unmodified'
        if type(tree[key]) == dict:
            children = get_plain_children(tree[key], depth + 1)
            result[key]['children'] = children
        else:
            result[key]['children'] = None
            result[key]['value'] = tree[key]
        result[key]['depth'] = depth
    return result


def gen_ast(file1, file2, depth=1):
    keys = set(file1.keys()).union(set(file2.keys()))

    diff = {}

    for key in keys:
        diff[key] = {}
        if key in file1 and key in file2:
            if type(file1[key]) == dict and type(file2[key]) == dict:
                diff[key]['children'] = []
                diff[key]['status'] = 'unmodified'
                nested_diff = gen_ast(file1[key], file2[key], depth + 1)
                diff[key]['children'] = nested_diff

            elif file1[key] == file2[key]:
                diff[key]['status'] = 'unmodified'
                diff[key]['value'] = format_value(file1[key])
                diff[key]['children'] = None
            else:
                diff[key]['status'] = 'modified'
                if type(file1[key]) == dict:
                    nested_diff = get_plain_children(
                        file1[key], depth + 1)
                    diff[key]['value'] = nested_diff
                    diff[key]['new_value'] = format_value(file2[key])
                elif type(file2[key]) == dict:
                    nested_diff = get_plain_children(
                        file2[key], depth + 1)
                    diff[key]['value'] = format_value(file1[key])
                    diff[key]['new_value'] = nested_diff
                else:
                    diff[key]['value'] = format_value(file1[key])
                    diff[key]['new_value'] = format_value(file2[key])

                diff[key]['children'] = None

        elif key in file1 and key not in file2:
            diff[key]['status'] = 'deleted'
            if type(file1[key]) == dict:
                nested_diff = get_plain_children(file1[key], depth + 1)
                diff[key]['children'] = nested_diff
            else:
                diff[key]['value'] = format_value(file1[key])
                diff[key]['children'] = None

        elif key not in file1 and key in file2:
            diff[key]['status'] = 'added'
            if type(file2[key]) == dict:
                nested_diff = get_plain_children(file2[key], depth + 1)
                diff[key]['children'] = nested_diff
            else:
                diff[key]['value'] = format_value(file2[key])
                diff[key]['children'] = None
        diff[key]['depth'] = depth

    return diff


def generate_diff(filepath1, filepath2, ext) -> str:
    parse = get_parser(ext)

    with open(filepath1) as f1:
        file1 = parse(f1)
    with open(filepath2) as f2:
        file2 = parse(f2)

    ast = gen_ast(file1, file2)

    diff = show_diff(ast)

    return diff


def format_value(value):
    if type(value) == str:
        return value
    if type(value) == dict:
        return json.dumps(value, indent=4)
    return json.dumps(value)
