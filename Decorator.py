def pwd(order):
    def order_new():
        pwd = input('Please input the password:')
        if pwd == '123456':
            order()
        else:
            print('Wrong password!')
    return order_new


@pwd
def buy():
    print('Buy Successful!')


@pwd
def sell():
    print('Sell Successful!')


if __name__ == '__main__':
    # buy()
    sell()
