import os

import pytest

import uetools.commands.build as build
from uetools.cli import args, main
from uetools.conf import ready
from uetools.testing import git_status

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_build(project, project_name):

    # Repo is clean
    assert os.path.exists(os.path.join(project, "Binaries")) is False
    assert os.path.exists(os.path.join(project, "Intermediate")) is False
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Binaries")) is False
    )
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Intermediate/"))
        is False
    )

    main(args("build", "--target", f"{project_name}Editor", "--mode", "Development"))

    # Repo has results
    assert os.path.exists(os.path.join(project, "Binaries")) is True
    assert os.path.exists(os.path.join(project, "Intermediate")) is True
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Binaries")) is True
    )
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Intermediate/"))
        is True
    )


# This takes a bit too long to tests specially because it always start from scratch
@skipif(not ready(), reason="Unreal engine is not installed")
def test_multi_build(project, project_name):

    # Repo is clean
    assert os.path.exists(os.path.join(project, "Binaries")) is False
    assert os.path.exists(os.path.join(project, "Intermediate")) is False
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Binaries")) is False
    )
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Intermediate/"))
        is False
    )

    main(
        args(
            "build",
            "--target",
            project_name,
            "--mode",
            "Development",
            "--profile",
            "short-update",
        )
    )

    # Repo has results
    assert os.path.exists(os.path.join(project, "Binaries")) is True
    assert os.path.exists(os.path.join(project, "Intermediate")) is True
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Binaries")) is True
    )
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Intermediate/"))
        is True
    )
