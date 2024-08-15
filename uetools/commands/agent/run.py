import os
import multiprocessing
from dataclasses import dataclass
import subprocess
import time
import threading
import traceback

import psutil
from argklass.command import Command


class RunAgent(Command):
    """Launch an unreal engine server

    Attributes
    ----------
    game: str
        Path to the executable

    Examples
    --------

    .. code-block:: console

       uecli agent run U:/Games/MyServer/Windows/v2.0/MyServer.exe

    """

    name: str = "run"

    @dataclass
    class Arguments:
        # fmt: off
        game: str               # Path to game server executable
        join: bool = False      # Wait for the server to end
        stop: bool = False      # Kill all servers before starting a new one
        log: str = None         # Path to server log
        port: int = 7777
        # fmt: on

    def execute(self, args: Arguments):
        # Note: this does not ensure that the server will keep running
        # we could do that in the server itself
        # where the server would kick all players and start a new game
        cwd = os.path.abspath(os.getcwd())

        log = f"{cwd}/server.log"
        if args.log is not None:
            log = args.log
    
        cmd = [
            args.game,
            "-fullstdoutlogoutput",
            "-utf8output",
            "-server",
            "-fps=30",
            # "-seconds=0.03",
            f"-abslog={log}",
            f"-port={args.port}"
        ]

        if args.stop:
            StopAgent().execute(args)

        manager = multiprocessing.Manager()
        p = UnrealEngineProcess(manager, cmd)
        time.sleep(10)

        if args.join:
            p.join()
        else:
            print()
            print("Detach... server will still be running")
            p.detach()

        return 0


class StopAgent(Command):
    """Stop an unreal engine server

    Attributes
    ----------
    game: str
        Name of the executable

    Examples
    --------

    .. code-block:: console

       uecli agent stop MyServer.exe

    """
    name: str = "stop"

    @dataclass
    class Arguments:
        # fmt: off
        game: str   # Path to game server executable
        # fmt: on
    
    def execute(self, args: Arguments):
        exec = os.path.split(args.game)[-1]
        for proc in psutil.process_iter(['pid', 'name', "exe"]):
            if proc.name().startswith(exec):
                print(f"Killing {proc.pid}: {proc.name()}")
                proc.kill()


INIT = 0
RUNNING = 1
STOPPED = 2
EXIT = 3

class Worker:
    def __init__(self, cmd, status, states, timeout) -> None:
        self.cmd = cmd
        self.status = status
        self.states = states
        self.timeout = timeout
        self.process = None

    def alive(self):
        return (self.process is not None) and (self.process.poll() is None) and (self.status.value != STOPPED)

    def read_output(self, stream):
        # This can hangs if unreal engine is not CLOSING
        while self.alive():
            try:
                stream.seek(0, os.SEEK_END)
                size = stream.tell()
                stream.seek(0, os.SEEK_CUR)

                if size > 0:
                    line = stream.readline()
                    if len(line) > 0:
                        print("UE: ", line, end="")
            except ValueError:
                pass
            except KeyboardInterrupt:
                print("received KB Interrupt")

    def kill(self):
        try:
            p = psutil.Process(self.process.pid)
            for c in p.children(recursive=True):
                c.kill()
        except psutil.NoSuchProcess:
            pass

    def show_children(self):
        p = psutil.Process(self.process.pid)
        print(">>>")
        for child in p.children(recursive=True):
            try:
                print(f" {child.name()}: {child.pid}")
                print(f"   - {child.exe()}")
            except Exception:
                traceback.print_exc()
        print("<<<")

    def run(self):
        with subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True,
            ) as process:
            self.process = process
            self.status.value = RUNNING
           

            stdout_reader = threading.Thread(target=self.read_output, args=(process.stdout,))
            stdout_reader.start()
            
            first_kill = None
            kill_count = 0
            while process.poll() is None:
                try:
                    time.sleep(0.1)

                    if self.status.value == EXIT:
                        # this process but leave unreal engine running
                        if not first_kill:
                            self.show_children()
                            first_kill = time.time()

                        process.kill()

                    if self.status.value == STOPPED:
                        if not first_kill:
                            print("Received kill message")
                            first_kill = time.time()
                        
                        self.kill()
                        kill_count += 1

                        if (kill_count + 1) % 100 == 0:
                            print(f"Still alive after {kill_count}")

                except Exception:
                    import traceback
                    traceback.print_exc()
                    self.status.value = STOPPED
        
            if first_kill:
                print(f"Killed after {time.time() - first_kill:.2f} s rc: {process.poll()} pid:{process.pid}")

            # if this hangs it is because the game is not closing
            stdout_reader.join()


def _worker(*args, **kwargs):
    w = Worker(*args, **kwargs)
    w.run()


class UnrealEngineProcess:
    """Launch UnrealEngine in its own process"""
    def __init__(self, manager, cmd) -> None:
        self.status = manager.Value("i", INIT)
        self.states = manager.dict()
        self.proc = multiprocessing.Process(
            target=_worker, args=(cmd, self.status, self.states, 60)
        )
        self.proc.start()

        while self.status.value == INIT:
            time.sleep(0.1)

    def detach(self):
        self.status.value = EXIT
        self.proc.join()

    def join(self):
        self.proc.join()

    def kill(self):
        self.status.value = STOPPED
        self.proc.join()

COMMANDS = [
    RunAgent,
    StopAgent,
]