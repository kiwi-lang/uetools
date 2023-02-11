import pytest

from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_engine(project):
    # I don't really want to test this with my install
    pass
