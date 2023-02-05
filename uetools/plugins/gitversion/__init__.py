import os
import re
import subprocess

from uetools.core.command import Command, newparser


class GitVersion(Command):
    """Update a file with git version info

    Replaces ``{%%<NAMESPACE>_TAG%%}``, ``{%%<NAMESPACE>_HASH%%}``, ``{%%<NAMESPACE>_DATE%%}`` inside a given file
    with the latest values

    Example
    -------

    .. code-block::

       uecli gitversion --namespace GKFOGOFWAR --file Source/GKFogOfWar/GKFogOfWar.Build.cs
    """

    name: str = "gitversion"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, GitVersion)
        parser.add_argument("--file", type=str, help="file to update")
        parser.add_argument("--namespace", type=str, help="file to update")

    @staticmethod
    def execute(args):
        directory = os.path.dirname(args.file)

        def execcmd(cmd, cwd):
            return (
                subprocess.check_output(cmd.split(" "), cwd=cwd).decode("utf-8").strip()
            )

        commit = execcmd("git --no-optional-locks rev-parse HEAD", directory)
        tag = execcmd("git --no-optional-locks describe --tags --abbrev=0", directory)
        date = execcmd(
            "git --no-optional-locks show -s --format=%ci " + commit, directory
        )

        replacements = [
            (f"{args.namespace}_TAG", tag),
            (f"{args.namespace}_HASH", commit),
            (f"{args.namespace}_DATE", date),
        ]

        with open(args.file, encoding="utf-8") as original_file:
            data = original_file.read()

        for k, v in replacements:
            pattern = "string " + k + ' = ".*";'
            replacement = f'string {k} = "{v}";'

            data, count = re.subn(pattern, replacement, data)

            if count == 1:
                print(f'Set {k} = "{v}"')
            else:
                print(f"Key {k} not found")

        with open(args.file + ".new", "w", encoding="utf-8") as new_file:
            new_file.write(data)

        os.replace(args.file + ".new", args.file)

        return 0


COMMANDS = GitVersion
