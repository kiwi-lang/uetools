import multiprocessing
import os
import re
import signal
import subprocess
import threading
import time
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass

from uetools.args.arguments import add_arguments
from uetools.args.command import Command, command_builder, newparser
from uetools.core.conf import WINDOWS, editor, find_project
from uetools.format.base import Formatter
from uetools.core.util import deduce_project


# fmt: off
@dataclass
class Arguments:
    """Launch unreal engine with mladapter setup"""
    resx                : int = 320     # resolution width
    resy                : int = 240     # resolution height
    fps                 : int = 20      # Max FPS
    windowed            : bool = True   # Window mode
    usefixedtimestep    : bool = True   # Block until the ML agent replies with an action
    game                : bool = True   #
    unattended          : bool = True   # Close when the game finishes
    onethread           : bool = False  # Run on a single thread
    reducethreadusage   : bool = False  #
    nosound             : bool = False  # Disable sound
    nullrhi             : bool = False  # Disable rendering
    deterministic       : bool = False  # Set seeds ?
    debug               : bool = False  #
    mladapterport       : int = 8123    # RPC server listen port
    stdout              : bool = True
    fullstdoutlogoutput : bool = True   # Print log to stdout
    utf8output          : bool = True   # --
    nosplash            : bool = True   # --
# fmt: on


SLEEP = 0.01


def build_command(args):
    args = vars(args)

    map = args.pop("map")
    project = args.pop("project")
    _ = args.pop("dry", False)

    project = find_project(project)

    # We found the project
    if project is not None:
        cmd = [editor(), project, map]

    # Assume the project is a path to the compiled project
    else:
        cmd = [project, map]

    cmd = cmd + command_builder(args)
    return cmd


def _process_kill(process):
    process.terminate()
    process.kill()

    # if WINDOWS:
    #    os.system(f"taskkill /F /PID {process.pid}")

    # else:
    #    process.send_signal(signal.SIGTERM)
    #    process.send_signal(signal.SIGKILL)

    # process.terminate()


def _process_interupt(process: multiprocessing.Process):
    process.terminate()
    process.kill()

    # #
    # if WINDOWS:
    #    # print(os.system(f"taskkill /F /PID {process.pid}"))
    #    signum = signal.CTRL_BREAK_EVENT
    # else:
    #    signum = signal.SIGINT

    # os.kill(process.pid, signum)


MAP_LOADED_CUE = re.compile(
    r"Took (?P<time>[0-9.]*) seconds to LoadMap\((?P<map>[A-Za-z\/]*)\)"
)

MLADAPTER_ENABLED_CUE = re.compile(
    r".*Creating MLAdapter manager of class (?P<class>[A-Za-z]*)"
)


class StartupLog(Formatter):
    def __init__(self, col=None) -> None:
        super().__init__(col)
        self.loaded = False
        self.mladapter = False
        # self.print = lambda *args, **kwargs: print("UE: ", *args, **kwargs)

    def format(
        self, datetime=None, frame=None, category=None, verbosity=None, message=None
    ):
        if MLADAPTER_ENABLED_CUE.search(message):
            self.mladapter = True

        if MAP_LOADED_CUE.search(message):
            self.loaded = True

        super().format(datetime, frame, category, verbosity, message)


_INIT = 0
_READY = 1
_STOP = 2


def _mp_worker(cmd, status, states, timeout=60):
    shell = True
    fmt = StartupLog()
    start = time.time()

    def read_output(process):
        while status.value != _STOP:
            try:
                line = process.stdout.readline()
                if len(line) > 0:
                    fmt.match_regex(line)
            except ValueError:
                if process.poll() is not None:
                    return
                raise

    def wait_ready(process, timeout):
        # Wait for UE to finish loading its stuff
        while (process.poll() is None) and (not fmt.loaded):
            if time.time() - start > timeout:
                raise TimeoutError("")

    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # This is needed because without lines might not be recognized as such
        text=True,
        shell=shell,
    ) as process:
        try:
            states["pid"] = process.pid
            states["status"] = "starting"

            stdout_reader = threading.Thread(target=read_output, args=(process,))
            stdout_reader.start()

            wait_ready(process, timeout=timeout)

            if fmt.loaded and not fmt.mladapter:
                raise RuntimeError("MLAdapter plugin is not enabled")

            states["status"] = "running"
            status.value = _READY

            while process.poll() is None:
                time.sleep(SLEEP)

                if status.value == _STOP:
                    states["status"] = "stopping"
                    _process_kill(process)
                    break

        except KeyboardInterrupt:
            states["status"] = "interrupted"

        states["status"] = "stopped"
        states["return_code"] = process.poll()
        return process.poll() + fmt.returncode()


class UnrealEngineProcess:
    def __init__(self, cmd, manager: multiprocessing.Manager, close) -> None:
        self.status = manager.Value("i", _INIT)
        self.states = manager.dict()
        self.close = close
        self.proc = multiprocessing.Process(
            target=_mp_worker, args=(cmd, self.status, self.states)
        )
        self.proc.start()

    def is_alive(self):
        return self.proc.is_alive()

    def interrupt(self):
        self.stop()

    def stop(self):
        if not self.proc.is_alive():
            return

        if self.states["status"] == "running":
            self.close()

        if WINDOWS:
            signum = signal.CTRL_BREAK_EVENT
        else:
            signum = signal.SIGINT

        pid = self.states["pid"]
        start = time.time()
        self.status.value = _STOP

        while self.proc.is_alive() and self.states["status"] == "running":
            try:
                os.kill(pid, signum)
            except SystemError:
                pass

            time.sleep(SLEEP)

            if time.time() - start > 30:
                raise RuntimeError("Could not shutdown UE")

        while self.proc.is_alive():
            time.sleep(0)

        print(f"Shutdown after {time.time() - start}")

    def join(self):
        self.proc.join()


def _ask_ue_to_exit(args):
    import socket

    from uetools.rl.client import Client

    def wrapper():
        try:
            client = Client(server_port=args.mladapterport, timeout=SLEEP)
            client.connect(timeout=SLEEP)
            client.add_functions()
            print(client.list_sensor_types())
            print(client.list_actuator_types())
            client.exit()
        except socket.timeout:
            pass

        except TimeoutError:
            pass

    return wrapper


@contextmanager
def unrealgame(args: Arguments):
    cmd = build_command(args)

    with multiprocessing.Manager() as manager:
        ue = UnrealEngineProcess(cmd, manager, _ask_ue_to_exit(args))

        # wait for UE to be ready
        while ue.is_alive() and ue.status.value != _READY:
            time.sleep(0)

        yield ue

        ue.stop()


class ML(Command):
    """Launch a game setup for machine learning

    Attributes
    ----------
    project: str
        Name of the the target to build (UnrealPak, RTSGame, RTSGameEditor, etc...)

    Examples
    --------

    .. code-block:: console

       uecli editor ml GamekitDev NewProjectTest

       # Launch your agent script that will connect and make the agents play the game

    """

    name: str = "ml"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, ML)
        parser.add_argument("map", type=str, help="Name of the map to open")
        parser.add_argument(
            "--project",
            type=str,
            help="Name of the the project to open",
            default=deduce_project(),
        )

        add_arguments(parser, Arguments)
        parser.add_argument(
            "--dry",
            action="store_true",
            default=False,
            help="Print the command it will execute without running it",
        )

    @staticmethod
    def execute(args):
        dry = vars(args).pop("dry")

        cmd = build_command(deepcopy(args))
        print(" ".join(cmd))

        if not dry:
            with unrealgame(args) as env:
                try:
                    # from uetools.core.client import Client

                    # client = Client(server_port=args.mladapterport, timeout=SLEEP)
                    # client.connect(timeout=SLEEP)
                    # client.add_functions()
                    # client.generate_methods()

                    while env.is_alive():
                        time.sleep(SLEEP)

                except KeyboardInterrupt:
                    env.interrupt()

        return 0


COMMANDS = ML
