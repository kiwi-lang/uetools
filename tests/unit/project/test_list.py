from uetools.core.cli import args, main


def test_project_list(project):
    main(args("project", "list"))
