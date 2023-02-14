import pytest

from uetools.core import args, main

skipif = pytest.mark.skipif


def test_list(capsys):
    main(args("plugin", "list"))
    capture = capsys.readouterr().out.splitlines()
    assert capture[0].startswith("No Plugins found inside")
