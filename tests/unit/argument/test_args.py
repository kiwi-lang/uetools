from dataclasses import dataclass
from typing import Tuple

from argklass.arguments import ArgumentParser

from uetools.core.cli import args


def test_groups():
    from argklass.groupargs import GroupArguments

    from uetools.commands.editor.editor import Arguments
    from uetools.core.cli import build_parser, discover_commands

    commands = discover_commands()

    parser = build_parser(commands)

    out = parser.parse_args(args("editor", "editor", "--project", "FakeProject"))

    gp = GroupArguments(out)
    gp.group_by_dataclass = True
    gp.group_by_parser = False

    data = gp.convert(parser)

    assert type(data.Arguments) == Arguments


def test_enum():
    import enum

    class Color(enum.Enum):
        RED = "RED"
        ORANGE = "ORANGE"
        BLUE = "BLUE"

    @dataclass
    class Args:
        color: Color = Color.BLUE

    p = ArgumentParser()
    p.add_arguments(Args)

    args1 = p.parse_args(args("--color", "BLUE"))
    args2 = p.parse_args(args("--color", "0"))

    assert type(args1.color) is Color
    assert type(args2.color) is Color


def test_tuple():
    @dataclass
    class Args:
        v: Tuple[float, float] = (2, 3)

    p = ArgumentParser()
    p.add_arguments(Args)

    args1 = p.parse_args(args("--v", "1,1"))
    args2 = p.parse_args(args("--v", "1", "1"))

    assert args1.v == (1, 1)
    assert args2.v == (1, 1)


def test_config():
    from argklass.config import apply_config, apply_defaults, save_as_config, save_defaults

    from uetools.core.cli import build_parser, discover_commands

    commands = discover_commands()

    parser = build_parser(commands)

    save_defaults(parser, "config.hjson")

    apply_defaults(parser, "config.hjson")

    out = parser.parse_args(args("editor", "editor", "--project", "FakeProject"))

    print(out)

    save_as_config(parser, out, "dump.hjson")

    apply_config(parser, out, "dump.hjson")

    print(out)
