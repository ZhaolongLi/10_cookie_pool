# coding:utf-8

from .db import RedisClient


conn = RedisClient('accounts','weibo')

def set(account,sep='----'):
    """
    录入账号信息
    :param account:
    :param sep:
    :return:
    """
    username,password = account.split(sep)
    result = conn.set(username,password)
    print('账号',username,'密码',password)
    print('录入成功' if result else '录入失败')

def scan():
    """
    交互输入
    :return:
    """
    print('请输入账号和密码，中间以"----"断开，输入exit退出')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)

if __name__ == '__main__':
    scan()
