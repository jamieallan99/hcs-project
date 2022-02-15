from crawler import PolicyCrawler, Crawler


crawler = Crawler()
crawler.crawl(PolicyCrawler)

for o in crawler.output:
    print(o[:5000], "\n")
