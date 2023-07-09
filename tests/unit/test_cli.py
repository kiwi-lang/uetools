from uetools.core.cli import args, main


def test_cli():
    # Show all the commands
    assert main(args("--help")) == 0

    # Show all the editor related commands
    assert main(args("editor", "--help")) == 0

    # Show the help for a command in particular
    assert main(args("editor", "editor", "--help")) == 0
