import argparse
import os
import xml.etree.ElementTree as ET
from copy import deepcopy
from dataclasses import asdict, fields, is_dataclass
import textwrap

from uetools.args.command import Command, newparser
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


def get_user_ubt_configfile():
    from pathlib import Path

    home_dir = Path.home()

    user_ubt_config = os.path.join(
        home_dir,
        "AppData",
        "Roaming",
        "Unreal Engine",
        "UnrealBuildTool",
        "BuildConfiguration.xml",
    )

    return user_ubt_config


def get_global_ubt_configfile():
    engine = engine_folder()
    global_ubt_config = os.path.join(
        engine, "Saved", "UnrealBuildTool", "BuildConfiguration.xml"
    )
    return global_ubt_config


def get_ubt_configfile():
    return get_user_ubt_configfile()


class Configure(Command):
    """Configure UBT by modifying its XML configuration file

    Examples
    --------

    .. code-block:: python

        $ ubt configure ParallelExecutor.MaxProcessorCount=16
        ParallelExecutor.MaxProcessorCount: 16 => 16

        $ uecli ubt configure BuildConfiguration.MaxParallelActions=8


        $ uecli ubt configure --list

        $ uecli ubt configure --list --filter BuildConfiguration

    Notes
    -----

    ``ParallelExecutor.MaxProcessorCount`` does not have to have an effect anymore
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
            "--filter", type=str, default=None, help="Key filter when doing list"
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
        print("Change")
        print("------")

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
                    old = getattr(node, p)
                    setattr(node, p, value)
                    print(f"  - {key}: (old: {old}) => (new: {value})")
                else:
                    raise Configure.error(node, p)
            except Exception as err:
                raise RuntimeError(
                    f"Pair {pair} does not follow the expected format <key>.<key>=<value>"
                ) from err

        print()

    @staticmethod
    def execute(args):
        configfile = get_ubt_configfile()
        configuration = from_xml(configfile)

        if args.list:
            print("    " + Configure.help())
            list_commands(args.filter)
            return

        Configure.change_config(configuration, args.items)

        output = to_xml(configuration)

        if args.show:
            print("File")
            print("-----")
            print(f"    {configfile}")
            print()
            print("XML")
            print("---")
            print(output)

        if not args.dry:
            with open(configfile, "w") as file:
                file.write(output)

        return 0


COMMANDS = Configure


def list_commands(filter=None):
    output = []

    print("Keys:")
    _list_commands(Configuration(), output, [], 1, filter)

    print("\n".join(output))


def _list_commands(config, output, namespaces, depth, filter):
    import copy
    from uetools.args.arguments import find_dataclass_docstring, find_docstring

    indent = "  " * depth

    source, _, start = find_dataclass_docstring(config.__class__)

    for ffield in fields(config):
        nm = copy.deepcopy(namespaces) + [ffield.name]

        docstring, start = find_docstring(ffield, source, start)

        value = getattr(config, ffield.name)
        if is_dataclass(value):
            items = []
            _list_commands(value, items, nm, depth + 1, filter)

            if items:
                output.extend(items)

        else:
            key = ".".join(nm)
            type = ffield.type.__name__
            value = getattr(config, ffield.name)

            if filter is None or filter in key:
                _show_field(output, indent, key, value, type, docstring)


def _show_field(output, indent, key, value, type, docstring, kind=None):
    col = 60

    if kind is None:
        kind = "compact"

    msg = f"{key:<{col}}: {type:<5} = {value}"

    #
    #
    #
    if kind == "simple":
        output.append(f"{indent}{msg}")

    #
    #
    #
    if kind == "compact":
        output.append(f"{indent}{msg}")

        wrap_iter = textwrap.wrap(docstring, width=col, subsequent_indent="")

        for i, line in enumerate(wrap_iter):
            output.append(f"{indent}    # {line}")
        output.append("")

    #
    #
    #
    if kind == "full":
        wrap_iter = textwrap.wrap(docstring, width=40, subsequent_indent=" ")

        for i, line in enumerate(wrap_iter):
            if i == 0:
                output.append(f"{indent}{msg} # {line}")
            else:
                output.append(f"{indent}{' ':<{len(msg)}} # {line}")


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
    frags.append("\n</Configuration>")
    return "".join(frags)


def _convert_value(v):
    v = v.strip()

    if v == "True":
        v = 1

    if v == "False":
        v = 0

    return v


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
                output.append(f"\n{idt}</{k}>")

        else:
            output.append(f"\n{idt}<{k}>")
            output.append(f"{_convert_value(v)}")
            output.append(f"</{k}>")
