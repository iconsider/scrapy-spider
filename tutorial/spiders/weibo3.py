import json
import re
import base64
import rsa
import binascii

from pip._vendor import requests

#模拟登录
def getLoginInfo():
    #获取基础信息
    preLoginURL = r'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)'
    html = requests.get(preLoginURL).text
    jsonStr = re.findall(r'\((\{.*?\})\)', html)[0]
    data = json.loads(jsonStr)
    servertime = data["servertime"]
    nonce = data["nonce"]
    pubkey = data["pubkey"]
    rsakv = data["rsakv"]
    return servertime, nonce, pubkey, rsakv


def getSu(username):
    """加密用户名，su为POST中的用户名字段"""
    su = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    print("flag1")
    print("加密的username：" + su)
    print("---------------------------------")
    return su


def getSp(password, servertime, nonce, pubkey):
    print("************password****************")
    print(password)
    print(servertime)
    print(nonce)
    print(pubkey)
    print("**************password**************")

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

def login(su, sp, servertime, nonce, rsakv):
    postData = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        "pagerefer": "http://open.weibo.com/wiki/2/statuses/home_timeline",
        "vsnf": "1",
        "su": su,
        "service": "miniblog",
        "servertime": servertime,
        "nonce": nonce,
        "pwencode": "rsa2",
        "rsakv": rsakv,
        "sp": sp,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "prelt": "126",
        "url": "http://open.weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
        "returntype": "META",
    }
    loginURL = r'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

    # print("****************************")
    # for key in postData:
    #     print(key)
    # print("****************************")
    # for value in postData.values():
    #     print(value)
    # print("****************************")


    session = requests.Session()
    res = session.post(loginURL, data=postData)
    html = res.content.decode('gbk')
    print(html)
    info = re.findall(r"location\.replace\(\'(.*?)\'", html)[0]
    if 'retcode=0' in info:
        print("登录成功！")
    else:
        print("登录失败！")   #登录失败的时候代码会有点问题
    return session

if __name__ == '__main__':
    servertime, nonce, pubkey, rsakv = getLoginInfo()
    su = getSu("331072550@qq.com")
    # su = getSu("xxxxxxxxxxxxxx")
    sp = getSp("Lmlmd312068", servertime, nonce, pubkey)
    session = login(su, sp, servertime, nonce, rsakv)