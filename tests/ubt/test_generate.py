import os

import pytest

from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_generate(project, project_name, project_root):

    # Regenerate the project files
    main(
        args(
            "ubt", "regenerate", project_name, "--projectfileformat", "VisualStudio2022"
        )
    )

    assert os.path.exists(os.path.join(project, f"{project_name}.sln"))
