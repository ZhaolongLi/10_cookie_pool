# coding:utf-8

# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码
REDIS_PASSWORD = None

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，可在此配置
GENERATOR_MAP = {
    'weibo':'WeiboCookiesGenerator'
}

# 测试模块类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'weibo':'WeiboValidTester'
}

TEST_URL_MAP = {
    'weibo':'https://m.weibo.cn/'
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和接口
API_HOST = '127.0.0.1'
API_PORT = 5000

# 产生模块开关
GENERATOR_PROCESS = True

# 验证模块开关
VALID_PROCESS = False

# 接口模块开关
API_PROCESS = True
