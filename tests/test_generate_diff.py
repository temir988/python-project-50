# -*- coding:utf-8 -*-
from gendiff.cli import show_diff, generate_diff


def test_show_diff():
    stub_diff = {
        'a': 'added',
        'b': 'deleted',
        'c': 'modified',
        'e': 'unmodified',
    }
    with open('tests/fixtures/show_result.txt') as file:
        diff = show_diff(stub_diff)
        result = ''.join(file.readlines())
        assert diff == result


def test_generate_diff():
    fp1 = 'tests/fixtures/file1.json'
    fp2 = 'tests/fixtures/file2.json'
    diff = generate_diff(fp1, fp2, 'json')

    with open('tests/fixtures/diff_result.txt') as file:
        result = ''.join(file.readlines())
        assert diff == result


def test_yaml_format():
    fp1 = 'tests/fixtures/file1.yaml'
    fp2 = 'tests/fixtures/file2.yaml'
    diff = generate_diff(fp1, fp2, 'yaml')

    with open('tests/fixtures/diff_result.txt') as file:
        result = ''.join(file.readlines())
        assert diff == result
