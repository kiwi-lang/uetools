def test_groups():
    from uetools.core.cli import discover_commands, build_parser
    from uetools.args.group import GroupArguments

    commands = discover_commands()

    parser = build_parser(commands)

    args = parser.parse_args()

    gp = GroupArguments(args)

    data = gp.convert(parser)

    print(data)


def test_types():
    from uetools.args.arguments import parse
    from dataclasses import dataclass
    from typing import Tuple
    import enum

    class Color(enum.Enum):
        RED = "RED"
        ORANGE = "ORANGE"
        BLUE = "BLUE"

    # print(data)
    @dataclass
    class Options:
        """Help string for this group of command-line arguments"""

        log_dir: str  # Help string for a required str argument
        learning_rate: float = 1e-4  # Help string for a float argument
        v: Tuple[float, float] = (1, 1)  # I am here
        color: Color = Color.BLUE

    print(parse(Options))


def test_config():
    from uetools.core.cli import discover_commands, build_parser
    from uetools.args.arguments import (
        apply_config,
        save_as_config,
        apply_defaults,
        save_defaults,
    )

    commands = discover_commands()

    parser = build_parser(commands)

    save_defaults(parser, "config.hjson")

    apply_defaults(parser, "config.hjson")

    args = parser.parse_args()

    print(args)

    save_as_config(parser, args, "dump.hjson")

    apply_config(parser, args, "dump.hjson")

    print(args)
