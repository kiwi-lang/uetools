import os

from uetools.core import args, main

samples = os.path.join(os.path.dirname(__file__), "format", "samples")


def test_fmt_cooking():
    main(
        args(
            "format",
            "--profile",
            "cooking",
            "--file",
            os.path.join(samples, "cooking_in.txt"),
        )
    )


def test_fmt_tests():
    main(
        args(
            "format",
            "--profile",
            "tests",
            "--file",
            os.path.join(samples, "tests_in.txt"),
        )
    )
