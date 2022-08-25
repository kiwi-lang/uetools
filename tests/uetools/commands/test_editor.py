import pytest

from uetools.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_editor(project):
    # The problem is that this does not close
    # also there are too many arguments to test
    pass
