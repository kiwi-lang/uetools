import os

from uetools.core.cli import args, main


def test_install(project, project_name):
    main(args("plugin", "new", project_name, "NewPlugin"))
    p = os.path.join(project, "Plugins", "NewPlugin")
    assert os.path.exists(p)
    assert os.path.exists(os.path.join(p, "NewPlugin.uplugin"))
