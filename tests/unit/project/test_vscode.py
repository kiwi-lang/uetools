import os

import pytest

from uetools.core.cli import args, main

skipif = pytest.mark.skipif


def test_vscode(project, project_name):
    assert os.path.exists(os.path.join(project, ".vscode")) is False

    main(args("project", "vscode", "--project", project_name, "--yes"))

    assert os.path.exists(os.path.join(project, ".vscode")) is True
