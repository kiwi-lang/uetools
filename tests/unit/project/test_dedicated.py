import os

from uetools.core import args, main


def test_unit_dedicated(project, project_name):

    assert (
        os.path.exists(os.path.join(project, "Source/ExampleProjectServer.Target.cs"))
        is False
    )

    # Add a new dedicated server target
    main(args("project", "dedicated", project_name))

    assert (
        os.path.exists(os.path.join(project, "Source/ExampleProjectServer.Target.cs"))
        is True
    )
    assert os.path.exists(os.path.join(project, "ExampleProject.sln")) is False
