#!/usr/bin/env python3        #跨平台注释
# -*- coding: utf-8 -*-       #中文支持注释

import scrapy


class oschinauser(scrapy.Item):
    u_id = scrapy.Field()
    u_name = scrapy.Field()
    u_post = scrapy.Field()
    u_address = scrapy.Field()
    u_signature = scrapy.Field()
    u_joindate = scrapy.Field()


class oschina(scrapy.Spider):
    name = "oschina"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Connection": "keep-alive",
        "Host": "my.oschina.net",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    }

    #当spider启动爬取并且未制定URL时，该方法被调用
    def start_requests(self):
        urls = [
            # r'https://my.oschina.net/xuwa/fans?s=time&p=1',
            r'https://my.oschina.net/javayou/fans?s=time&p=1',
            # r'https://my.oschina.net/huateng/fans?s=time&p=1',
            # r'https://my.oschina.net/u/152503/fans?s=time&p=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        userlink = response.css("div.username a::attr('href')")

        for l in userlink:
            fansurl = l.extract() + "/fans"
            print(fansurl)
            self.writedown(fansurl + "\n")
            yield scrapy.Request(l.extract() + "/home", headers=self.headers, callback=self.getinfo)  #url加上/home防止某些用户使用其他页面布局，如https://my.oschina.net/damihui
            yield scrapy.Request(fansurl, headers=self.headers, callback=self.parse)

        try:
            if response.css('ul.paging li:last-child a::text').extract()[0] == "下一页":  # 到达最后一页，下一步按钮会消失，但if里头的css选择器不会为空，为最后一页的url
                next_page = response.urljoin(response.css('ul.paging li:last-child a::attr("href")').extract()[0])
                yield scrapy.Request(next_page, headers=self.headers, callback=self.parse)
            else:
                return
        except IndexError:
            if len(userlink) == 0:
                print("子节点：" + response.url)
                self.writedown_nofans(response.url + "\n")
                return

    # 用于记录所有粉丝节点的link
    def writedown(self, data):
        with open("z:/oschina_allfans.txt", 'a') as f:
            f.write(data)


    # 用于记录所有粉丝为0的节点的link
    def writedown_nofans(self, data):
        with open("z:/oschina_nofans.txt", 'a') as f:
            f.write(data)

    # 用于记录所有粉丝节点的info
    def writedown_info(self, item):
        with open("z:/oschina_fansinfo.txt", 'a') as f:
            fansinfo = item["u_id"] + ";" + item["u_name"] + ";" + item["u_post"] + ";" + item["u_address"] + ";" + item["u_signature"] + ";" + item["u_joindate"] + "\n"
            f.write(fansinfo)

    def getinfo(self, response):
        item = oschinauser();

        item["u_id"] = response.url.replace(r"https://my.oschina.net/u/", r"").replace(r"https://my.oschina.net/", r"").replace(r"/home", r"")
        item["u_name"] = response.css("div[class='user-title flex-end'] span.nickname::text").extract()[0]
        try:
            item["u_post"] = response.css("div[class='user-title flex-end'] span.post::text").extract()[0]
        except:
            item["u_post"] = ""

        try:
            item["u_address"] = response.css("div[class='user-title flex-end'] span.address::text").extract()[0]
        except:
            item["u_address"] = ""

        #-1表示用户有自己的签名
        if response.css("div[class='user-signature'] span:first-child::text").extract()[0].find("很懒，签名啥也没写") == -1:
            item["u_signature"] = response.css("div[class='user-signature'] span:first-child::text").extract()[0]
        else:
            item["u_signature"] = ""

        item["u_joindate"] = response.css("div[class='user-score'] div[class='join-time text-muted']::text").extract()[0].replace(r"\n", "").strip()

        self.writedown_info(item)
        return