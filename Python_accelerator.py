from numba import jit
from time import time


@jit
def func(x):
    n = 0
    for i in range(x):
        n += i
    return n


if __name__ == "__main__":
    start_time = time()
    result = func(1000000000)
    print(result)
    print(time()-start_time)

# 不加速48.0, 加速0.10
