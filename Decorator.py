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
    print('Successful buy!')


@pwd
def sell():
    print('Successful sell!')


if __name__ == '__main__':
    # buy()
    sell()
