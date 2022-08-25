import os

import pytest

from uetools.cli import args, main
from uetools.commands.local import LocalEditor
from uetools.conf import ready

skipif = pytest.mark.skipif


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
            "local",
            "--bootstrap",
            "--project",
            project_name,
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
            "uat-local",
            "--project",
            project_name,
            "--IncludePlugins",
            "--ParallelGather",
            "--LocalizationSteps",
            "Gather",
            "--LocalizationProjectNames",
            project_name,
        )
    )
