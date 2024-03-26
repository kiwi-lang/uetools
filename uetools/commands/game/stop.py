# https://docs.unrealengine.com/5.0/en-US/world-partition-in-unreal-engine/


from dataclasses import dataclass

from argklass.command import Command

from uetools.core.conf import editor_cmd
from uetools.core.run import popen_with_format
from uetools.core.util import command_builder
from uetools.format.base import Formatter


class Stop(Command):
    """Find a running UnrealEngine server and stops it"""

    name: str = "stop"

    # fmt: off
    @dataclass
    class Arguments:
        """Convert a UE4 map using world partition"""
    # fmt: on

    @staticmethod
    def execute(args):
        cmd = [editor_cmd()] + command_builder(args)
        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = Stop
