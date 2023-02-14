import pytest

from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_editor(project):
    # The problem is that this does not close
    # also there are too many arguments to test
    pass
