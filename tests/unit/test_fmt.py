import pytest

from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_fmt(project):
    # Not tested, but the Formatter is tested by itself
    pass
