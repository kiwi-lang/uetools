import concurrent.futures


executor = concurrent.futures.ThreadPoolExecutor()


def poolexecutor():
    return executor


def submit(fun, *args):
    return poolexecutor().submit(fun, *args)


def as_completed(futures):
    return concurrent.futures.as_completed(futures)


def shutdown():
    executor.shutdown()
