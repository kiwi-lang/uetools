import pytest

from uetools.core.cli import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_editor_cook(project, project_name):
    main(args("editor", "cook", "--project", project_name, "--build", "Development"))
