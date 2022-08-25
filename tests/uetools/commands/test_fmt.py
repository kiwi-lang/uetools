import pytest

from uetools.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_fmt(project):
    # Not tested, but the Formatter is tested by itself
    pass
