# loop3.py
import enum


class TaskState(enum.Enum):
    PENDING = 1
    RUNNING = 2
    DONE = 3


class Task:
    def __init__(self, coroutine):
        self.id = id(self)

        self._coroutine = coroutine
        self._callbacks = []

    def __next__(self):
        self._state = TaskState.RUNNING
        return self._coroutine.__next__()

    def add_done_callback(self, callback):
        if callable(callback):
            self._callbacks.append(callback)
        else:
            raise TypeError('Expecting a callable')

    def remove_done_callback(self, callback):
        self._callbacks.remove(callback)

    @property
    def done_callbacks(self):
        return self._callbacks


def coro(name, n=10):
    i = 0
    while i < n:
        print(f'{name}: {i}')
        i += 1
        yield
    return n


def mycallback(task):
    print(f'Task {task.id} done')


if __name__ == '__main__':
    tasks = [Task(coro('foo')), Task(coro('bar', n=7))]
    for task in tasks:
        task.add_done_callback(mycallback)

    while tasks:
        current = tasks.pop(0)
        try:
            next(current)
        except StopIteration:
            for callback in current.done_callbacks:
                callback(current)
        else:
            tasks.append(current)
    print('All done')

    # What are the problems with this simple event loop?
    # - How does one get a hold of the result of a coroutine?
    # - Can we mix sync and async code?
    # - 100% CPU usage
    # - Is round-robing the best scheduling?
    # - What about IO events (e.g., sockets)?
    # - Others?
