import pytest

from uetools.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_server(project):
    # That one is also a bit tricky to test
    pass
