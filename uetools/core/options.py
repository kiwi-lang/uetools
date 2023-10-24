
import dataclasses

from uetools.args.arguments import choice
from uetools.core.conf import get_build_platforms, guess_platform


def platform_choice():
    return choice(*get_build_platforms(), default=guess_platform())


def platform_choices():
    metadata = dict()
    metadata['nargs'] ='+'
    metadata["choices"] = get_build_platforms()
    metadata["_kind"] = 'argument'
    metadata["type"] = str
    metadata["default"] = [guess_platform()]
    
    return dataclasses.field(
        default_factory=lambda: [guess_platform()],
        metadata=metadata
    )