def fib(n):
    a, b = 0, 1

    for _ in range(n):
        a, b = b, a+b
        yield a


if __name__ == '__main__':
    number = int(input('Please enter the number to generate: '))
    print(list(fib(number)))
