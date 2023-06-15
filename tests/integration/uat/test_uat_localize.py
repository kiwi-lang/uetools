import os

import pytest

from uetools.commands.editor.localize import LocalEditor
from uetools.core.cli import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(True, reason="Localization does not work on the example project")
@skipif(is_ci(), reason="Unreal engine is not installed")
def test_uatlocal(project, project_name):

    # UAT does not bootstrap the project so we need to create the config first
    assert (
        os.path.exists(os.path.join(project, "Config/Localization/ExampleProject.ini"))
        is False
    )
    LocalEditor.bootstrap(project_name, project_name)
    assert (
        os.path.exists(os.path.join(project, "Config/Localization/ExampleProject.ini"))
        is True
    )

    main(
        args(
            "uat",
            "localize",
            project_name,
            "--IncludePlugins",
            "--ParallelGather",
            "--LocalizationSteps",
            "Gather",
            "--LocalizationProjectNames",
            project_name,
        )
    )
