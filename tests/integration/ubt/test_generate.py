import os

import pytest

from uetools.core.cli import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_generate(project, project_name, project_root):
    assert not os.path.exists(os.path.join(project, f"{project_name}.sln"))

    # Regenerate the project files
    main(args("ubt", "regenerate", project_name, "--projectfileformat", "VisualStudio2022"))

    assert os.path.exists(os.path.join(project, f"{project_name}.sln"))
