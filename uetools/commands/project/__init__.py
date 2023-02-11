import uetools.commands.project
from uetools.core.command import ParentCommand


class Project(ParentCommand):
    """Set of commands to manage an UnrealProject"""

    name: str = "project"

    @staticmethod
    def module():
        return uetools.commands.project


COMMANDS = Project
