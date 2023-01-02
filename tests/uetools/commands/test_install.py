import json
import subprocess

import pytest

from uetools.core import args, main
from uetools.core.conf import find_project, ready

skipif = pytest.mark.skipif


def get_project_conf(name):
    project = find_project(name)

    with open(project, encoding="utf-8") as project_file:
        project_conf = json.load(project_file)

    return project_conf


@skipif(not ready(), reason="Unreal engine is not installed")
def test_install(project, project_name):
    # Regenerate the project files
    main(
        args(
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

    main(args("disable", project_name, "ExamplePlugin2"))

    for plugin in get_project_conf(project_name)["Plugins"]:
        if plugin["Name"] == "ExamplePlugin2":
            assert plugin["Enabled"] is False
            break
    else:
        assert False, "Plugin not found or it was not disabled"


@skipif(not ready(), reason="Unreal engine is not installed")
def test_install_submodule(project, project_name):
    # Regenerate the project files
    main(
        args(
            "install",
            project_name,
            "ExamplePlugin2",
            "https://github.com/kiwi-lang/ExamplePlugin",
            "--submodule",
            "--enable",
            "--force",
        )
    )

    output = subprocess.check_output(
        "git config --file .gitmodules --name-only --get-regexp path".split(" "),
        text=True,
        cwd=project,
    )
    assert output.strip() == "submodule.Plugins/ExamplePlugin2.path"
