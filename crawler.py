import scrapy
from scrapy.crawler import CrawlerProcess

class PolicyCrawler(scrapy.Spider):
    name = "policies"
    maxdepth = 2
    start_urls = [ 'http://google.com', 'http://facebook.com']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.output_callback = kwargs.get('args').get('callback')

    def parse(self, response):
        depth = 0

        if 'depth' in response.meta:
            depth = response.meta['depth']

        for page in response.css('body'):
            if depth < self.maxdepth:
                a_selectors = response.xpath("//a")
                for selector in a_selectors:
                    # Extract the link text
                    text = selector.xpath("text()").extract_first()
                    # Extract the link href
                    link = selector.xpath("@href").extract_first()
                    # Create a new Request object
                    request = response.follow(link, callback=self.parse)
                    # Return it thanks to a generator
                    request.meta['depth'] = depth + 1
                    if str(link).count("policies"):
                        yield request
            self.data.append(page.extract())
        # if you wanna extract more than whole body
        # for title in response.css('h2.entry-title'):
        #     yield {'title': title.css('a ::text').extract_first()}

        # for next_page in response.css('div.prev-post > a'):
        #     yield response.follow(next_page, self.parse)


    def close(self, spider, reason):
        self.output_callback(self.data)


class Crawler:

    def __init__(self):
        self.output = None
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

    def yield_output(self, data):
        self.output = data

    def crawl(self, cls):
        self.process.crawl(cls, args={'callback': self.yield_output})
        self.process.start()    