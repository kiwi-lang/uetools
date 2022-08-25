import pytest

from uetools.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_uat(project):
    pass
