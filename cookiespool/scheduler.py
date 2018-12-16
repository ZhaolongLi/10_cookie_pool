# coding:utf-8

import time
from multiprocessing import Process
from .api import app
from .config import *
from .generator import *
from .tester import *

class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        """
        Cookie检测
        :param cycle:
        :return:
        """
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
        """
        运行Web接口
        :return:
        """
        print('API接口开始运行')
        app.run(host=API_HOST,port=API_PORT)

    def run(self):
        """
        多进程调度器运行入口
        :return:
        """
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()