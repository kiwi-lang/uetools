from collections import defaultdict
from distutils.command.clean import clean
import os
import re
import json

param_dump = os.path.join(
    os.path.dirname(__file__),
     'params.txt'
)

FLAG = re.compile(r'(?P<path>[A-Za-z\/]*)\.cpp:(?P<line>[0-9]*):(\s*)(.*)TEXT\(\s*"\s*(?P<arg>-?[._A-Za-z0-9]*(=[;%a-z]*)?)\s*".*\)')



def remove(list, ignore):
    return [x for x in list if x not in ignore]


def keep(a, b):
    return [x for x in a if x in b]


class ParameterParser:
    def __init__(self) -> None:
        self.args = defaultdict(set)
        self.params = defaultdict(list)
        self.unhandled = []
        self.group_override = [
            'AutomationController',
            'DerivedDataCache',
            'VulkanRHI',
            'WebBrowser',
            'RHI',
        ]

    def show_unhandled(self):
        for line in self.unhandled:
            print(line, end='')

        print()
        print('Unhandled: ', len(self.unhandled))

    def first_pass(self, raw, path, line, arg):

        ignore = set(['Source', 'Private'])

        for override in self.group_override:
            if override in path:
                frags = [override]
                break
        else:
            frags = remove(path.split('/'), ignore)

        clean_name = arg.replace('-', '').replace('=', '')

        if clean_name:
            if clean_name in self.args:
                self.args[clean_name] = keep(self.args[clean_name], frags)
            else:
                self.args[clean_name] = frags
        elif arg not in ('', "="):
            self.unhandled.append(raw)

    def second_pass(self):
        for arg, group in self.args.items():
            self.params['_'.join(group)].append(arg)

def parse_params():
    params = ParameterParser()

    with open(param_dump, 'r') as file:
        for line in file:
            result = FLAG.search(line)

            if result:
                data = result.groupdict()
                params.first_pass(line, **data)
            else:
                params.unhandled.append(line)

    params.second_pass()

    with open(os.path.join(os.path.dirname(__file__), 'params.json'), 'w') as file:
        json.dump(params.params, file, indent=2)

    print('Unhandled')
    print('-' * 80)
    params.show_unhandled()

parse_params()
