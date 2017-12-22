#!/usr/bin/env python3        #跨平台注释
# -*- coding: utf-8 -*-       #中文支持注释

import scrapy


#抓取某人的所有粉丝的链接
class oschina1(scrapy.Spider):
    name = "oschina1"
    counter = 0
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
            r'https://my.oschina.net/javayou/fans?s=time&p=1',
        ]

        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        self.counter = self.counter + 1
        userlink = response.css("div.username a::attr('href')")
        for l in userlink:
            print(l.extract() + "\n")
            with open("z:/fans.txt", 'a') as f:  #a表示追加模式
                f.write(l.extract() + "\n")

        # if self.counter == 10:
        #     return

        if response.css('ul.paging li:last-child a::text').extract()[0] == "下一页":  #到达最后一页，下一步按钮会消失，下面的表达式会拿到最后一页url
            next_page = response.urljoin(response.css('ul.paging li:last-child a::attr("href")').extract()[0])
            yield scrapy.Request(next_page, headers=self.headers, callback=self.parse)