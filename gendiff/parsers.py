import json

import yaml


def get_parser(ext: str):
    parsers = {
        'json': json.load,
        'yaml': yaml.safe_load,
        'yml': yaml.safe_load,
    }
    return parsers[ext]
