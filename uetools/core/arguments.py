"""Simplified SimpleParsing because it was not simple"""
from __future__ import annotations

import argparse
import dataclasses
import inspect
import typing
from dataclasses import MISSING, fields
from typing import get_type_hints

forward_refs_to_types = {
    "tuple": typing.Tuple,
    "set": typing.Set,
    "dict": typing.Dict,
    "list": typing.List,
    "type": typing.Type,
}


def field(*args, choices=None, type=None, **kwargs):
    metadata = kwargs.pop("metadata", dict())
    if choices:
        metadata["choices"] = choices

    if type is not None:
        metadata["type"] = type

    return dataclasses.field(*args, metadata=metadata, **kwargs)


def choice(*args, default=MISSING, **kwargs):
    if default is MISSING:
        default = args[0]

    return field(default=default, choices=args, **kwargs)


def _get_type_hint(hint):
    local_ns = {
        "typing": typing,
        **vars(typing),
    }
    local_ns.update(forward_refs_to_types)

    class Temp_:
        pass

    Temp_.__annotations__ = {"a": cvt_type(hint)}
    annotations_dict = get_type_hints(Temp_, localns=local_ns)
    return annotations_dict["a"]


def cvt_type(hint):
    try:
        if "| None" in hint:
            return "Optional[" + hint.replace("| None", "") + "]"
        return hint
    except:
        return hint


def _add_flag(group, field, docstring):
    default = False
    action = "store_true"

    if field.default is True:
        default = True
        action = "store_false"

    group.add_argument(
        "--" + field.name,
        action=action,
        default=default,
        help=docstring,
    )


def is_optional(type_hint):
    try:
        return type_hint.__origin__ is typing.Optional
    except:
        return False


def is_list(type_hint):
    try:
        return type_hint.__origin__ is typing.List
    except:
        return False


def leaf_type(type_hint):
    try:
        return type_hint.__args__[0]
    except:
        return type_hint


def _add_argument(group, field, docstring):
    type = _get_type_hint(field.type)
    name = field.name
    required = True

    nargs = None
    if is_optional(type):
        nargs = "?"
        required = False

    if is_list(type):
        nargs = "+"

    # Optional + List = nargs=*
    default = MISSING
    if field.default is not MISSING:
        default = field.default
        required = False

    if field.default_factory is not MISSING:
        default = field.default_factory()

    choices = None
    if field.metadata:
        choices = field.metadata.get("choices")

    positional = False
    if default is MISSING:
        positional = True
        default = None

    kwargs = dict(
        nargs=nargs,  # nargs
        const=None,  # Const
        default=default,
        type=leaf_type(type),
        choices=choices,
        help=docstring,
        metavar=None,
    )

    if positional:
        group.add_argument(
            name,
            **kwargs,
        )
    else:
        group.add_argument(
            "--" + name,  # Option Strings
            dest=name,  # dest
            required=not positional and required,
            **kwargs,
        )


def find_docstring(field, lines, start_index):
    start = start_index
    nlines = len(lines)

    while start < nlines and field.name not in lines[start]:
        start += 1

    if start >= nlines:
        return None, start_index

    idx = lines[start].find("#")

    if idx > 0:
        return lines[start][idx + 1 :].strip(), start_index

    return None, start


def add_arguments(parser: argparse.ArgumentParser, dataclass, create_group=True):
    source = inspect.getsource(dataclass).splitlines()
    start = 0

    group = parser
    if create_group:
        group = parser.add_argument_group(
            title=dataclass.__name__,
            description=dataclass.__doc__ or "",
        )

    for field in fields(dataclass):
        docstring, start = find_docstring(field, source, start)
        # print(dataclass, field)

        if field.type == "bool" or field.type is bool:
            _add_flag(group, field, docstring)
        else:
            _add_argument(group, field, docstring)
