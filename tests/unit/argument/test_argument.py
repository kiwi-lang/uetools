from argparse import ArgumentParser
from dataclasses import dataclass, field, fields
from typing import Optional


from uetools.core.arguments import group, argument, subparser, add_arguments, parser
from uetools.core.argformat import HelpAction, DumpParserAction, HelpActionException

@dataclass
class Undo:
    """Undo doc"""
    argument: bool # arg doc


@dataclass
class Do:
    """Do doc"""
    argument: bool # arg doc


@dataclass
class Redo:
    """Redo doc"""
    argument: bool # arg doc


@dataclass()
class Edit:
    """Edit doc"""
    editcmd: str = subparser()
    undo: Undo = parser(Undo)
    do: Do = parser(Do)
    redo: Redo = parser(Redo)


@dataclass
class Group:
    """
    Group help
    """
    verbose: bool # verbose doc


@dataclass
class CommandLine:
    """Command line help"""
    group: Group = group(Group) 

    cmd: str = subparser() # ignored doc
    edit: Edit = parser(Edit) # ignored


if __name__ == '__main__':

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-h", "--help", action=HelpAction, help="show this help message and exit"
    )
    parser.add_argument(
        "-d", "--d", action=DumpParserAction, help="show this help message and exit"
    )
    add_arguments(parser, CommandLine)

    try:
        args = parser.parse_args()     
        print(args)
        print(args.cmd)
    except HelpActionException:
        pass
