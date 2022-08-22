from argparse import ArgumentParser

from gamekit.commands import commands


def parse_args():
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')

    for _, command in commands.items():
        command.arguments(subparsers)

    return parser.parse_args()

def main():
    args = parse_args()

    cmd_name = args.command
    command = commands.get(cmd_name)

    if command is None:
        print(f'Action `{cmd_name}` not implemented')
        return

    command.execute(args)


if __name__ == '__main__':
    main()
