import os

from git import Repo

from uetools.command import Command, chdir, newparser
from uetools.conf import load_conf
from uetools.run import run


class Engine(Command):
    """Update the engine source code"""

    name: str = "engine"

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
        engine_root = os.path.abspath(
            os.path.join(load_conf().get("engine_path"), "..")
        )

        if args.update:
            cmd = Engine.update(engine_root, args.remote)
        else:
            cmd = Engine.checkout(engine_root, args.branch, args.remote)

        with chdir(engine_root):
            Engine.execute_cmd(cmd, dry=args.dry)

    @staticmethod
    def update(engine_root, remote):
        """Update current branch by pulling the latest changes"""
        engine_repo = Repo(engine_root)
        cmd = ["git", "pull", remote, engine_repo.active_branch]
        return [cmd]

    @staticmethod
    def checkout(engine_root, branch, remote):
        """Checkout a new branch"""
        engine_repo = Repo(engine_root)

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
                run(cmd, check=True)


COMMANDS = Engine
