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
    result = func(100000000)
    print(result)
    print(time()-start_time)

# 不加速4.80, 加速0.05
