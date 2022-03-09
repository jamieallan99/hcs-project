import base64
from email import header
from multiprocessing.connection import wait
from wsgiref import headers
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

from data import get_list_of_domains
from matchrules.XpathCookieRule import XpathCookieRule
from matchrules.CookieIdRule import CookieIdRule
from matchrules.OneTrustSdkRule import OneTrustSdkRule
from matchrules.CookieClassRule import CookieClassRule

load_page_script="""
    function main(splash)
        assert(splash:go(splash.args.url))
        assert(splash:wait(3))
        return {html=splash:html()}
    end
"""

class PolicyCrawler(scrapy.Spider):
    name = "policies"
    maxdepth = 2
    start_urls = get_list_of_domains()[:10]
    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
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
            CookieIdRule, 
            OneTrustSdkRule,
            CookieClassRule  
        ]
        self.crawled_sucess = 0
        self.ftc_count = 0
        self.parsed_domains = set()

    def start_requests(self): 
        splash_args = {
            'html': 1,
            'png': 1,
            'timeout': 200,
            'width': 1024,
            'wait': 10,
        }
        headers = {'User-Agent': 'my-test-banner-app'}
        for url in self.start_urls:
            domain = url.split('.')[0]
            top_level_domain = url.split('.')[-1]
            if domain not in self.parsed_domains and top_level_domain in ['com', 'uk', 'edu']:
                self.parsed_domains.add(domain)
                yield SplashRequest("https://"+url, self.parse, 
                    endpoint='render.json', 
                    args=splash_args,
                    headers=headers
                )

    def parse(self, response):
        key = response.url
        bannerHtml = self.runRules(response)
        
        if bannerHtml is not None and len(bannerHtml) > 0:
            self.crawled_sucess+=1
            self.data[key] = bannerHtml
        else:
            self.ftc_count+=1
            self.data[key] = "FailedToFindBanner"
        png = base64.b64decode(response.data['png'])
        filename = f'images/{response.url.strip("htps:/w.").split(".")[0]}.png'
        with open(filename, 'wb') as f:
            f.write(png)
            
    def runRules(self, response):
        i = 0
        res = "" 
        while i < len(self.rules) and len(res) == 0:
            rule = self.rules[i]()
            res = rule.extract(response)
            i+=1
        
        return res


    def close(self, spider, reason):
        print(f"Succefully extracted {self.crawled_sucess}")
        print(f"Failed to extact banner from {self.ftc_count} sites")
        self.output_callback(self.data)


class Crawler:

    def __init__(self):
        self.output = None
        self.process = CrawlerProcess()

    def yield_output(self, data):
        self.output = data

    def crawl(self, cls):
        self.process.crawl(cls, args={'callback': self.yield_output})
        self.process.start()    