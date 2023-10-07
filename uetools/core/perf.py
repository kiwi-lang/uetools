import sys
import time
from contextlib import contextmanager
from collections import defaultdict
from threading import get_native_id

profile = dict()


def _append(timer):
    global timer_builder
    timer_builder[get_native_id()].append(timer)


def _pop():
    global timer_builder
    if timer_builder:
        timer_builder[get_native_id()].pop()


class TimerGroup:
    def __init__(self, name) -> None:
        self.start = None
        self.end = None
        self.name = name
        self.timing = None
        self.subgroups = dict()

    def latest(self):
        if self.end:
            return self.end - self.start

        return time.time() - self.start

    def __enter__(self):
        self.start = time.time()
        _append(self)
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.timing = self.end - self.start
        _pop()

    def show(self, depth=1):
        col = 40 - depth
        idt = depth * " "
        lsize = max(col - len(self.name), 0)
        sep = {0: "_", 1: ".", 2: " "}[depth % 3]

        print(f"{idt}{self.name} {sep * lsize} {self.latest():5.2f}")
        if len(self.subgroups) > 0:
            for _, v in self.subgroups.items():
                v.show(depth + 1)

    def timeit(self, name):
        timer = TimerGroup(name)
        self.subgroups[name] = timer
        return timer


timer_builder = defaultdict(list)


def _current():
    global timer_builder
    timerlist = timer_builder[get_native_id()]

    if len(timerlist) == 0:
        TimerGroup(f"root: {get_native_id()}").__enter__()

    return timerlist[-1]


@contextmanager
def timeit(name):
    timer = _current()

    with timer.timeit(name) as timer:
        yield timer


def show_timings():
    if "-xyz" not in sys.argv:
        return

    print()
    print("Timings:")

    for _, thread_group in timer_builder.items():
        timer = thread_group[0]
        try:
            timer.__exit__()
        except:
            pass
        timer.show()
        print("")
