import logging
import urllib

from pip._vendor import requests
import scrapy
import json
import re
import base64
import rsa
import binascii


logger = logging.getLogger('mycustomlogger')

#自己写的，结合scrapy的微博模拟登录，能登录成功
class WeiboSpider(scrapy.Spider):
    name = 'weibo'

    def start_requests(self):
        url = r'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

        servertime, nonce, pubkey, rsakv = self.getLoginInfo()
        su = self.getSu("xxxxxx@qq.com")
        sp = self.getSp("xxxxxxxxxxx", servertime, nonce, pubkey)
        pd = self.makeData(su, sp, servertime, nonce, rsakv)

        # self.logger.info("****************************")
        # self.logger.info(type(pd))
        # self.logger.info(len(pd))
        #
        # for key in pd:
        #     print(key)
        # self.logger.info("****************************")
        # for value in pd.values():
        #     print(value)
        #
        # self.logger.info(pd["entry"])
        # self.logger.info("****************************")

        return [scrapy.http.FormRequest(url, formdata=pd, callback=self.logged_in)]


    def getLoginInfo(self):
        #获取基础信息
        preLoginURL = r'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)'
        html = requests.get(preLoginURL).text
        jsonStr = re.findall(r'\((\{.*?\})\)', html)[0]
        data = json.loads(jsonStr)
        servertime = str(data["servertime"])
        nonce = data["nonce"]
        pubkey = data["pubkey"]
        rsakv = data["rsakv"]
        return servertime, nonce, pubkey, rsakv


    def getSu(self, username):
        """加密用户名，su为POST中的用户名字段"""
        su = base64.b64encode(username.encode('utf-8')).decode('utf-8')
        print("加密的username：" + su)
        return su


    def getSp(self, password, servertime, nonce, pubkey):
        # self.logger.info("-------------------password start-----------------------")
        # self.logger.info(password)
        # self.logger.info(servertime)
        # self.logger.info(nonce)
        # self.logger.info(pubkey)
        # self.logger.info("-------------------password end-----------------------")



        """加密密码，sp为POST中的用户名字段"""
        pubkey = int(pubkey, 16)
        key = rsa.PublicKey(pubkey, 65537)
        # 以下拼接明文从js加密文件中得到
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        message = message.encode('utf-8')
        sp = rsa.encrypt(message, key)
        # 把二进制数据的每个字节转换成相应的2位十六进制表示形式。
        sp = binascii.b2a_hex(sp)
        print("flag1")
        print("未加密的password：" + password)
        print("---------------------------------")
        return sp

    def makeData(self, su, sp, servertime, nonce, rsakv):
        postData = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            "pagerefer": "",
            "vsnf": "1",
            "su": su,
            "service": "miniblog",
            "servertime": servertime,
            "nonce": nonce,
            "pwencode": "rsa2",
            "rsakv": rsakv,
            "sp": sp,
            "sr": "1920*1080",
            "encoding": "UTF-8",
            "prelt": "277",
            "url": "http://open.weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "META",
        }
        return postData

    def logged_in(self, response):

        body = str(response.body)
        self.logger.info(body)
        pattern = re.compile(r'^(.*)retcode=0(.*)$')
        match = pattern.match(body)
        if match:
            self.logger.info("-------------------登录成功-----------------------")
        else:
            self.logger.info("-------------------登录失败-----------------------")

