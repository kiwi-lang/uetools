from uetools.args.command import ParentCommand


class Editor(ParentCommand):
    """Set of commands to launch the editors in different modes"""

    name: str = "editor"

    @staticmethod
    def module():
        import uetools.commands.editor

        return uetools.commands.editor


COMMANDS = Editor
