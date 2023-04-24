# 函数作为装饰器
def pwd(order):
    def order_new():
        pwd = input('Please input the password:')
        if pwd == '123456':
            order()
        else:
            print('Wrong password!')
    return order_new


# 类作为装饰器
class Pwd:
    def __init__(self, f):
        self.f = f

    def __call__(self):
        pwd = input('Please input the password:')
        if pwd == '123456':
            self.f()
        else:
            print('Wrong password!')


@Pwd
def buy():
    print('Buy Successful!')


@Pwd
def sell():
    print('Sell Successful!')


if __name__ == '__main__':
    # buy()
    sell()
