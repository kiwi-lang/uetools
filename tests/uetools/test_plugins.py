import subprocess

from uetools.commands import discover_commands


def test_uetools_plugin():

    assert "command" not in discover_commands()

    subprocess.run(
        "pip install git+https://github.com/kiwi-lang/uetools.plugins.myplugin".split(
            " "
        ),
        check=True,
    )

    assert "command" in discover_commands()

    subprocess.run("pip unistall uetools.plugins.myplugin".split(" "), check=True)
