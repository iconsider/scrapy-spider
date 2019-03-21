import io
import re
import sys

from scrapy.selector import Selector

import scrapy


#手工用cookie登录，能拿到用户详细页，但由于内容在script内，无法准确拿到对应的用户数据
class weibotest(scrapy.Spider):
    name = 'weibotest'
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码

    def start_requests(self):  # 当spider启动爬取并且未制定start_urls时，该方法被调用。
        urls = [
            "http://weibo.com/p/1005055123831506/info?mod=pedit_more",
            # "http://weibo.com/p/1005056138215337/info?mod=pedit_more",
            # "http://weibo.com/p/1005055115485942/info?mod=pedit_more",
        ]

        cookie = {
            "SINAGLOBAL": "2726683001650.3564.1480943310037",
            "_s_tentry": "login.sina.com.cn",
            "Apache": "3648376911913.9355.1493251940799",
            "ULV": "1493251940877:148:41:20:3648376911913.9355.1493251940799:1493251884832",
            "login_sid_t": "e88f3c464e650eb52b9555a67944f1f7",
            "UOR": ",,login.sina.com.cn",
            "SCF": "AmIFSKpOY6j15cYEB17AAYjsvxXVGdZam6QhbjtyljHdm3oD9L-xmIqULgk_kUteYw-AVjn99oJiQw7WPplaItA.",
            "SUB": "_2A250Bmp_DeThGeVL7FYU8inOyDiIHXVXcty3rDV8PUNbmtBeLUvdkW-PaBwIsPrjG963Y6nYBVrVT3CXSw..",
            "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5eqV82aVM0koq5nCeHaPWD5JpX5K2hUgL.FoefS0BfeoMEe0B2dJLoIEBLxK-LBo5L12qLxK-L1hnL1KnLxK-L1hqLBozLxK-L1hqLBozt",
            "SUHB": "0oU4EuHyweD1ks",
            "ALF": "1524845998",
            "SSOLoginState": "1493309999",
            "un": "xxxxxxxxxxxxx@qq.com",
            "wvr": "6",
        }

        for url in urls:
            yield scrapy.Request(url=url, cookies=cookie, callback=self.parse)

    def parse(self, response):

        print("--------------------------------------------")

        #消除一些转义字符，例如换行符
        s1 = response.body.decode().replace(r'\"', r'"')\
            .replace(r'\/', r'/').replace(r'\r\n', r'')\
            .replace(r'\n', r'').replace(r'\t', r'').replace(r'<!--//模块-->', r'')\


        p = re.compile(r'<script>.*</script>')
        script_set = p.findall(s1)

        data = ""
        print("\n**************************")
        for s in script_set:
            s = s.replace(r'<script>FM.view({', r'{').replace(r'})</script>', r'}').replace(r'});</script>', r'}')
            # print(s)
            # print("\n**************************")
            try:
                di = eval(s)
                print(len(di))
                # print(di["html"])
                for d in di:
                    print(d)
                    print("\n")
                print("\n**************************")
            except:
                continue





        # selector = Selector(data)

        print("--------------------------------------------")


    def formatBody(self, resposne):
        pass
