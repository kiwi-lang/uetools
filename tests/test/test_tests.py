import pytest

from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_tests(project):
    # There are no test to check in the example project
    pass
