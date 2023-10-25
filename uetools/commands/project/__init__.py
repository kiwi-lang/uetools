from argklass.command import ParentCommand

import uetools.commands.project


class Project(ParentCommand):
    """Set of commands to manage an UnrealProject"""

    name: str = "project"

    @staticmethod
    def module():
        return uetools.commands.project


COMMANDS = Project
