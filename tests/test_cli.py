import pytest

from uetools.core import args, main


def test_cli():
    with pytest.raises(SystemExit) as err:
        main(args("--help"))

    assert err.value.code == 0
