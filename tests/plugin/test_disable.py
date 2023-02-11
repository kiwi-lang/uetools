import pytest

from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_disable(project):
    # this is tests with install which install a plugin
    pass
