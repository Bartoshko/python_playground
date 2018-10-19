from multiprocessing import Pool
import time
import fib_c


def profile(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(end - start)

    return wrapper


@profile
def nomultiprocess():
    b = list(map(fib_c.calculate, [35] * 5))
    print(f'no multiprocessing {b}')


@profile
def hasmultiprocess():
    pool = Pool(5)
    b = pool.map(fib_c.calculate, [35] * 5)
    print(f'multiprocessing {b}')


nomultiprocess()
hasmultiprocess()
