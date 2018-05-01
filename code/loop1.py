# loop1.py
def coro(name, n=10):
    i = 0
    while i < n:
        print(f'{name}: {i}')
        i += 1
        yield
    return n


coros = [coro('foo'), coro('bar', n=7)]
while coros:
    current = coros.pop(0)
    try:
        next(current)
    except StopIteration:
        print('Coroutine done')
    else:
        coros.append(current)
print('All done')

# What are the problems with this simple event loop?
# - We have no way of referring to a given coroutine
# - How does one get a hold of the result of a coroutine?
# - How do we know when a coroutine is done?
# - Can we mix sync and async code?
# - 100% CPU usage
# - Is round-robing the best scheduling?
# - What about IO events (e.g., sockets)?
# - Others?
