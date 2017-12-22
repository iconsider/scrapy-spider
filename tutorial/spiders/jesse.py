import scrapy

class pachong(scrapy.Spider):
    name = "pachong"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        filename = 'test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
