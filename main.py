from crawler import PolicyCrawler, Crawler
from html_parsing import strip_tags

crawler = Crawler()
crawler.crawl(PolicyCrawler)

with open('temp_file.txt', 'w', encoding="utf-8") as f:
    for o in crawler.output:
        f.write(strip_tags(o) + "\n")
