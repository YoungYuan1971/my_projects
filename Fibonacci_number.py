def fib(n):
    a, b = 0, 1
    fib_list = []

    for _ in range(n):
        a, b = b, a+b
        fib_list.append(a)

    print(fib_list)


if __name__ == '__main__':
    number = int(input('Please enter the number to generate: '))
    fib(number)
