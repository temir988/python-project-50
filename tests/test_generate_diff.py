# -*- coding:utf-8 -*-
from gendiff.cli import show_diff, generate_diff


def test_multi_nested_file():
    fp1 = 'tests/fixtures/orignested1.json'
    fp2 = 'tests/fixtures/orignested2.json'
    diff = generate_diff(fp1, fp2, 'json')

    with open('tests/fixtures/orignested_result.txt') as file:
        result = ''.join(file.readlines())
        assert diff == result
