import json
import os
import shutil
from dataclasses import dataclass

from uetools.core.arguments import add_arguments
from uetools.core.command import Command, newparser
from uetools.core.conf import (
    engine_folder,
    get_version_tag,
    retrieve_exact_engine_version,
)


class FinalizePlugin(Command):
    """Finalize Plugin for redistribution

    * Set the engine version inside the <plugin>.uplugin
    * Set installed to false inside <plugin>.uplugin
    * Check MarketplaceURL
    * Set VersionName
    * Copy some Config folder

    """

    name: str = "finalize"

    @dataclass
    class Arguments:
        plugin: str  #: plugin name
        output: str  #: output
        marketplace: bool = False  #: make the folder marketplace friendly

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, FinalizePlugin)
        add_arguments(parser, FinalizePlugin.Arguments)

    @staticmethod
    def execute(args):
        base_url = "com.epicgames.launcher://ue/marketplace/product/"
        plugin_dir = os.path.dirname(os.path.abspath(args.plugin))

        plugin_version = get_version_tag(plugin_dir).replace("v", "").split("-")[0]

        engine_version = retrieve_exact_engine_version(engine_folder())

        # Configure the plugin descriptor
        # -------------------------------
        with open(args.output) as f:
            uplugin = json.load(f)

        version_old = uplugin["VersionName"]
        installed_old = uplugin["Installed"]
        engine_old = uplugin["EngineVersion"]

        uplugin["VersionName"] = plugin_version
        uplugin["Installed"] = False
        uplugin["EngineVersion"] = engine_version

        print("Plugin Version:", version_old, " => ", plugin_version)
        print("     Installed:", installed_old, " => ", False)
        print(" EngineVersion:", engine_old, " => ", engine_version)

        assert (
            len(uplugin["MarketplaceURL"][len(base_url) :]) > 0
        ), "MarketPlace URL missing"

        with open(args.output, "w") as f:
            json.dump(uplugin, f, indent=2)

        # Copy files
        # ----------
        config_folder = os.path.join(plugin_dir, "Config")
        output_folder = os.path.dirname(args.output)

        shutil.copytree(
            config_folder, os.path.join(output_folder, "Config"), dirs_exist_ok=True
        )

        if args.marketplace:
            FinalizePlugin.remove_temp_folders(output_folder)

    @staticmethod
    def remove_temp_folders(output_folder):
        bad_folders = [
            "Binaries",
            "Build",
            "Intermediate",
            "Saved",
            "DerivedDataCache",
            "Cooked",
        ]

        def handler(function, path, excinfo):
            cls, instance, traceback = excinfo

            print(f"{instance}: {path}")

        for folder in bad_folders:
            to_be_removed = os.path.join(output_folder, folder)

            if os.path.exists(to_be_removed):
                print(f"Removing {to_be_removed}")
                shutil.rmtree(to_be_removed, onerror=handler)


COMMANDS = FinalizePlugin
