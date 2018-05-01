# coro1.py
def foo():
    print('Hello')
    yield
    print('World')
    yield
    print('Bye')
    yield
    print('World')


# g = foo()
# next(g)
# next(g)
# next(g)
# next(g)
