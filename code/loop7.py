# loop7.py
import enum
import time


_EVENT_LOOP = None


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


class Loop:
    def __init__(self):
        self._tasks = []
        self._stop = False

    def create_task(self, coroutine):
        if isinstance(coroutine, Task):
            return coroutine

        task = Task(coroutine)
        self._tasks.append(task)
        print(f'Added Task {task.id}')
        return task

    def remove(self, task):
        self.tasks.remove(task)

    def _stop_loop_cb(self, task):
        self._stop = True

    def run_until_complete(self, coroutine):
        task = self.create_task(coroutine)
        task.add_done_callback(self._stop_loop_cb)
        self.run_forever()
        task.remove_done_callback(self._stop_loop_cb)
        return task.result

    def run_forever(self):
        self._stop = False              # Just in case we are restarted

        while not self._stop:
            if not self._tasks:
                continue

            current = self._tasks.pop(0)
            try:
                next(current)
            except StopIteration as e:
                current.result = e.value
            except Exception as e:
                current.exception = e
                print(f'Warning: Task {current.id} raised {e!r}')
            else:
                self._tasks.append(current)
            finally:
                if current.done:
                    for callback in current.done_callbacks:
                        callback(current)


class Future:
    def __init__(self):
        self.result = None
        self._stop = False

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value
        self._stop = True

    def __iter__(self):
        while not self._stop:
            yield
        return self.result


def get_event_loop():
    global _EVENT_LOOP

    if _EVENT_LOOP is None:
        _EVENT_LOOP = Loop()
    return _EVENT_LOOP


def wait(coroutines, loop=None):
    # Schedule all coroutines with the event loop BUT add a callback to each
    # of them that keeps track of how many coroutines have finished vs how
    # many were started. When all coroutines are done, quit
    if loop is None:
        loop = get_event_loop()

    counter = len(coroutines)
    fut = Future()

    def _callback(task):
        nonlocal counter

        counter -= 1
        if counter == 0:
            fut.result = True

    tasks = []
    for coro in coroutines:
        task = loop.create_task(coro)
        task.add_done_callback(_callback)
        tasks.append(task)

    # fut acts as a "syncronization barrier" with the help of _callback.
    # yield from is a shorthand for "fut = iter(fot); while True: next(fut)"
    yield from fut

    for task in tasks:
        task.remove_done_callback(_callback)
    return tasks


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


def blocking():
    yield
    time.sleep(5)


def mycallback(task):
    if task.exception:
        print(f'Task {task.id} raised {task.exception!r}')
    else:
        print(f'Task {task.id} result: {task.result}')


def spawner(task):
    if task.exception:
        print(f'Task {task.id} raised {task.exception!r}')
    else:
        print(f'Task {task.id} result: {task.result}')

    # Twist
    loop = get_event_loop()
    task = loop.create_task(coro('baz', n=2))
    task.add_done_callback(mycallback)
    print(f'Spawned Task {task.id}')


if __name__ == '__main__':
    loop = get_event_loop()

    task = loop.create_task(coro('foo'))
    task.add_done_callback(mycallback)

    task = loop.create_task(coro('bar', n=7))
    task.add_done_callback(mycallback)

    task = loop.create_task(fail(n=3))
    task.add_done_callback(spawner)

    loop.run_forever()
    print('All done')

    # What are the problems with this simple event loop?
    # - What is the role of callbacks?
    # - 100% CPU usage
    # - Is round-robing the best scheduling?
    # - What about IO events (e.g., sockets)?
    # - Others?
