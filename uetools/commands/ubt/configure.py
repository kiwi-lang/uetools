import os
import xml.etree.ElementTree as ET
from copy import deepcopy
from dataclasses import asdict, dataclass, field

from uetools.core.command import Command, newparser
from uetools.core.conf import engine_folder

valid_file = """
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ParallelExecutor>
        <MaxProcessorCount>32</MaxProcessorCount>
    </ParallelExecutor>
    <BuildConfiguration>
    </BuildConfiguration>
    <WindowsPlatform>
    </WindowsPlatform>
</Configuration>
"""


# Can I make a Dataclass of the UBT config and initialize it using the XML
# and save the XML from the dataclass ?
# 100% it is possible, just might take some time
# I can just save the dataclass as a dict and save the values as
#
# <dict>
#   <key>value</key>
# </dict>


@dataclass
class WindowsPlatformT:
    """Windows Platform"""


@dataclass
class ModuleConfigurationT:
    """Module Configuration"""


@dataclass
class FASTBuildT:
    """FAST Build"""


@dataclass
class TaskExecutorT:
    """TaskExecutor"""


@dataclass
class HybridExecutorT:
    """HybridExecutor"""


@dataclass
class ParallelExecutorT:
    """ParallelExecutor"""

    bStopCompilationAfterErrors: bool = False
    bShowCompilationTimes: bool = False
    bShowPerActionCompilationTimes: bool = True
    bLogActionCommandLines: bool = True
    bPrintActionTargetNames: bool = True
    MaxProcessorCount: int = 32
    ProcessorCountMultiplier: float = 1
    MemoryPerActionBytes: int = 0


@dataclass
class SNDBST:
    """SNDBS"""


@dataclass
class XGET:
    """XGE"""


@dataclass
class BuildModeT:
    """BuildMode"""


@dataclass
class ProjectFileGeneratorT:
    """ProjectFileGenerator"""


@dataclass
class HoloLensPlatformT:
    """HoloLensPlatform"""


@dataclass
class IOSToolChainT:
    """IOSToolChain"""


@dataclass
class WindowsTargetRulesT:
    """WindowsTargetRules"""


@dataclass
class CLionGeneratorT:
    """CLionGenerator"""


@dataclass
class CMakeFileGeneratorT:
    """CMakeFileGenerator"""


@dataclass
class CodeLiteGeneratorT:
    """CodeLiteGenerator"""


@dataclass
class EddieProjectFileGeneratorT:
    """EddieProjectFileGenerator"""


@dataclass
class KDevelopGeneratorT:
    """KDevelopGenerator"""


@dataclass
class MakefileGeneratorT:
    """MakefileGenerator"""


@dataclass
class QMakefileGeneratorT:
    """QMakefileGenerator"""


@dataclass
class RiderProjectGeneratorT:
    """RiderProjectGenerator"""


@dataclass
class VSCodeProjectFileGeneratorT:
    """VSCodeProjectFileGenerator"""


@dataclass
class VCMakeProjectFileGeneratorT:
    """VCMakeProjectFileGenerator"""


@dataclass
class VCProjetFileGeneratorT:
    """VCProjetFileGenerator"""


@dataclass
class XCodeProjectFileGeneratorT:
    """XCodeProjectFileGenerator"""


@dataclass
class SourceFileWorkingSetT:
    """SourceFileWorkingSet"""


@dataclass
class RemoteMacT:
    """RemoteMac"""


@dataclass
class LogT:
    """Log"""


@dataclass
class Configuration:
    """Configuration"""

    WindowsPlatform: WindowsPlatformT = field(default_factory=WindowsPlatformT)
    ModuleConfiguration: ModuleConfigurationT = field(
        default_factory=ModuleConfigurationT
    )
    FASTBuild: FASTBuildT = field(default_factory=FASTBuildT)
    TaskExecutor: TaskExecutorT = field(default_factory=TaskExecutorT)
    HybridExecutor: HybridExecutorT = field(default_factory=HybridExecutorT)
    ParallelExecutor: ParallelExecutorT = field(default_factory=ParallelExecutorT)
    SNDBS: SNDBST = field(default_factory=SNDBST)
    XGE: XGET = field(default_factory=XGET)
    BuildMode: BuildModeT = field(default_factory=BuildModeT)
    ProjectFileGenerator: ProjectFileGeneratorT = field(
        default_factory=ProjectFileGeneratorT
    )
    HoloLensPlatform: HoloLensPlatformT = field(default_factory=HoloLensPlatformT)
    IOSToolChain: IOSToolChainT = field(default_factory=IOSToolChainT)
    WindowsTargetRules: WindowsTargetRulesT = field(default_factory=WindowsTargetRulesT)
    CLionGenerator: CLionGeneratorT = field(default_factory=CLionGeneratorT)
    CMakeFileGenerator: CMakeFileGeneratorT = field(default_factory=CMakeFileGeneratorT)
    CodeLiteGenerator: CodeLiteGeneratorT = field(default_factory=CodeLiteGeneratorT)
    EddieProjectFileGenerator: EddieProjectFileGeneratorT = field(
        default_factory=EddieProjectFileGeneratorT
    )
    KDevelopGenerator: KDevelopGeneratorT = field(default_factory=KDevelopGeneratorT)
    MakefileGenerator: MakefileGeneratorT = field(default_factory=MakefileGeneratorT)
    QMakefileGenerator: QMakefileGeneratorT = field(default_factory=QMakefileGeneratorT)
    RiderProjectGenerator: RiderProjectGeneratorT = field(
        default_factory=RiderProjectGeneratorT
    )
    VSCodeProjectFileGenerator: VSCodeProjectFileGeneratorT = field(
        default_factory=VSCodeProjectFileGeneratorT
    )
    VCMakeProjectFileGenerator: VCMakeProjectFileGeneratorT = field(
        default_factory=VCMakeProjectFileGeneratorT
    )
    VCProjetFileGenerator: VCProjetFileGeneratorT = field(
        default_factory=VCProjetFileGeneratorT
    )
    XCodeProjectFileGenerator: XCodeProjectFileGeneratorT = field(
        default_factory=XCodeProjectFileGeneratorT
    )
    SourceFileWorkingSet: SourceFileWorkingSetT = field(
        default_factory=SourceFileWorkingSetT
    )
    RemoteMac: RemoteMacT = field(default_factory=RemoteMacT)
    Log: LogT = field(default_factory=LogT)


def find_or_insert(root, *paths, namespaces=None):
    node = root
    for i, p in enumerate(paths):
        full_path = "ue:" + "/ue:".join(paths[: i + 1])
        val = root.find(full_path, namespaces)

        if val is None:
            val = ET.Element(p)
            node.insert(0, val)

        node = val

    return val


class Configure(Command):
    """Disable unused plugin that are loading by default"""

    name: str = "configure"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Configure)
        parser.add_argument(
            "--cpu", default=32, type=int, help="Limit the number of cpu to use"
        )

    @staticmethod
    def execute(args):
        #
        # https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/DevelopmentSetup/BuildConfigurations/
        # https://docs.unrealengine.com/5.0/en-US/build-configuration-for-unreal-engine/
        #
        engine = engine_folder()
        namespaces = {"ue": "https://www.unrealengine.com/BuildConfiguration"}

        # this should work for everybody but it doesn't
        global_ubt_config = os.path.join(
            engine, "Saved", "UnrealBuildTool", "BuildConfiguration.xml"
        )
        if os.name != "nt":
            # this is not loaded by UBT
            # UnrealEngine\Engine\Source\Programs\UnrealBuildTool\System\XmlConfig.cs
            #   this one is ignored if touch /opt/UnrealEngine/Engine/Build/InstalledBuild.txt exists
            #   creating the file triggers a bunch of other issues
            #
            #   FileReference UserConfigLocation = FileReference.Combine(Unreal.EngineDirectory, "Saved", "UnrealBuildTool", "BuildConfiguration.xml");
            #   FileReference.Combine(new DirectoryReference(AppDataFolder), "Unreal Engine", "UnrealBuildTool", "BuildConfiguration.xml");
            #   FileReference.Combine(new DirectoryReference(PersonalFolder), "Unreal Engine", "UnrealBuildTool", "BuildConfiguration.xml");
            #
            #   AppDataFolder = ''              <= this should be ~/.config # XDG_CONFIG_HOME
            #   PersonalFolder = /home/runner   <= this

            home = os.path.expanduser("~")
            app_data = os.path.join(home, ".config")
            if "XDG_CONFIG_HOME" not in os.environ:
                os.environ["XDG_CONFIG_HOME"] = app_data
            else:
                app_data = os.environ["XDG_CONFIG_HOME"]

            app_ubt_config = os.path.join(
                app_data,
                "Unreal Engine",
                "UnrealBuildTool",
                "BuildConfiguration.xml",
            )

            user_ubt_config = os.path.join(
                home,
                "Unreal Engine",
                "UnrealBuildTool",
                "BuildConfiguration.xml",
            )

        # user_ubt_config = os.path.join(home, "AppData", "Roaming", "Unreal Engine", "UnrealBuildTool", "BuildConfiguration.xml")
        # local_ubt_config = os.path.join(home, "Documents", "Unreal Engine", "UnrealBuildTool", "BuildConfiguration.xml")

        ET.register_namespace("", "https://www.unrealengine.com/BuildConfiguration")
        tree = ET.parse(global_ubt_config)

        root = tree.getroot()
        node = find_or_insert(
            root, "ParallelExecutor", "MaxProcessorCount", namespaces=namespaces
        )

        oldval = node.text
        node.text = str(args.cpu)

        print(f"CPU {oldval} => {args.cpu}")

        ET.indent(tree, space="  ", level=0)
        tree.write(global_ubt_config, xml_declaration=True, encoding="utf-8")
        return 0


COMMANDS = Configure


def from_xml(filename: str) -> Configuration:
    """Parse UBT XML Configuration file"""
    namespaces = {"ue": "https://www.unrealengine.com/BuildConfiguration"}
    ET.register_namespace("", "https://www.unrealengine.com/BuildConfiguration")
    tree = ET.parse(filename)

    root = tree.getroot()
    config = asdict(Configuration())

    path = []
    _from_xml(config, path, root, namespaces, 0)

    return config


def _from_xml(config, path: list, tree, namespaces, depth):
    configdict = asdict(config)

    for k, v in configdict.items():
        fullpath = deepcopy(path) + [k]
        ref = getattr(config, k)

        if isinstance(v, dict):
            _from_xml(ref, fullpath, tree, namespaces, depth + 1)

        else:
            fullpath = "/".join([f"ue:{p}" for p in fullpath])
            node = tree.find(fullpath, namespaces)
            setattr(config, k, node.text)


def to_xml(config: Configuration) -> str:
    """Writes a UBT XML configuration file"""
    frags = []

    dictconf = asdict(config)

    frags.append('<?xml version="1.0" encoding="utf-8" ?>\n')
    frags.append(
        '<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">'
    )
    _to_xml(dictconf, frags, 1)
    frags.append("</Configuration>")

    return "".join(frags)


def _to_xml(dictionary: dict, output: list, depth: int) -> None:
    idt = "  " * depth

    for k, v in dictionary.items():
        if not v:
            continue

        if isinstance(v, dict):
            output.append(f"\n{idt}<{k}>")
            _to_xml(v, output, depth + 1)
            output.append(f"\n{idt}</{k}>\n")
        else:
            output.append(f"\n{idt}<{k}>")
            output.append(f"{v}")
            output.append(f"</{k}>")


def check():
    """check POC"""
    config = Configuration()
    print(to_xml(config))


if __name__ == "__main__":
    check()
