import pytest

from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_disable(project):
    # this is tests with install which install a plugin
    pass
