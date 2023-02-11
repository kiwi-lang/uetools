import uetools.commands.editor
from uetools.core.command import ParentCommand


class Editor(ParentCommand):
    """Set of commands to launch the editors in different modes"""

    name: str = "editor"

    @staticmethod
    def module():
        return uetools.commands.editor


COMMANDS = Editor
