from dataclasses import dataclass
import os

from tqdm import tqdm

from uetools.args.command import Command


def zipfolder(src, dest, progress):
    import zipfile

    zip_filename = dest + ".zip"
    archive_dir = os.path.dirname(dest)

    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    if archive_dir:
        os.makedirs(archive_dir, exist_ok=True)

    with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        path = os.path.normpath(src)
        if path != os.curdir:
            zf.write(path, path)
            progress.update(1)

        for dirpath, dirnames, filenames in os.walk(src):
            for name in sorted(dirnames):
                path = os.path.normpath(os.path.join(dirpath, name))
                zf.write(path, path)
                progress.update(1)
            
            for name in filenames:
                path = os.path.normpath(os.path.join(dirpath, name))
                if os.path.isfile(path):
                    zf.write(path, path)
                    progress.update(1)


class Zip(Command):
    """Publish a gitlab package to the registry
    
    Examples
    --------

    .. code-block::

       uecli gitlab zip ./ArchivedBuilds/Windows/ Acara

       E:/Examples/Acaraceim/Acara.zip

    """

    name: str = "zip"

    @dataclass
    class Arguments:
        src: str
        dest: str

    @staticmethod
    def execute(args):
        import zipfile
        
        with tqdm() as progress:
            zipfolder(args.src, args.dest, progress)
        
        return 0


COMMANDS = Zip
