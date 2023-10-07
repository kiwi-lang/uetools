from uetools.core.command import Command, chdir, newparser
from uetools.core.conf import engine_root
from uetools.core.run import run


class Engine(Command):
    """Update the engine source code"""

    name: str = "update"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Engine)
        parser.add_argument(
            "--branch", type=str, default="5.0", help="checkout a branch"
        )
        parser.add_argument("--remote", type=str, default="origin", help="remote name")
        parser.add_argument(
            "--update",
            action="store_true",
            default=False,
            help="Pull the latest changes",
        )
        parser.add_argument(
            "--dry",
            action="store_true",
            default=False,
            help="Print the command that are going to be executed",
        )

    @staticmethod
    def execute(args):
        root = engine_root()

        if args.update:
            cmd = Engine.update(root, args.remote)
        else:
            cmd = Engine.checkout(root, args.branch, args.remote)

        with chdir(root):
            return Engine.execute_cmd(cmd, dry=args.dry)

    @staticmethod
    def update(root, remote):
        """Update current branch by pulling the latest changes"""
        from git import Repo

        engine_repo = Repo(root)
        cmd = ["git", "pull", remote, engine_repo.active_branch]
        return [cmd]

    @staticmethod
    def checkout(root, branch, remote):
        """Checkout a new branch"""
        from git import Repo

        engine_repo = Repo(root)

        if branch == engine_repo.active_branch:
            cmd = [["git", "pull", remote, branch]]

        else:
            cmd = [
                ["git", "fetch", remote, branch],
                ["git", "checkout", branch],
            ]

        return cmd

    @staticmethod
    def execute_cmd(cmds, dry=False):
        """Execute commands"""
        for cmd in cmds:
            print(" ".join(cmd))

            if not dry:
                return run(cmd, check=True).returncode

        return 0


COMMANDS = Engine
