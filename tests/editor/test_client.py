import pytest

from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_client(project):
    # the problem is the client just "opens"
    pass
