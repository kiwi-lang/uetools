import os

import pytest

from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


# @skipif(True, reason="Takes too much ram")
@skipif(not ready(), reason="Unreal engine is not installed")
def test_build(project, project_name):

    # Repo is clean
    assert os.path.exists(os.path.join(project, "Binaries")) is False

    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Binaries")) is False
    )

    main(
        args(
            "ubt",
            "build",
            f"{project_name}Editor",
            "--mode",
            "Development",
        )
    )

    # Repo has results
    assert os.path.exists(os.path.join(project, "Binaries")) is True

    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Binaries")) is True
    )


# This takes a bit too long to tests specially because it always start from scratch
# @skipif(True, reason="Takes too much ram")
@skipif(not ready(), reason="Unreal engine is not installed")
def test_multi_build(project, project_name):

    # Repo is clean
    assert os.path.exists(os.path.join(project, "Binaries")) is False
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Binaries")) is False
    )
    main(
        args(
            "ubt",
            "build",
            project_name,
            "--mode",
            "Development",
            "--profile",
            "short-update",
        )
    )

    # Repo has results
    assert os.path.exists(os.path.join(project, "Binaries")) is True
    assert (
        os.path.exists(os.path.join(project, "Plugins/ExamplePlugin/Binaries")) is True
    )
