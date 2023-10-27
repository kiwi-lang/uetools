import pytest

from uetools.core.cli import args, main
from uetools.core.conf import load_conf, ready, save_conf

skipif = pytest.mark.skipif


# I dont want to run this test on my machine, but on the CI it is fine
@skipif(ready(), reason="Unreal engine is installed")
def test_init():
    previous_conf = load_conf()

    main(args("init", "--engine", "ENGINE_FOLDER_TEST", "--project", "PROJECT_FOLDER_TEST"))

    new_conf = load_conf()
    assert new_conf["engine_path"] == "ENGINE_FOLDER_TEST"
    assert new_conf["project_path"] == ["PROJECT_FOLDER_TEST"]

    save_conf(previous_conf)
