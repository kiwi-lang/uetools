import pytest

from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_server(project, project_name):
    # That one is also a bit tricky to test
    main(args("editor", "resavepackages", project_name))
