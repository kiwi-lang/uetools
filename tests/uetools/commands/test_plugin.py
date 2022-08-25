import subprocess

import pytest

from uetools.cli import args, main
from uetools.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_plugin(project, project_name, tmp_path):

    main(args("build", "--target", f"{project_name}Editor", "--mode", "Development"))

    main(
        args(
            "plugin",
            project,
            "Plugins/ExamplePlugin/ExamplePlugin.uplugin",
            "--output",
            "E:/Trash",
            "--platforms",
            "Win64",
        )
    )

    print(subprocess.run(["ls"], cwd=project))
