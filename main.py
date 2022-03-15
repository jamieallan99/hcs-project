from crawler import PolicyCrawler, Crawler
from html_parsing import strip_tags

"""
    initialize the crawler and run it
    return: save the output from the crawler into a temp_file
"""

crawler = Crawler()
crawler.crawl(PolicyCrawler)


with open('temp_file.txt', 'w', encoding="utf-8") as f:
    for key,value in crawler.output.items():
        write_out = strip_tags(value) if value else "None"
        f.write(key+'\n' + write_out + "\n\n")
