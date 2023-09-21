import sys
import time
from contextlib import contextmanager

profile = dict()


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
        global timer_builder

        self.start = time.time()
        timer_builder.append(self)
        return self

    def __exit__(self, *args):
        global timer_builder
        self.end = time.time()
        self.timing = self.end - self.start

        if timer_builder:
            timer_builder.pop()

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


timer_builder = []
TimerGroup("root").__enter__(),


@contextmanager
def timeit(name):
    timer = timer_builder[-1]

    with timer.timeit(name) as timer:
        yield timer


def show_timings():
    if "-xyz" not in sys.argv:
        return

    print()
    print("Timings:")
    timer = timer_builder[0]
    timer.__exit__()
    timer.show()
