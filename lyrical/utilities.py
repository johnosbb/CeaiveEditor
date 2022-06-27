from pprint import pprint
from inspect import getmembers
from types import FunctionType


def isBlank(myString):
    return not (myString and myString.strip())


def isNotBlank(myString):
    return bool(myString and myString.strip())


def attributes(obj):
    disallowed_names = {
        name for name, value in getmembers(type(obj))
        if isinstance(value, FunctionType)}
    return {
        name: getattr(obj, name) for name in dir(obj)
        if name[0] != '_' and name not in disallowed_names and hasattr(obj, name)}


def print_attributes(obj):
    pprint(attributes(obj))
