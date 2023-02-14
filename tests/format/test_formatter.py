import os
import subprocess

folder = os.path.join(os.path.dirname(__file__), "samples")

import pytest

from uetools.format.base import Formatter
from uetools.format.cooking import CookingFormatter
from uetools.format.tests import TestFormatter

log_lines = """
LogWindows: Failed to load 'aqProf.dll' (GetLastError=126)
LogWindows: File 'aqProf.dll' does not exist
LogProfilingDebugging: Loading WinPixEventRuntime.dll for PIX profiling (from ../../../Engine/Binaries/ThirdParty/Windows/WinPixEventRuntime/x64).
LogConfig: Display: Loading HoloLens ini files took 0.02 seconds
LogConfig: Display: Loading Android ini files took 0.02 seconds
LogConfig: Display: Loading Unix ini files took 0.03 seconds
LogConfig: Display: Loading Windows ini files took 0.03 seconds
LogConfig: Display: Loading TVOS ini files took 0.03 seconds
LogConfig: Display: Loading Linux ini files took 0.03 seconds
LogConfig: Display: Loading LinuxArm64 ini files took 0.03 seconds
LogPluginManager: Mounting Engine plugin FastBuildController
"""

formatted = """
[  0][L][LogWindows              ] Failed to load 'aqProf.dll' (GetLastError=126)
[  0][L][LogWindows              ] File 'aqProf.dll' does not exist
[  0][L][LogProfilingDebugging   ] Loading WinPixEventRuntime.dll for PIX profiling (from ../../../Engine/Binaries/ThirdParty/Windows/WinPixEventRuntime/x64).
[  0][D][LogConfig               ]  Loading HoloLens ini files took 0.02 seconds
[  0][D][LogConfig               ]  Loading Android ini files took 0.02 seconds
[  0][D][LogConfig               ]  Loading Unix ini files took 0.03 seconds
[  0][D][LogConfig               ]  Loading Windows ini files took 0.03 seconds
[  0][D][LogConfig               ]  Loading TVOS ini files took 0.03 seconds
[  0][D][LogConfig               ]  Loading Linux ini files took 0.03 seconds
[  0][D][LogConfig               ]  Loading LinuxArm64 ini files took 0.03 seconds
[  0][L][LogPluginManager        ] Mounting Engine plugin FastBuildController
"""


def test_formatter(capsys):
    fmt = Formatter(24)

    for line in log_lines.split("\n"):
        fmt.match_regex(line)

    captured = capsys.readouterr()
    assert captured.out.strip() == formatted.strip()


@pytest.mark.skipif(os.name == "nt", reason="Not supported")
def test_formatter_cook(capsys, tmp_path):

    result = os.path.join(tmp_path, "output.txt")
    target = os.path.join(folder, "cooking_out.txt")
    input = os.path.join(folder, "cooking_in.txt")

    with open(input) as file:
        input = file.readlines()

    fmt = CookingFormatter(24)
    for line in input:
        fmt.match_regex(line)

    captured = capsys.readouterr()
    with open(result, "w") as file:
        file.write(captured.out)

    assert os.path.exists(result)
    assert os.path.exists(target)

    cmd = ["diff", "-Z", target, result]
    print(" ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", check=True)

    assert result.stdout == ""


@pytest.mark.skipif(os.name == "nt", reason="Not supported")
def test_formatter_test(capsys, tmp_path):
    result = os.path.join(tmp_path, "output.txt")
    target = os.path.join(folder, "tests_out.txt")
    input = os.path.join(folder, "tests_in.txt")

    with open(input) as file:
        input = file.readlines()

    fmt = TestFormatter(24)
    for line in input:
        fmt.match_regex(line)

    captured = capsys.readouterr()
    with open(result, "w") as file:
        file.write(captured.out)

    assert os.path.exists(result)
    assert os.path.exists(target)

    cmd = ["diff", "-Z", target, result]
    print(" ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", check=True)

    assert result.stdout == ""


sample = os.path.join(folder, "error_code.txt")


def test_formater_return_exit_code():
    with open(sample) as file:
        input = file.readlines()

    fmt = Formatter(24)
    for line in input:
        fmt.match_regex(line)

    assert fmt.returncode() == 139
