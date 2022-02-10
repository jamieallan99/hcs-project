from crawler import PolicyCrawler, Crawler


crawler = Crawler()
crawler.crawl(PolicyCrawler)
print(crawler.output)
