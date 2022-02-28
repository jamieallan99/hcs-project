import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

from data import get_list_of_domains

load_page_script="""
    function main(splash)
        assert(splash:go(splash.args.url))
        splash:wait(5)

        function wait_for(splash, condition)
            while not condition() do
                splash:wait(0.5)
            end
        end

        local result, error = splash:wait_for_resume([[
            function main(splash) {
                setTimeout(function () {
                    splash.resume();
                }, 5000);
            }
        ]])

        wait_for(splash, function()
            return splash:evaljs("document.querySelector('[target]') != null")
        end)

        -- repeat
        -- splash:wait(5))
        -- until( splash:select('[target]') ~= nil )

        return {html=splash:html()}
    end
"""

class PolicyCrawler(scrapy.Spider):
    name = "policies"
    maxdepth = 2
    start_urls = get_list_of_domains()[:27]#  [ 'http://google.com', 'http://facebook.com']
    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.output_callback = kwargs.get('args').get('callback')

    def start_requests(self): 
        splash_args = {
           'html': 1,
           'png': 1,
           'width': 600,
           'render_all': 1,
           'lua_source': load_page_script
        }
        for url in self.start_urls:
            yield SplashRequest("http://www."+url, self.parse, 
                endpoint='execute', 
                #args={'wait': 1}, 
                args=splash_args
           )
    def parse(self, response):

        html = response._body.decode("utf-8") 
        #print(html)

        key = response.url
        item1 = response.xpath("//div[contains(.//text(), 'cookie')]/../..").get()
        item2 = response.xpath("//p[contains(.//text(), 'cookie')]/../..").get()
        item3 = response.xpath("//span[contains(.//text(), 'cookie')]/../..").get()
        
        item2_or_3 = item2 if item2 else item3
        self.data[key] = item1 if  item1 else item2_or_3
        # for page in response.css('title::text').getAll():
        #     self.data.append(page.get())
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
            'USER_AGENT': "Chrome/98.0.4758.102"
        })

    def yield_output(self, data):
        self.output = data

    def crawl(self, cls):
        self.process.crawl(cls, args={'callback': self.yield_output})
        self.process.start()    