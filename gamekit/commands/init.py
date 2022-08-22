import os

from gamekit.conf import load_conf, save_conf, CONFIG, CONFIGNAME, Command


class Init(Command):
    """Initialize the configuration file for the command line interface"""

    name: str = "init"

    @staticmethod
    def arguments(subparsers):
        init = subparsers.add_parser(Init.name, help='Initialize engine location')
        init.add_argument('--engine', default=None, type=str, help='path to the engine folder')
        init.add_argument('--projects', default=None, type=str, help='path to your projects folder')

    @staticmethod
    def execute(args):
        config = os.path.join(CONFIG, CONFIGNAME)
        conf = dict()

        default_engine = '/UnrealEngine/Engine'
        default_project = os.path.abspath(os.path.join('..', default_engine))

        if os.path.exists(config):
            conf = load_conf()
            default_engine = conf.get('engine_path', default_engine)
            default_project = conf.get('project_path', default_project)

        if args.engine is None:
            engine_path = input(f'Engine Folder [{default_engine}]: ')
        else:
            engine_path = args.engine

        if args.projects is None:
            project_folders = input(f'Project Folder [{default_project}]: ')
        else:
            project_folders = args.projects

        engine_path = engine_path or default_engine
        project_folders = project_folders or default_project

        conf['engine_path'] = engine_path
        conf['project_path'] = project_folders

        save_conf(conf)
        print(f'Updated Engine paths inside `{config}`')


COMMAND = Init
