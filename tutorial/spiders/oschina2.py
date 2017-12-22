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


#抓取某人的个人信息
class oschina2(scrapy.Spider):
    name = "oschina2"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Connection": "keep-alive",
        "Host": "my.oschina.net",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    }

    def start_requests(self):
        urls = [
            r'https://my.oschina.net/u/3388869',
            r'https://my.oschina.net/u/3453522',
            r'https://my.oschina.net/u/3448296',
            r'https://my.oschina.net/u/3448080',
            r'https://my.oschina.net/u/3448068',
            r'https://my.oschina.net/u/2346353',
        ]

        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = oschinauser();
        # print(response.url.replace(r"https://my.oschina.net/u/", r""))
        # print(response.css("div[class='user-title flex-end'] span.nickname::text").extract()[0])
        # print(response.css("div[class='user-title flex-end'] span.post::text").extract()[0])
        # print(response.css("div[class='user-title flex-end'] span.address::text").extract()[0])
        # print(response.css("div[class='user-signature'] span:first-child::text").extract()[0])
        # print(response.css("div[class='user-score'] div[class='join-time text-muted']::text").extract()[0].replace(r"\n", "").strip())





        item["u_id"] = response.url.replace(r"https://my.oschina.net/u/", r"")
        item["u_name"] = response.css("div[class='user-title flex-end'] span.nickname::text").extract()[0]
        try:
            item["u_post"] = response.css("div[class='user-title flex-end'] span.post::text").extract()[0]
        except:
            item["u_post"] = ""

        try:
            item["u_address"] = response.css("div[class='user-title flex-end'] span.address::text").extract()[0]
        except:
            item["u_address"] = ""

        item["u_signature"] = response.css("div[class='user-signature'] span:first-child::text").extract()[0]
        item["u_joindate"] = response.css("div[class='user-score'] div[class='join-time text-muted']::text").extract()[0].replace(r"\n", "").strip()
        print(item)
        print("---")


