from uetools.core import args, main


def test_project_list(project):
    main(args("project", "list"))
