import os

import pytest

from uetools.core import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_vscode(project, project_name):

    assert os.path.exists(os.path.join(project, ".vscode")) is False

    main(args("project", "vscode", project_name, "--yes"))

    assert os.path.exists(os.path.join(project, ".vscode")) is True
