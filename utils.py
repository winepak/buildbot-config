#!/usr/bin/env python2

import sys

def application_id_is_valid(possible_id):
    return len(possible_id.split('.')) >= 3

def buildname_to_id(buildname):
    if "//" in buildname:
        return buildname.split("//", 1)[0]

    return buildname.split("/", 1)[0]

def strip_dot_git(module):
    if module.endswith(".git"):
        module = module[:-4]
    
    return module

PY2 = sys.version_info[0] == 2
def asciiize(str):
    if PY2 and isinstance (str, unicode):
        return str.encode('ascii', 'ignore')
    return str

# This makes things work with python2
def json_to_ascii(value):
    if isinstance(value, dict):
        d = {}
        for key, dict_value in value.items():
            d[json_to_ascii(key)] = json_to_ascii(dict_value)
        return d
    elif isinstance (value, list):
        l = []
        for list_value in value:
            l.append(json_to_ascii(list_value))
        return l
    else:
        return asciiize(value)
