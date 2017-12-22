#!/usr/bin/env python3        #跨平台注释
# -*- coding: utf-8 -*-           #中文支持注释

import io
import sys

import scrapy



class zhihu(scrapy.Spider):
    name = "zhihu"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "www.zhihu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
    }

    def start_requests(self):
        urls = [
            r'https://www.zhihu.com/people/liqing/followers?page=1',
        ]

        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)



    def parse(self, response):
        # str = response.body.decode('utf-8')
        print("*****************************")
        name = response.css(r'''span.ProfileHeader-name''')
        userlink = response.css(r'''div.ContentItem-head a.UserLink-link''')


        print(response.body.decode('utf-8'))
        for ul in userlink:
            pass
            # print(ul.extract() + "\n")
        print("*****************************")
