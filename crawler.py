from multiprocessing.connection import wait
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

from data import get_list_of_domains
from matchrules.XpathCookieRule import XpathCookieRule
from matchrules.CookieIdRule import CookieIdRule
from matchrules.OneTrustSdkRule import OneTrustSdkRule
from matchrules.CookieClassRule import CookieClassRule

"""
    lua script which waits for a webpage to load so we can extract the banner
    since sometimes it takes time for a banner to appear

    this is used in our SplashRequest function
"""
load_page_script="""
    function main(splash)
        assert(splash:go(splash.args.url))
        assert(splash:wait(3))
        return {html=splash:html()}
    end
"""


"""
    our own Spider Scrapy crawler class
    which crawls the domain names defined in start_urls
    and uses rules to extract appropriate parts from the webpages
    
"""
class PolicyCrawler(scrapy.Spider):
    start_urls = get_list_of_domains()
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
        
    """
        function which returns an iterable with the first Requests to crawl for this spider
        it is called by Scrapy when the spider is opened for scraping

        it uses Splash Request which Executes a custom rendering script and returns a result
        in our cases we only use english pages which end with com, uk or edu domain root
    """
    def start_requests(self): 
        splash_args = {
           'lua_source': load_page_script,
           'timeout': 200,
           'width': 1024,
        }
        headers = {'User-Agent': 'my-test-banner-app'}

        for url in self.start_urls:
            domain = url.split('.')[0]
            top_level_domain = url.split('.')[-1]

            if domain not in self.parsed_domains and top_level_domain in ['com', 'uk', 'edu']:
                self.parsed_domains.add(domain)

                yield SplashRequest("https://"+url, self.parse, 
                    endpoint='execute', 
                    args=splash_args,
                    headers=headers
                )

    """
        the default callback used by Scrapy to process downloaded responses, 
        when their requests do not specify a callback

        we use different specific rules to parse the crawled responses
        if we find some parsed response with our rules we saved
        otherwise we assume the banner was not present on the page (adding FailedToFindBanner key-word)
    """
    def parse(self, response):
        key = response.url
        bannerHtml = self.runRules(response)
        
        if bannerHtml is not None and len(bannerHtml) > 0:
            self.crawled_sucess+=1
            self.data[key] = bannerHtml
        else:
            self.ftc_count+=1
            self.data[key] = "FailedToFindBanner"
            
    """
        function to run individual rules from the list of rules
    """
    def runRules(self, response):
        i = 0
        res = "" 
        while i < len(self.rules) and len(res) == 0:
            rule = self.rules[i]()
            res = rule.extract(response)
            i+=1
        
        return res

    """
        callback function to close the Scrapy Spider crawler and save the crawled output
    """
    def close(self, spider, reason):
        print(f"Succefully extracted {self.crawled_sucess}")
        print(f"Failed to extact banner from {self.ftc_count} sites")
        self.output_callback(self.data)


"""
    class which starts a Twisted reactor for you, 
    since Scrapy is built on top of the Twisted asynchronous networking library

    it uses CrawlerProcess() to strat the Twisted reactor
    it uses output variable to store the crawled data
    the crawl function actually runs the scrapy crawler with our own Spider Scrapy class, i.e. PolicyCrawler

"""
class Crawler:

    def __init__(self):
        self.output = None
        self.process = CrawlerProcess()

    def yield_output(self, data):
        self.output = data

    def crawl(self, cls):
        self.process.crawl(cls, args={'callback': self.yield_output})
        self.process.start()    