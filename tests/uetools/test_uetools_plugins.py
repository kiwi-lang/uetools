import subprocess
from contextlib import contextmanager

import pytest

from uetools.commands import discover_commands

skipif = pytest.mark.skipif


@contextmanager
def install_plugin():
    subprocess.run(
        "pip install git+https://github.com/kiwi-lang/uetools.plugins.myplugin".split(
            " "
        ),
        check=True,
    )

    yield

    subprocess.run(
        "pip uninstall uetools.plugins.myplugin --yes".split(" "), check=True
    )


@skipif(True, reason="Flaky")
def test_uetools_plugin():
    try:
        subprocess.run(
            "pip uninstall uetools.plugins.myplugin --yes".split(" "), check=True
        )
    except subprocess.CalledProcessError:
        pass

    assert "command" not in discover_commands()

    with install_plugin():
        for i in range(10):
            if "command" in discover_commands():
                break

        assert "command" in discover_commands()


def test_ml_plugin_was_installed():
    assert "ml" in discover_commands()
