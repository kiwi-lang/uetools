import os
from dataclasses import asdict, dataclass

from simple_parsing import choice

from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import find_project, ubt
from uetools.core.run import run

NONE = object()

generators = [
    "Make",
    "CMake",
    "QMake",
    "KDevelop",
    "CodeLite",
    "VisualStudio",
    "VisualStudio2019",
    "VisualStudio2022",
    "XCode",
    "Eddie",
    "VisualStudioCode",
    "VisualStudioMac",
    "CLion",
    "Rider",
    NONE,
]

# fmt: off
@dataclass
class Arguments:
    """Generate project files

    Notes
    -----

    While UBT shows all those generator options, none of them really work.
    For them to be used you need to modify the ``BuildConfiguration.xml`` which is the configuration
    used for the project file configuration.

    The build configuration can be found in ``${ENGINE_ROOT}/Engine/Saved/UnrealBuildTool/BuildConfiguration.xml

    .. code-block:: xml

       <?xml version="1.0" encoding="utf-8" ?>
       <Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
           <ProjectFileGenerator>
               <Format>VisualStudioCode</Format>
           </ProjectFileGenerator>
       </Configuration>

    """

    makefile            : bool = False  # Generate Linux Makefile
    cmakefile           : bool = False  # Generate project files for CMake
    qmakefile           : bool = False  # Generate project files for QMake
    kdevelopfile        : bool = False  # Generate project files for KDevelop
    codelitefiles       : bool = False  # Generate project files for Codelite
    xcodeprojectfiles   : bool = False  # Generate project files for XCode
    eddieprojectfiles   : bool = False  # Generate project files for Eddie
    vscode              : bool = False  # Generate project files for Visual Studio Code
    vsmac               : bool = False  # Generate project files for Visual Studio Mac
    clion               : bool = False  # Generate project files for CLion
    rider               : bool = False  # Generate project files for Rider
    projectfiles        : bool = True   # Generate project files based on IDE preference.
    projectfileformat   : str = choice(*generators, default=NONE, type=str)
    game                : bool = True
    engine              : bool = True
    progress            : bool = True
# fmt: on


class Generate(Command):
    """Generate project files"""

    name: str = "regenerate"

    @staticmethod
    def arguments(subparsers):
        """Adds the arguments for this command to the given parser"""
        parser = newparser(subparsers, Generate)
        parser.add_argument("project", type=str, help="project name")
        parser.add_arguments(Arguments, dest="args")

    @staticmethod
    def execute(args):

        project = find_project(args.project)

        cmd = [ubt(), f"-project={project}", "-Mode=GenerateProjectFiles"]

        cmd_options = command_builder(asdict(args.args))

        cmd = cmd + cmd_options

        print(" ".join(cmd))

        root = os.path.dirname(project)

        return run(
            cmd,
            check=True,
            cwd=root,
        ).returncode


COMMANDS = Generate
