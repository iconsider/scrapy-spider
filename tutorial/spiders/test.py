import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes1"
    #allowed_domains = ["toscrape.com"]
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
            yield item

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)  #返回一个绝对路径的url
            yield scrapy.Request(next_page, callback=self.parse)


