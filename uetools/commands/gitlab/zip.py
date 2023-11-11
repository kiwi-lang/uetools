import os
from dataclasses import dataclass

from argklass.command import Command
from tqdm import tqdm


def zipfolder(src, dest, progress, topfolder):
    import zipfile

    def rename(path: str):
        abssrc = os.path.abspath(src)
        path = os.path.abspath(path)
        common = os.path.commonpath([path, abssrc])

        if topfolder is None:
            wrap = os.path.split(abssrc)[-1]
        else:
            wrap = topfolder
            
        newname = path.removeprefix(common)

        if newname and (newname[0] == '\\' or newname[0] == '/'):
            newname = newname[1:]

        newname = os.path.join(wrap, newname)
        newname = newname.replace('\\', '/')

        if False:
            print(newname)
        
        return newname

    zip_filename = dest
    archive_dir = os.path.dirname(dest)

    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    if archive_dir:
        os.makedirs(archive_dir, exist_ok=True)

    with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        path = os.path.normpath(src)

        if path != os.curdir:
            zf.write(path, rename(path))
            progress.update(1)

        for dirpath, dirnames, filenames in os.walk(src):
            for name in sorted(dirnames):
                path = os.path.normpath(os.path.join(dirpath, name))
                zf.write(path, rename(path))
                progress.update(1)

            for name in filenames:
                path = os.path.normpath(os.path.join(dirpath, name))
                if os.path.isfile(path):
                    zf.write(path, rename(path))
                    progress.update(1)


class Zip(Command):
    """Zip a folder;
    The content of the folder is wrapped inside a folder named after the zip archive.

    Examples
    --------

    .. code-block::

       uecli gitlab zip ./ArchivedBuilds/Windows/ Acara.zip

       E:/Examples/Acaraceim/Acara.zip

    """

    name: str = "zip"

    @dataclass
    class Arguments:
        src: str
        dest: str
        name: str = None

    @staticmethod
    def execute(args):
        try:
            if args.name is None:
                _, tail = os.path.split(args.dest)
                args.name = tail.split('.')[0]
        except:
            pass
    
        with tqdm() as progress:
            zipfolder(args.src, args.dest, progress, args.name)

        return 0


COMMANDS = Zip
