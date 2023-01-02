import os

import pytest

from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_vscode(project, project_name):

    assert os.path.exists(os.path.join(project, ".vscode")) is False

    main(args("vscode", project_name, "--yes"))

    assert os.path.exists(os.path.join(project, ".vscode")) is True
