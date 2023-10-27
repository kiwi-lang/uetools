import sys
import time
from collections import defaultdict
from contextlib import contextmanager
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
        self.total = 0
        self.count = 0
        self.subgroups = dict()

    def latest(self):
        if self.end:
            return self.end - self.start

        return time.time() - self.start

    def __enter__(self):
        self.start = time.time()
        self.end = None
        _append(self)
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.timing = self.end - self.start
        self.total += self.timing
        self.count += 1
        _pop()

    def safe_total(self):
        return max(self.total, self.latest())

    def show(self, depth=1):
        col = 40 - depth
        idt = depth * " "
        lsize = max(col - len(self.name), 0)
        sep = {0: "_", 1: ".", 2: " "}[depth % 3]

        msg = f"{idt}{self.name} {sep * lsize} {self.latest():5.2f}"
        ext = " " * (15 + 6)
        if self.count > 1:
            ext = f"{self.total:5.2f} | {self.count:5d} | {self.total / self.count:5.2f}"

        explained = 0
        if len(self.subgroups) > 0:
            for _, v in self.subgroups.items():
                explained += v.safe_total()

        exp = ""
        if explained > 0:
            exp = f"{explained / self.safe_total() * 100:6.2f}"

        print(f"{msg} | {ext} | {exp}")

        if len(self.subgroups) > 0:
            for _, v in self.subgroups.items():
                v.show(depth + 1)

    def timeit(self, name):
        timer = self.subgroups.get(name)

        if timer is None:
            timer = TimerGroup(name)

        self.subgroups[name] = timer
        return timer


timer_builder = defaultdict(list)


def _current() -> TimerGroup:
    global timer_builder
    timerlist = timer_builder[get_native_id()]

    if len(timerlist) == 0:
        TimerGroup(f"root: {get_native_id()}").__enter__()

    return timerlist[-1]


def runtime():
    return _current().safe_total()


@contextmanager
def timeit(name):
    timer = _current()

    with timer.timeit(name) as timer:
        yield timer


def show_timings():
    if "-xyz" not in sys.argv:
        print(f"Runtime {runtime():5.2f} s")
        return

    print()
    print(f"{'Timings:':<40}  {'L (s)':>5} | {'T (s)':>5} | {'Count':>5} | {'T/C':>5} |")

    for _, thread_group in timer_builder.items():
        timer = thread_group[0]
        try:
            timer.__exit__()
        except:
            pass

        timer.show()
        print("")
