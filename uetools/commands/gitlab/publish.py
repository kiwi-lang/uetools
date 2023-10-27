import os
from dataclasses import dataclass

import requests
from argklass.command import Command
from tqdm import tqdm

from uetools.core.conf import find_project
from uetools.core.options import platform_choice, projectfield

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


def upload_package(
    src,
    api_url,
    project_id,
    package_name,
    package_version,
    filename,
    token,
    chunk_size=1024,
):
    # PUT /projects/:id/packages/generic/:package_name/:package_version/:file_name?status=:status
    url = f"{api_url}/projects/{project_id}/packages/generic/{package_name}/{package_version}/{filename}"

    if os.getenv("CI_JOB_TOKEN") is not None:
        headers = {"JOB-TOKEN": token}
    else:
        headers = {"Authorization": f"Bearer {token}"}

    print("URL: ", url)
    response = requests.put(
        url,
        headers=headers,
        data=ChunkUploader(src, chunk_size),
    )

    if response.status_code in (200, 201):
        return 0

    raise RuntimeError(response.text)


class Publish(Command):
    """Publish a gitlab package to the registry"""

    name: str = "publish"

    # fmt: off
    @dataclass
    class Arguments:
        path: str
        filename: str
        package: str = None
        project: str = projectfield()  # project's name
        platform: str = platform_choice()
        chunk: int = 1024 * 8

        api_url: str      = os.getenv("CI_API_V4_URL", default_url)
        project_id: str   = os.getenv("CI_PROJECT_ID")
        commit_tag: str   = os.getenv("CI_COMMIT_TAG", "v0.0.0")
        commit_short: str = os.getenv("CI_COMMIT_SHORT_SHA")
        token: str        = os.getenv("CI_JOB_TOKEN")
        # fmt: on

    @staticmethod
    def execute(args):
        project_path = find_project(args.project)
        project_name = os.path.basename(project_path)[:-9]

        project = project_name
        platform = args.platform
        ext = args.path.rsplit(".", maxsplit=1)[1]

        if args.package is None:
            args.package = f"{project}"

        package_name = args.package
        package_version = f"{args.commit_short}-{platform}"

        print(f"Uploading: {args.path}")
        print(f"       as: {args.filename}.{ext}")

        upload_package(
            args.path,
            args.api_url,
            args.project_id,
            package_name,
            package_version,
            f"{args.filename}.{ext}",
            args.token,
             args.chunk,
        )

        return 0


COMMANDS = Publish
