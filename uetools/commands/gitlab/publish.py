from dataclasses import dataclass
import json
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


class Publish(Command):
    """Publish a gitlab package to the registry"""

    name: str = "publish"

    @dataclass
    class Arguments:
        filename: str
        project: str = deduce_project()  # project's name
        platform: str = platform_choice()
        chunk: int = 1024

    @staticmethod
    def execute(args):
        project_path = find_project(args.project)
        project_name = os.path.basename(project_path)[:-9]

        project = project_name
        platform = args.platform

        file_path: str = args.filename
        chunk_size = args.chunk

        # fmt: off
        api_url      = os.getenv("CI_API_V4_URL")
        project_id   = os.getenv("CI_PROJECT_ID")
        commit_tag   = os.getenv("CI_COMMIT_TAG")
        commit_short = os.getenv("CI_COMMIT_SHORT_SHA")
        token        = os.getenv("CI_JOB_TOKEN")
        # fmt: on

        ext = file_path.rsplit(".", maxsplit=1)[1]

        package_name = f"{project}"
        package_version = f"{platform}-{commit_short}"
        filename = f"{project}-{commit_tag}.{ext}"

        # PUT /projects/:id/packages/generic/:package_name/:package_version/:file_name?status=:status
        url = f"{api_url}/projects/{project_id}/packages/generic/{package_name}/{package_version}/{filename}"

        headers = {"JOB-TOKEN": token}

        file_size = pathlib.Path(file_path).stat().st_size

        def bar():
            return tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

        with open(file_path, "rb") as file:
            with bar() as pbar:
                response = requests.put(url, headers=headers, data=file, stream=True)

                for data in response.iter_content(chunk_size=chunk_size):
                    pbar.update(len(data))

        if response.status_code == 200:
            return 0

        print(response.text)
        return -1


COMMANDS = Publish
