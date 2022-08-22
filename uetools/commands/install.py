from uetools.conf import Command


class Install(Command):
    """Install a plugin to an unreal project.

    Examples
    --------

    .. code-block::

       # This will install the plugin inside RTSGame/Plugins/
       #  it will download the repository on put it inside the RTSGame/Plugins/ folder
       uecli install RTSGame https://github.com/Phyronnaz/VoxelPlugin

       # This will install the plugin inside RTSGame/Plugins/
       # it will execute the following command:
       #    - git submodule add https://github.com/Phyronnaz/VoxelPlugin Plugins/VoxelPlugin
       #
       uecli install RTSGame https://github.com/Phyronnaz/VoxelPlugin --destination Plugins --submodule

    """

    name: str = "install"

    @staticmethod
    def arguments(subparsers):
        install = subparsers.add_parser(
            Install.name, help="Install a Plugin in a unreal project"
        )
        install.add_argument("name", type=str, help="Project name")
        install.add_argument("url", type=str, help="repository url of the plugin")
        install.add_argument(
            "--destination",
            type=str,
            default="Plugins",
            help="Plugin destination, relative to the root of the project",
        )
        install.add_argument(
            "--submodule",
            action="store_true",
            default=False,
            help="add the plugin as a git submodule",
        )

    @staticmethod
    def execute(args):
        pass


COMMAND = Install
