import os

from uetools.core.cli import args, main


def test_ubt_configure(monkeypatch, tmp_path):
    config = os.path.join(tmp_path, "BuildConfiguration.xml")
    monkeypatch.setattr(
        "uetools.commands.ubt.configure.get_ubt_configfile", lambda: config
    )

    main(args("ubt", "configure", "--list"))

    # Dry run so the configuration was not created
    main(args("ubt", "configure", "--dry", "ParallelExecutor.MaxProcessorCount=1"))
    assert not os.path.exists(config)

    # File was created
    main(args("ubt", "configure", "ParallelExecutor.MaxProcessorCount=2"))
    assert os.path.exists(config)

    with open(config) as file:
        assert "<MaxProcessorCount>2</MaxProcessorCount>" in file.read()

    # Value was updated
    main(args("ubt", "configure", "ParallelExecutor.MaxProcessorCount=4"))
    assert os.path.exists(config)

    with open(config) as file:
        assert "<MaxProcessorCount>4</MaxProcessorCount>" in file.read()
