import json
from pprint import pprint


def show_diff(diff) -> str:
    # pprint(diff)
    status_map = {
        'added': '+ ',
        'deleted': '- ',
        'unmodified': '  ',
        'modified': '  ',
    }

    spaces = 4
    offset = 2
    space = ' '

    # depth * spaces - offset

    def iter(diff):
        formatted_diff = '{\n'
        for key in sorted(diff.keys()):
            indent = space * (diff[key]['depth'] * spaces - offset)
            if diff[key]['children']:
                child_diff = iter(diff[key]['children'])
                formatted_diff += '{i}{s}{k}: {v}'.format(
                    k=key, i=indent, s=status_map[diff[key]['status']], v=child_diff)
                formatted_diff += indent + '  ' + '}\n'
            elif diff[key]['status'] == 'modified':
                if type(diff[key]['value']) == dict:
                    child_diff = iter(diff[key]['value'])
                    formatted_diff += '{i}{s}{k}: {v}'.format(
                        k=key, i=indent, s=status_map['deleted'], v=child_diff)
                    formatted_diff += indent + '  ' + '}\n'

                    formatted_diff += '{i}{s}{k}: {v}\n'.format(
                        k=key, i=indent, s=status_map['added'], v=diff[key]['new_value'])

                elif type(diff[key]['new_value']) == dict:
                    child_diff = iter(diff[key]['new_value'])
                    formatted_diff += '{i}{s}{k}: {v}\n'.format(
                        k=key, i=indent, s=status_map['deleted'], v=diff[key]['value'])
                    formatted_diff += '{i}{s}{k}: {v}\n'.format(
                        k=key, i=indent, s=status_map['added'], v=child_diff)
                    formatted_diff += indent + '  ' + '}\n'
                else:
                    formatted_diff += '{i}{s}{k}: {v}\n'.format(
                        k=key, i=indent, s=status_map['deleted'], v=diff[key]['value'])
                    formatted_diff += '{i}{s}{k}: {v}\n'.format(
                        k=key, i=indent, s=status_map['added'], v=diff[key]['new_value'])
            else:
                v = diff[key]['value']
                if type(diff[key]['value']) == dict:
                    pass
                status = status_map[diff[key]['status']]
                formatted_diff += '{i}{s}{k}: {v}\n'.format(
                    k=key, i=indent, s=status, v=v)
        return formatted_diff
    res = iter(diff)

    res += '}'
    # print(formatted_diff)
    return res
