import pytest

from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_tests(project, project_name):
    # There are no test to check in the example project
    # main(args("test", "run", project_name))
    pass
