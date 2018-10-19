from multiprocessing import Pool
import time


def fib(n):
    if n <= 2:
        return 1
    return fib(n-1) + fib(n-2)


def profile(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(end - start)
    return wrapper


@profile
def nomultiprocess():
    b = list(map(fib, [35]*5))
    print(f'no multiprocessing {b}')

@profile
def hasmultiprocess():
    pool = Pool(5)
    b = pool.map(fib, [35]*5)
    print(f'multiprocessing {b}')


nomultiprocess()
hasmultiprocess()
