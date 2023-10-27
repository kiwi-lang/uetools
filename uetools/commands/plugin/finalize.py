import json
import os
import shutil
from dataclasses import dataclass

from argklass.command import Command

from uetools.core.conf import engine_folder, get_version_tag, retrieve_exact_engine_version
from uetools.core.util import deduce_plugin


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
        output: str  # output
        plugin: str = deduce_plugin()  # plugin name
        marketplace: bool = False  # make the folder marketplace friendly

    @staticmethod
    def execute(args):
        errors = []

        base_url = "com.epicgames.launcher://ue/marketplace/product/"
        plugin_dir = os.path.dirname(os.path.abspath(args.plugin))

        plugin_version = get_version_tag(plugin_dir).replace("v", "").split("-")[0]

        engine_version = retrieve_exact_engine_version(engine_folder())

        # Configure the plugin descriptor
        # -------------------------------
        with open(args.output) as f:
            uplugin = json.load(f)

        version_old = uplugin.get("VersionName") or ""
        installed_old = uplugin.get("Installed") or ""
        engine_old = uplugin.get("EngineVersion") or ""

        uplugin["VersionName"] = plugin_version
        uplugin["Installed"] = False
        uplugin["EngineVersion"] = engine_version

        print(f"Plugin Version: {version_old:<10} => ", plugin_version)
        print(f"     Installed: {installed_old:<10} => ", False)
        print(f" EngineVersion: {engine_old:<10} => ", engine_version)

        if len(uplugin["MarketplaceURL"][len(base_url) :]) <= 0:
            errors.append("MarketPlace URL missing")

        with open(args.output, "w") as f:
            json.dump(uplugin, f, indent=2)

        # Copy files
        # ----------
        config_folder = os.path.join(plugin_dir, "Config")

        if os.path.exists(config_folder):
            output_folder = os.path.dirname(args.output)
            shutil.copytree(config_folder, os.path.join(output_folder, "Config"), dirs_exist_ok=True)

        # Remove build files
        # ------------------
        if args.marketplace:
            FinalizePlugin.remove_temp_folders(output_folder)

        print()
        print("Errors:")
        print("-------")
        for err in errors:
            print(f" - {err}")

        return len(errors)

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
