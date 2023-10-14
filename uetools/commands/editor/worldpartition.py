# https://docs.unrealengine.com/5.0/en-US/world-partition-in-unreal-engine/


from dataclasses import dataclass
from typing import Optional

from uetools.args.command import Command, command_builder
from uetools.core.conf import editor_cmd
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter
from uetools.core.util import deduce_project


class WorldPartition(Command):
    """Convert a UE4 map using world partition"""

    name: str = "worldpartition"

    # fmt: off
    @dataclass
    class Arguments:
        """Convert a UE4 map using world partition"""

        map                     : str
        project                 : Optional[str] = deduce_project()  # Name of the the project to open
        SCCProvider             : Optional[str] = None   # Specifies which source control provider to use. To run without source control, specify -SCCProvider=None.
        Verbose                 : bool          = False  # Displays verbose logging.
        ConversionSuffix        : bool          = False  # Appends the _WP suffix to a converted map. This is useful when converting Levels for testing purposes while keeping the source Level intact.
        DeleteSourceLevel       : bool          = False  # Deletes source Levels after conversion.
        ReportOnly              : bool          = False  # Reports what would happen during the conversion. Does not do the conversion.
        GenerateIni             : bool          = False  # Generates a default .ini conversion file for this map. Does not do the conversion.
        SkipStableGUIDValidation: bool          = False  # Skips the unstable actor GUIDs validation process. Levels with unstable actor GUIDs will result in different conversion output when converting several times. Resaving the Level fixes this.
        OnlyMergeSubLevels      : bool          = False  # Converts and merges Levels and Sublevels to One File Per Actor without World Partition. The converted Level can be used as a Level Instance in a World Partition Level.
        FoliageTypePath         : Optional[str] = None   # Extracts Foliage Types as Assets to the given path. Use if the Level contains embedded Foliage Types.
    # fmt: on

    @staticmethod
    def execute(args):
        cmd = [editor_cmd()] + command_builder(args)
        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = WorldPartition
