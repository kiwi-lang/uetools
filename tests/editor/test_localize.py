import os

import pytest

from uetools.commands.editor.localize import LocalEditor
from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(True, reason="Localization does not work on the example project")
@skipif(not ready(), reason="Unreal engine is not installed")
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


@skipif(True, reason="Localization does not work on the example project")
@skipif(not ready(), reason="Unreal engine is not installed")
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
