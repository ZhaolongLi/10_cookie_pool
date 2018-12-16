# coding:utf-8

import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from .config import *
from .db import RedisClient
from login.weibo.cookies import WeiboCookies


class CookiesGenerator(object):
    def __init__(self,website='default'):
        """
        父类，初始化一些对象
        :param website: 名称
        """
        self.website = website
        self.cookies_db = RedisClient('cookies',self.website)
        self.accounts_db = RedisClient('accounts',self.website)
        self.init_browser()

    def __del__(self):
        self.close()

    def init_browser(self):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :return:
        """
        self.browser = webdriver.Chrome()

    def new_cookies(self,username,password):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        # rasie NotImplementedError
        pass


    def process_cookies(self,cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    def run(self):
        """
        运行，得到所有账户，然后顺次模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.get_usernames()
        cookies_usernames = self.cookies_db.get_usernames()

        for username in accounts_usernames:
            if not username in cookies_usernames:
                password = self.accounts_db.get_value(username)
                print('正在生成Cookies','账号',username,'密码',password)
                result = self.new_cookies(username,password)
                # 成功获取
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('成功获取到Cookies',cookies)
                    if self.cookies_db.set(username,json.dumps(cookies)):
                        print('成功保存到Cookies')

                # 密码错误，移除账号
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                else:
                    print(result.get('content'))
            else:
                print('所有账号都已经成功获取Cookies')

    def close(self):
        """
        关闭
        :return:
        """
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')


class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self,website='weibo'):
        """
        初始化操作
        :param website: 站点名称
        """
        CookiesGenerator.__init__(self,website)
        self.website = website

    def new_cookies(self,username,password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和密码
        """
        return WeiboCookies(username,password,self.browser).main()


if __name__ == '__main__':
    generator = WeiboCookiesGenerator()
    generator.run()
