# loop4.py
import enum


class TaskState(enum.Enum):
    PENDING = 1
    RUNNING = 2
    DONE = 3


class Task:
    _all_tasks = set()

    def __init__(self, coroutine):
        self.id = id(self)
        Task._all_tasks.add(self)

        self._coroutine = coroutine
        self._callbacks = []

        self._state = TaskState.PENDING
        self.result = None
        self.exception = None

    def __next__(self):
        self._state = TaskState.RUNNING
        return self._coroutine.__next__()

    @classmethod
    def all_tasks(cls):
        return cls._all_tasks

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

    @property
    def done(self):
        return self._state is TaskState.DONE

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._state = TaskState.DONE
        self._result = value

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value):
        self._state = TaskState.DONE
        self._exception = value


def coro(name, n=10):
    i = 0
    while i < n:
        print(f'{name}: {i}')
        i += 1
        yield
    return n


def fail(n=10):
    i = 0
    while i < n:
        yield
        i += 1
    raise Exception('Done')


def mycallback(task):
    if task.exception:
        print(f'Task {task.id} raised {task.exception!r}')
    else:
        print(f'Task {task.id} result: {task.result}')


if __name__ == '__main__':
    tasks = [Task(coro('foo')), Task(coro('bar', n=7)), Task(fail(n=3))]
    for task in tasks:
        task.add_done_callback(mycallback)

    while tasks:
        current = tasks.pop(0)
        try:
            next(current)
        except StopIteration as e:
            current.result = e.value
        except Exception as e:
            current.exception = e
        else:
            tasks.append(current)
        finally:
            if current.done:
                for callback in current.done_callbacks:
                    callback(current)
    print('All done')

    # What are the problems with this simple event loop?
    # - Can we mix sync and async code?
    # - 100% CPU usage
    # - Is round-robing the best scheduling?
    # - What about IO events (e.g., sockets)?
    # - Others?
