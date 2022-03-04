import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

from data import get_list_of_domains
from matchrules.XpathCookieRule import XpathCookieRule


load_page_script="""
    function main(splash)
        assert(splash:go(splash.args.url))
        splash:wait(3)

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
        -- splash:wait(2))
        -- until( splash:select('[target]') ~= nil )

        return {html=splash:html()}
    end
"""

class PolicyCrawler(scrapy.Spider):
    name = "policies"
    maxdepth = 2
    start_urls = get_list_of_domains()[:50]
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
        self.rules = [
            XpathCookieRule,
        ]
        

    def start_requests(self): 
        splash_args = {
           'html': 1,
           'png': 1,
           'width': 600,
           'render_all': 1,
           'lua_source': load_page_script,
           'timeout': 90
        }
        # self.start_urls = ['cnn.com']
        for url in self.start_urls:
            yield SplashRequest("https://www."+url, self.parse, 
                endpoint='execute', 
                #args={'wait': 1}, 
                args=splash_args
           )
    def parse(self, response):
        key = response.url
        bannerHtml = self.runRules(response)
        
        if bannerHtml is not None and len(bannerHtml) > 0:
            self.data[key] = bannerHtml
        else:
            self.data[key] = "FTC"
            
    def runRules(self, response):
        i = 0
        res = "" 
        while i < len(self.rules) and len(res) == 0:
            rule = self.rules[i]()
            res = rule.extract(response)
            i+=1
        
        return res


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