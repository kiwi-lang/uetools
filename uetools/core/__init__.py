"""Top level module for uetools"""

__descr__ = "Unreal Engine Tools"
__version__ = "0.1.5"
__license__ = "BSD 3-Clause License"
__author__ = "Pierre Delaunay"
__author_email__ = "pierre@delaunay.io"
__copyright__ = "2022 Pierre Delaunay"
__url__ = "https://github.com/kiwi-lang/uetools"


from .cli import args, main

__slot___ = ["main", "args"]
