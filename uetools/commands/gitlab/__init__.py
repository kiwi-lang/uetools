from uetools.args.command import ParentCommand


class Gitlab(ParentCommand):
    name: str = "gitlab"

    @staticmethod
    def module():
        import uetools.commands.gitlab
        return uetools.commands.gitlab


COMMANDS = Gitlab
