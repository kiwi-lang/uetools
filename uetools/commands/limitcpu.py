import os
from dataclasses import dataclass
import xml.etree.ElementTree as ET

from uetools.core.command import Command, newparser
from uetools.core.conf import find_project, engine_folder


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

class LimitCPU(Command):
    """Disable unused plugin that are loading by default"""

    name: str = "limitcpu"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, LimitCPU)
        parser.add_argument('--cpu', default=32, type=int, help='Limit the number of cpu to use')

    @staticmethod
    def execute(args):
        engine = engine_folder()
        namespaces = {
            "ue": 'https://www.unrealengine.com/BuildConfiguration'
        }
        global_ubt_config = os.path.join(engine, "Saved", "UnrealBuildTool", "BuildConfiguration.xml")
        # user_ubt_config = os.path.join(home, "AppData", "Roaming", "Unreal Engine", "UnrealBuildTool", "BuildConfiguration.xml")
        # local_ubt_config = os.path.join(home, "Documents", "Unreal Engine", "UnrealBuildTool", "BuildConfiguration.xml")

        ET.register_namespace("", 'https://www.unrealengine.com/BuildConfiguration')
        tree = ET.parse(global_ubt_config)
        
        root = tree.getroot()

        val = root.find("ue:ParallelExecutor/ue:MaxProcessorCount", namespaces)
        oldval = val.text
        val.text = str(args.cpu)

        print(f'CPU {oldval} => {args.cpu}')
        tree.write(global_ubt_config, xml_declaration=True, encoding='utf-8')

        return 0




COMMANDS = LimitCPU
