# coding:utf-8

import random
import redis
from .config import *

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

if __name__ == '__main__':
    conn = RedisClient('accounts','weibo')
    result = conn.set('hello','sss3s')
    print(result)
