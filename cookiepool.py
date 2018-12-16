# coding:utf-8

import random
import redis

class RedisClient(object):
    def __init__(self,type,website,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param type:
        :param website:
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
        self.type = type
        self.website = website

    def get_name(self):
        """
        获取Hash的名称
        :return: Hash的名称
        """
        return "{type}:{website}".format(type=self.type,website=self.website)

    def set(self,username,value):
        """
        设置键值对
        :param username: 用户名
        :param value: 密码或者Cookies
        :return:
        """
        return self.db.hset(self.get_name(),username,value)

    def get_value(self,username):
        """
        根据键名获取键值
        :param username: 用户名
        :return:
        """
        return self.db.hget(self.get_name(),username)

    def delete(self,username):
        """
        根据键名删除键值对
        :param username: 用户名
        :return: 删除结果
        """
        return self.db.hdel(self.get_name(),username)

    def count(self):
        """
        获取数目
        :return: 数目
        """
        return self.db.hlen(self.get_name())

    def random_value(self):
        """
        随机得到键值，用于随机Cookies获取
        :return: 随机 Cookies
        """
        return random.choice(self.db.hvals(self.get_name()))

    def get_usernames(self):
        """
        获取所有账号信息
        :return: 所有用户名
        """
        return self.db.hkeys(self.get_name())

    def get_all(self):
        """
        获取所有键值对
        :return: 用户名和密码或Cookie的映射表
        """
        return self.db.hgetall(self.get_name())

    for username in accounts_usernames:
        if not username in cookies_usernames:
            password = self.accounts_db.get(username)
            print('正在生成Cookies','账号',username,'密码',password)
            result = self.new_cookies(username,password)

    def get_cookies(self):
        """
        获取Cookie
        :return:
        """
        return self.browser.get_cookies()

    def main(self):
        """
        主函数
        :return:
        """
        self.open()
        if self.password_error():
            return {
                'status':2,
                'content':'用户名或密码错误'
            }
        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status':1,
                'content':cookies
            }
        # 获取验证码图片
        image = self.get_image('captcha.png')
        numbers = self.detect_image(image)
        self.move(numbers)
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status':1,
                'content':cookies
            }
        else:
            return {
                'status':3,
                'content':'登录失败'
            }

        result = self.new_cookies(username,password)
        # 成功获取
        if result.get('status') == 1:
            cookies = self.process_cookies(result.get('content'))
            print('成功获取到Cookies',cookies)
            if self.cookies_db.set(username,json.dumps(cookies)):
                print('成功保存Cookies')
        # 密码错误，移除账号
        elif result.get('status') == 2:
            print(result.get('content'))
            if self.accounts_db.delete(username):
                print('成功删除账号')
        else:
            print(result.get('content'))


class ValidTester(object):
    def __init__(self,website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies',self.website)
        self.accounts_db = RedisClient('accounts',self.website)

    def test(self,username,cookies):
        """
        测试cookie是否有效
        :param username:
        :param cookies:
        :return:
        """
        raise NotImplementedError

    def run(self):
        """
        程序入口
        :return:
        """
        cookies_groups = self.cookies_db.all()
        for username,cookies in cookies_groups.items()
            self.test(username,cookies)



import json
import requests
from requests.exceptions import ConnectionError

class WeiboValidTester(ValidTester):
    def __init__(self,website='weibo'):
        ValidTester.__init__(self,website)

    def test(self,username,cookies):
        """
        重写父类的方法，测试
        :param username:
        :param cookies:
        :return:
        """
        print('正在测试Cookies','用户名',username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法',username)
            self.cookies_db.delete(username)
            print('删除Cookies',username)
            return

        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url,cookies=cookies,timeout=5,allow_redirects=False)
            if response.status_code == 200:
                print('Cookies有效',username)
                print('部分测试结果',response.text[0:50])
            else:
                print(response.status_code,response.headers)
                print('Cookies失效',username)
                self.cookies_db.delete(username)
                print('删除Cookies',username)
        except ConnectionError as e:
            print('发生异常',e.args)

    TEST_URL_MAP = {
        'weibo':'https://m.weibo.cn/'
    }



import json
from flask import Flask,g
app = Flask(__name__)
# 生成模块的配置字典
GENERATOR_MAP = {
    'weibo':'WeiboCookiesGenerator'
}
@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'

def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g,website):
            setattr(g,website + '_cookies',eval('RedisClient' + '("cookies","' + website + '")'))
    return g

@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookie,访问地址如/weibo/random
    :param website:
    :return:
    """
    g = get_conn()
    cookies = getattr(g,website + '_cookies').random()
    return cookies



import time
from multiprocessing import Process
from cookiespool.api import app
from cookiespool.config import *
from cookiespool.generator import *
from cookiespool.tester import *

class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Cookies检测进程开始运行')
            try:
                for website,cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        """
        产生Cookies
        :param cycle:
        :return:
        """
        while True:
            print('Cookies生成进程开始运行')
            try:
                for website,cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Cookies生成完成')
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API接口开始运行')
        app.run(host=API_HOST,port=API_PORT)

    def run(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()


# 产生模块类，如扩展其他站点，在此配置
GENERATOR_MAP = {
    'weibo':'WeiboCookiesGenerator'
}

# 测试模块类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'weibo':'WeiboValidTester'
}


# 产生模块开关
GENERATOR_PROCESS = True

# 验证模块开关
VALID_PROCESS = False

# 接口模块开关
API_PROCESS = True


