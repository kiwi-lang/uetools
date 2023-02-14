import json
import subprocess

import pytest

from uetools.core import args, main
from uetools.core.conf import find_project, is_ci

skipif = pytest.mark.skipif


def get_project_conf(name):
    project = find_project(name)

    with open(project, encoding="utf-8") as project_file:
        project_conf = json.load(project_file)

    return project_conf


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_install(project, project_name):
    # Regenerate the project files
    main(
        args(
            "plugin",
            "install",
            project_name,
            "ExamplePlugin2",
            "https://github.com/kiwi-lang/ExamplePlugin",
            "--enable",
        )
    )

    for plugin in get_project_conf(project_name)["Plugins"]:
        if plugin["Name"] == "ExamplePlugin2":
            assert plugin["Enabled"] is True
            break
    else:
        assert False, "Plugin not found"

    main(args("plugin", "disable", project_name, "ExamplePlugin2"))

    for plugin in get_project_conf(project_name)["Plugins"]:
        if plugin["Name"] == "ExamplePlugin2":
            assert plugin["Enabled"] is False
            break
    else:
        assert False, "Plugin not found or it was not disabled"


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_install_submodule(project, project_name, capsys):
    # Regenerate the project files
    with capsys.disabled():
        main(
            args(
                "plugin",
                "install",
                project_name,
                "ExamplePlugin2",
                "https://github.com/kiwi-lang/ExamplePlugin",
                "--submodule",
                "--enable",
                "--force",
            )
        )

    main(args("plugin", "list", project_name))
    capture = capsys.readouterr().out.splitlines()

    # Plugins:
    #   - ExamplePlugin
    #   - ExamplePlugin2
    assert len(capture) == 3

    output = subprocess.check_output(
        "git config --file .gitmodules --name-only --get-regexp path".split(" "),
        text=True,
        cwd=project,
    )
    assert output.strip() == "submodule.Plugins/ExamplePlugin2.path"
