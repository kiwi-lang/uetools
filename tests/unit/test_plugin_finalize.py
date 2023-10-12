import os

from uetools.core.cli import args, main


def test_plugin_finalize(project, project_name):

    p1 = os.path.join(project, "Plugins", "ExamplePlugin", "ExamplePlugin.uplugin")
    p2 = os.path.join(project, "Plugins", "ExamplePlugin2", "ExamplePlugin2.uplugin")

    # Add a new plugin
    main(
        args(
            "plugin",
            "install",
            "--project",
            os.path.join(project, project_name + ".uproject"),
            "ExamplePlugin2",
            "https://github.com/kiwi-lang/ExamplePlugin",
        )
    )

    rc = main(args("plugin", "finalize", p1, p2))

    assert rc == 1
