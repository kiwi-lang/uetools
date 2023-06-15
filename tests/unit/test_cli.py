import pytest

from uetools.core.cli import args, main


def test_cli():
    with pytest.raises(SystemExit) as err:
        # Show all the commands
        main(args("--help"))

        # Show all the editor related commands
        main(args("editor", "--help"))

        # Show the help for a command in particular
        main(args("editor", "editor", "--help"))

    assert err.value.code == 0
