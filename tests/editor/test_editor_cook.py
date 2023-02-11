import pytest

from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_editor_cook(project, project_name):
    main(args("editor", "cook", project_name, "--build", "Development"))