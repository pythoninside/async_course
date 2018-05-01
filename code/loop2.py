# loop2.py
class Task:
    def __init__(self, coroutine):
        self.id = id(self)

        self._coroutine = coroutine

    def __next__(self):
        return self._coroutine.__next__()


def coro(name, n=10):
    i = 0
    while i < n:
        print(f'{name}: {i}')
        i += 1
        yield
    return n


if __name__ == '__main__':
    tasks = [Task(coro('foo')), Task(coro('bar', n=7))]
    while tasks:
        current = tasks.pop(0)
        try:
            next(current)
        except StopIteration:
            print(f'Task {current.id} done')
        else:
            tasks.append(current)
    print('All done')

    # What are the problems with this simple event loop?
    # - How does one get a hold of the result of a coroutine?
    # - How do we know when a coroutine is done?
    # - Can we mix sync and async code?
    # - 100% CPU usage
    # - Is round-robing the best scheduling?
    # - What about IO events (e.g., sockets)?
    # - Others?
