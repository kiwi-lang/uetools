import pytest

from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_uat_cook(project, project_name):

    main(args("cook", "--project", project_name, "--build", "Development"))

    main(args("uat-cook", "--build", "--project", project_name))

    # TODO check what files the cooking should generate
