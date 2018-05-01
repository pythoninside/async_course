# coro2.py
def foo():
    print('Hello')
    yield
    print('World')
    yield
    print('Bye')
    yield
    print('World')
    return 42


# g = foo()
# while True:
#     try:
#         next(g)
#     except StopIteration as e:
#         print(f'Coroutine returned {e.value}')
#         break
