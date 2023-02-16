import argparse
import os
import xml.etree.ElementTree as ET
from copy import deepcopy
from dataclasses import asdict, fields, is_dataclass

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

from .xmldef import Configuration


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


def get_ubt_configfile():
    engine = engine_folder()
    global_ubt_config = os.path.join(
        engine, "Saved", "UnrealBuildTool", "BuildConfiguration.xml"
    )
    return global_ubt_config


class Configure(Command):
    """Configure UBT by modifying its XML configuration file

    Examples
    --------

    .. code-block:: python

        $ ubt configure ParallelExecutor.MaxProcessorCount=16
        ParallelExecutor.MaxProcessorCount: 16 => 16

    """

    name: str = "configure"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Configure)
        parser.add_argument(
            "--show", action="store_true", help="Show the generated XML"
        )
        parser.add_argument(
            "--dry",
            action="store_true",
            help="Do not persist the configuration change to disk",
        )
        parser.add_argument(
            "--list", action="store_true", help="Show all the possible keys"
        )
        parser.add_argument(
            "items",
            nargs=argparse.REMAINDER,
            help="Configuration values to change, format is <key>.<key>=<value>",
        )

    @staticmethod
    def error(node, p):
        attr = ", ".join(list(asdict(node).keys()))
        name = node.__class__.__name__
        return RuntimeError(
            f"Node {name} does not have a '{p}' attribute choose between: {attr}"
        )

    @staticmethod
    def change_config(configuration, items):
        # Change Configuration
        for pair in items:
            try:
                key, value = pair.split("=")
                path = key.split(".")

                node = configuration
                for p in path[:-1]:
                    if hasattr(node, p):
                        node = getattr(node, p)
                    else:
                        raise Configure.error(node, p)

                p = path[-1]
                if hasattr(node, p):
                    setattr(node, p, value)
                    print(f"{key}: {getattr(node, p)} => {value}")
                else:
                    raise Configure.error(node, p)
            except Exception as err:
                raise RuntimeError(
                    f"Pair {pair} does not follow the expected format <key>.<key>=<value>"
                ) from err

    @staticmethod
    def execute(args):
        configfile = get_ubt_configfile()
        configuration = from_xml(configfile)

        if args.list:
            print("    " + Configure.help())
            list_commands()
            return

        Configure.change_config(configuration, args.items)

        output = to_xml(configuration)

        if args.show:
            print(output)

        if not args.dry:
            with open(configfile, "w") as file:
                file.write(output)

        return 0


COMMANDS = Configure


def list_commands():
    output = []

    print("Keys:")
    _list_commands(Configuration(), output, [], 1)

    print("\n".join(output))


def _list_commands(config, output, namespaces, depth):
    import copy

    indent = "  " * depth

    for ffield in fields(config):
        nm = copy.deepcopy(namespaces) + [ffield.name]

        value = getattr(config, ffield.name)
        if is_dataclass(value):
            items = []
            _list_commands(value, items, nm, depth + 1)

            if items:
                # output.append(f'{indent}{field.name}')
                output.extend(items)

        else:
            key = ".".join(nm)
            type = ffield.type.__name__
            value = getattr(config, ffield.name)
            output.append(f"{indent}{key:<50}: {type:<5} = {value}")


def from_xml(filename: str) -> Configuration:
    """Parse UBT XML Configuration file"""

    if not os.path.exists(filename):
        return Configuration()

    namespaces = {"ue": "https://www.unrealengine.com/BuildConfiguration"}
    ET.register_namespace("", "https://www.unrealengine.com/BuildConfiguration")
    tree = ET.parse(filename)

    root = tree.getroot()
    config = Configuration()

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

            if node is not None:
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
            child = []
            _to_xml(v, child, depth + 1)

            if child:
                output.append(f"\n{idt}<{k}>")
                output.extend(child)
                output.append(f"\n{idt}</{k}>\n")

        else:
            output.append(f"\n{idt}<{k}>")
            output.append(f"{v}")
            output.append(f"</{k}>")
