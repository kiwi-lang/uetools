import pytest

from uetools.core import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_uat_cook(project, project_name):
    main(args("uat", "cook", project_name))
