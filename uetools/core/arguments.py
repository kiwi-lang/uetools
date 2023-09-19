"""Simplified SimpleParsing because it was not simple"""
from __future__ import annotations

import argparse
import dataclasses
import inspect
import re
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


class Subparser:
    pass


def argument(default, **kwargs):
    # argparse.ArgumentParser().add_argument
    kwargs["type"] = "argument"
    return dataclasses.field(default=default, metadata=kwargs)


def group(default, **kwargs):
    # argparse.ArgumentParser().add_argument_group()
    kwargs["type"] = "group"
    return dataclasses.field(default_factory=default, metadata=kwargs)


def subparser(**kwargs):
    # argparse.ArgumentParser().add_subparsers()
    kwargs["type"] = "subparser"
    return dataclasses.field(default=None, metadata=kwargs)


def parser(default, **kwargs):
    # argparse.ArgumentParser().add_subparsers().add_parser()
    kwargs["type"] = "parser"
    return dataclasses.field(default_factory=default, metadata=kwargs)


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


def deduce_add_arguments(field, docstring):
    type = _get_type_hint(field.type)
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

    return positional, required, kwargs


def _add_argument(group, field, docstring):
    positional, required, kwargs = deduce_add_arguments(field, docstring)

    name = field.name

    if positional:
        return group.add_argument(
            name,
            **kwargs,
        )
    else:
        return group.add_argument(
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


docstring_oneline = re.compile(r'(\s*)"""(.*)"""')
docstring_start = re.compile(r'(\s*)"""(.*)')
docstring_end = re.compile(r'(.*)"""')


def find_dataclass_docstring(dataclass):
    source = inspect.getsource(dataclass).splitlines()
    docstring_lines = []

    started = False
    recognized = 0
    for i, line in enumerate(source):
        if "@dataclass" in line:
            recognized += 1
            continue

        if "class " in line:
            recognized += 1
            continue

        if recognized == 2 and not started and docstring_oneline.match(line):
            docstring_lines.append(line.strip()[3:-3])
            break

        if recognized == 2 and not started and docstring_start.match(line):
            started = True
            docstring_lines.append(line.strip()[3:])
            continue

        if started and docstring_end.match(line):
            docstring_lines.append(line.strip()[:-3])
            started = False
            break

        if started:
            docstring_lines.append(line.strip())
    else:
        i = 0

    return source, "\n".join(docstring_lines).strip(), i


def add_arguments(
    parser: argparse.ArgumentParser, dataclass, create_group=True, mapper=None
):
    """Traverse the dataclass hierarchy and build a parser tree"""
    source, parser.description, start = find_dataclass_docstring(dataclass)

    group = parser
    subparser = None
    if create_group:
        group = parser.add_argument_group(
            title=dataclass.__name__,
            description=dataclass.__doc__ or "",
        )

    if mapper is None:
        mapper = dict()

    def map(a, b):
        # assert a not in mapper
        # mapper[a] = b
        # assert b not in mapper
        # mapper[b] = a
        pass

    map(parser, dataclass)

    for field in fields(dataclass):
        meta = dict(field.metadata)
        special_argument = meta.pop("type", None)
        docstring, start = find_docstring(field, source, start)

        if special_argument == "group":
            meta.setdefault("title", field.name)
            meta.setdefault("description", docstring)

            group = parser.add_argument_group(**meta)
            map(group, field)

            add_arguments(group, field.type, create_group=False)
            continue

        if special_argument == "subparser":
            meta.setdefault("title", field.name)
            meta.setdefault("description", docstring)
            meta.setdefault("dest", field.name)

            if subparser is None:
                subparser = parser.add_subparsers(**meta)
                map(subparser, field)
            continue

        if special_argument == "parser":
            meta.setdefault("name", field.name)
            meta.setdefault("description", docstring)

            parser = subparser.add_parser(**meta)
            mapper[field] = parser
            add_arguments(parser, field.type, create_group=False)
            continue

        if special_argument == "argument":
            _, _, deduced = deduce_add_arguments(field, docstring)

            for k, v in deduced.items():
                meta.setdefault(k, v)

            map(parser.add_argument(**meta), field)
            continue

        if field.type == "bool" or field.type is bool:
            map(_add_flag(group, field, docstring), field)
        else:
            map(_add_argument(group, field, docstring), field)
