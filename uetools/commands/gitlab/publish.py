from dataclasses import dataclass
import os
import pathlib

import requests
from tqdm import tqdm

from uetools.args.arguments import choice
from uetools.args.command import Command
from uetools.core.conf import find_project
from uetools.core.util import deduce_project
from uetools.core.conf import get_build_platforms, guess_platform


def platform_choice():
    return choice(*get_build_platforms(), default=guess_platform())


default_url = "https://gitlab.com/api/v4/"


class ChunkUploader:
    def __init__(self, filename, chunksize=1024):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0

    def bar(self):
        return tqdm(total=self.totalsize, unit="B", unit_scale=True, unit_divisor=1024)

    def __iter__(self):
        with self.bar() as progress:
            with open(self.filename, "rb") as file:
                while True:
                    data = file.read(self.chunksize)

                    if not data:
                        break

                    progress.update(len(data))
                    yield data

    def __len__(self):
        return self.totalsize


class Publish(Command):
    """Publish a gitlab package to the registry"""

    name: str = "publish"

    # fmt: off
    @dataclass
    class Arguments:
        filename: str
        project: str = deduce_project()  # project's name
        platform: str = platform_choice()
        chunk: int = 1024 * 8

        api_url: str      = os.getenv("CI_API_V4_URL", default_url)
        project_id: str   = os.getenv("CI_PROJECT_ID")
        commit_tag: str   = os.getenv("CI_COMMIT_TAG")
        commit_short: str = os.getenv("CI_COMMIT_SHORT_SHA")
        token: str        = os.getenv("CI_JOB_TOKEN")
        # fmt: on

    @staticmethod
    def execute(args):
        project_path = find_project(args.project)
        project_name = os.path.basename(project_path)[:-9]

        project = project_name
        platform = args.platform

        file_path: str = args.filename
        chunk_size = args.chunk

        ext = file_path.rsplit(".", maxsplit=1)[1]

        package_name = f"{project}"
        package_version = f"{platform}-{args.commit_short}"
        filename = f"{project}-{args.commit_tag}.{ext}"

        # PUT /projects/:id/packages/generic/:package_name/:package_version/:file_name?status=:status
        url = f"{args.api_url}/projects/{args.project_id}/packages/generic/{package_name}/{package_version}/{filename}"

        headers = {"JOB-TOKEN": args.token}

        print("URL: ", url)
        response = requests.put(
            url, 
            headers=headers, 
            data=ChunkUploader(file_path, chunk_size),
        )

        if response.status_code == 200:
            return 0

        print(response.text)
        return -1


COMMANDS = Publish
