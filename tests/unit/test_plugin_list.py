import pytest

from uetools.core.cli import args, main

skipif = pytest.mark.skipif

@skipif(True, reason="need a real project to check its plugin")
def test_list(capsys):
    main(args("plugin", "list", "--project", "projectname"))
    capture = capsys.readouterr().out.splitlines()
    print(capture)

    assert capture[0].startswith("No Plugins found inside")
