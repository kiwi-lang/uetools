import os

import pytest

from uetools.core import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_dedicated(project, project_name):

    assert (
        os.path.exists(os.path.join(project, "Source/ExampleProjectServer.Target.cs"))
        is False
    )

    # Add a new dedicated server target
    main(args("project", "dedicated", project_name))

    assert (
        os.path.exists(os.path.join(project, "Source/ExampleProjectServer.Target.cs"))
        is True
    )
    assert os.path.exists(os.path.join(project, "ExampleProject.sln")) is False

    # Regenerate the project files
    main(
        args(
            "ubt", "regenerate", project_name, "--projectfileformat", "VisualStudio2022"
        )
    )

    assert os.path.exists(os.path.join(project, "ExampleProject.sln")) is True
    assert (
        os.path.exists(os.path.join(project, "Binaries/Win64/ExampleProjectServer.exe"))
        is False
    )

    # New target should exist and be buildable
    # this takes a while too
    main(args("ubt", "ubt", f"{project_name}Server", "--project", project_name))

    assert (
        os.path.exists(os.path.join(project, "Binaries/Win64/ExampleProjectServer.exe"))
        is True
    )
