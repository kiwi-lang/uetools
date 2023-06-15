import os

import pytest

from uetools.core.cli import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(True, reason="Localization does not work on the example project")
@skipif(is_ci(), reason="Unreal engine is not installed")
def test_local(project, project_name):
    assert (
        os.path.exists(os.path.join(project, "Config/Localization/ExampleProject.ini"))
        is False
    )

    # Create a bootstrapped localizationt target
    # end gather text to be localized
    main(
        args(
            "editor",
            "localize",
            project_name,
            "--bootstrap",
            "--run",
            "GatherText",
            "--target",
            project_name,
        )
    )

    assert (
        os.path.exists(os.path.join(project, "Config/Localization/ExampleProject.ini"))
        is True
    )
