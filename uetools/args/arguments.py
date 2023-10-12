"""Simplified SimpleParsing because it was not simple"""
from __future__ import annotations

import argparse
from collections.abc import Sequence
import dataclasses
import inspect
import enum
import re
import typing
from dataclasses import MISSING, fields, is_dataclass
from typing import Any, get_type_hints

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


def _get_type_hint(hint, value):
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


def is_optional(type_hint, value):
    try:
        return type_hint.__origin__ is typing.Optional or (
            type_hint.__origin__ is typing.Union
            and len(type_hint.__args__) == 2
            and type_hint.__args__[1] is type(None)
        )
    except:
        return False


def is_list(type_hint, value):
    try:
        return type_hint.__origin__ is typing.List
    except:
        return False


def is_enum(type_hint, value):
    try:
        return issubclass(type_hint, enum.Enum)
    except:
        return False


def is_tuple(type_hint, value):
    try:
        if type(value) == tuple:
            return len(value)
    except TypeError:
        pass
    return 0


def leaf_type(type_hint):
    try:
        return type_hint.__args__[0]
    except:
        return type_hint


def to_enum(enum_type):
    elems = list(enum_type)

    elem = elems[0]
    name_t = type(elem.name)

    def cvt(value):
        try:
            return enum_type[name_t(value)]
        except:
            pass

        try:
            return elems[int(value)]
        except:
            pass

        for elem in elems:
            if elem.name == value:
                return elem

            if elem.value == value:
                return elem

    return cvt


def tuple_action(ftype):
    def _(*args, **kwargs):
        return _TupleStoreAction(*args, ttype=ftype, **kwargs)

    return _


class _TupleStoreAction(argparse._StoreAction):
    def __init__(self, *args, ttype=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ttype = ttype

    def __call__(self, parser, namespace, values, option_string=None):
        elems = []
        if isinstance(values, str):
            values = values.split(",")

        if isinstance(values[0], str) and len(values) == 1 and "," in values[0]:
            values = values[0].split(",")

        for value_t, value in zip(self.ttype.__args__, values):
            elems.append(value_t(value))

        setattr(namespace, self.dest, tuple(elems))


def deduce_add_arguments(field, docstring):
    ftype = _get_type_hint(field.type, field.default)
    required = True
    action = None
    nargs = None

    if is_optional(ftype, field.default):
        nargs = "?"
        ftype = leaf_type(ftype)
        required = False

    if is_list(ftype, field.default):
        nargs = "+"
        ftype = leaf_type(ftype)

    if is_tuple(ftype, field.default):
        nargs = "*"

        def ftype(x):
            return x

        action = tuple_action(field.type)

    if is_enum(ftype, field.default):
        ftype = to_enum(field.type)

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
        type=ftype,
        choices=choices,
        help=docstring,
        metavar=None,
        action=action,
    )

    return positional, required, kwargs


def _add_argument(group: argparse._ArgumentGroup, field, docstring) -> argparse.Action:
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


def _group(dataclass, title=None, dest=None):
    if dest:
        return dest

    if title:
        return title

    return dataclass.__name__


def add_arguments(
    parser: argparse.ArgumentParser, dataclass, title=None, create_group=True, dest=None
):
    """Traverse the dataclass hierarchy and build a parser tree"""
    source, parser.description, start = find_dataclass_docstring(dataclass)

    group = parser
    subparser = None
    if create_group:
        group = parser.add_argument_group(
            title=title or dataclass.__name__,
            description=dataclass.__doc__ or "",
        )
        setattr(group, "_dataclass", dataclass)
        setattr(group, "_dest", dest)

    for field in fields(dataclass):
        meta = dict(field.metadata)
        special_argument = meta.pop("type", None)
        docstring, start = find_docstring(field, source, start)

        if is_dataclass(field.type):
            add_arguments(group, field.type, dest=field.name, create_group=create_group)
            continue

        if special_argument == "group":
            meta.setdefault("title", field.name)
            meta.setdefault("description", docstring)

            group = group.add_argument_group(**meta)

            add_arguments(group, field.type, create_group=False)
            continue

        if special_argument == "subparser":
            meta.setdefault("title", field.name)
            meta.setdefault("description", docstring)
            meta.setdefault("dest", field.name)

            if subparser is None:
                subparser = group.add_subparsers(**meta)
            continue

        if special_argument == "parser":
            meta.setdefault("name", field.name)
            meta.setdefault("description", docstring)

            group = subparser.add_parser(**meta)
            add_arguments(group, field.type, create_group=False)
            continue

        if special_argument == "argument":
            _, _, deduced = deduce_add_arguments(field, docstring)

            for k, v in deduced.items():
                meta.setdefault(k, v)

            group.add_argument(**meta)
            continue

        if field.type == "bool" or field.type is bool:
            _add_flag(group, field, docstring)
        else:
            _add_argument(group, field, docstring)

    return group


class ArgumentParser(argparse.ArgumentParser):
    def __init__(
        self,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None,
        epilog: str | None = None,
        parents: Sequence[ArgumentParser] = [],
        formatter_class: argparse._FormatterClass = argparse.HelpFormatter,
        prefix_chars: str = "-",
        fromfile_prefix_chars: str | None = None,
        argument_default: Any = None,
        conflict_handler: str = "error",
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
        group_by_parser: bool = False,
        group_by_dataclass: bool = False,
        dataclass: type = argparse.Namespace,
    ) -> None:
        super().__init__(
            prog,
            usage,
            description,
            epilog,
            parents,
            formatter_class,
            prefix_chars,
            fromfile_prefix_chars,
            argument_default,
            conflict_handler,
            add_help,
            allow_abbrev,
            exit_on_error,
        )
        self.group_by_parser: bool = group_by_parser
        self.group_by_dataclass: bool = group_by_dataclass
        self.dataclass = dataclass

    def add_arguments(self, dataclass, dest=None, create_group=True):
        add_arguments(self, dataclass, dest=dest, create_group=create_group)

    def add_subparsers(self, *args, **kwargs):
        kwargs.setdefault("parser_class", type(self))
        return super().add_subparsers(*args, **kwargs)

    def set_defaults(self, config):
        from .config import ArgumentConfig

        transform = ArgumentConfig(config)
        transform(self)

    def save_defaults(self, config):
        from .config import ArgumentConfig

        config = dict()

        transform = ArgumentConfig(config)
        transform(self)

        return config

    def parse_args(self, *args, config=None, **kwargs):
        from .group import group_by_dataclass
        from .config import ArgumentConfig

        args = super().parse_args(*args, **kwargs)

        grouped = group_by_dataclass(
            self, args, self.group_by_parser, self.group_by_dataclass, self.dataclass
        )

        # Apply a config on top of the command line
        #   Command line takes precedence
        transform = ArgumentConfig(config, grouped)
        transform(self)

        return grouped


def argument_parser(dataclass, *args, title=None, dest=None, **kwargs):
    parser = ArgumentParser(*args, **kwargs, group_by_dataclass=True)
    parser.add_arguments(dataclass, create_group=True)
    return parser


def parse(dataclass, *args, title=None, dest=None, **kwargs):
    p = argument_parser(dataclass, *args, title=None, dest=None, **kwargs)

    gp = _group(dataclass, title=title, dest=dest)

    return getattr(p.parse_args(), gp)


def parse_known_args(dataclass, *args, title=None, dest=None, **kwargs):
    p = argument_parser(dataclass, *args, title=None, dest=None, **kwargs)

    gp = _group(dataclass, title=title, dest=dest)

    args, others = p.parse_known_args()

    return getattr(args, gp), others
