from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("-csv", help="Provide a csv file with the urls to be crawled", required=False)
parser.add_argument("-f", help="Specify the name of the file to store the output", required=False)
args, leftovers = parser.parse_known_args()

if args.csv is not None:
    os.environ["CSV"] = args.csv
else:
    os.environ["CSV"] = "top500Domains.csv"

csv = os.getenv("CSV")

# these import statements must be here (instead of at the top of the file) because
# the global variable CSV must be set first
from crawler import PolicyCrawler, Crawler
from html_parsing import strip_tags

"""
    initialize the crawler and run it
    return: save the output from the crawler into a temp_file
"""

crawler = Crawler()
crawler.crawl(PolicyCrawler)

if args.f is not None:
    with open(args.f, 'w', encoding="utf-8") as f:
        # crawl a comma separated list of urls provided by the user
        print(crawler.output.items())
        for key, value in crawler.output.items():
            write_out = strip_tags(value) if value else "None"
            f.write(key + '\n' + write_out + "\n\n")
else:
    with open('temp_file.txt', 'w', encoding="utf-8") as f:
        print(crawler.output.items())
        for key, value in crawler.output.items():
            write_out = strip_tags(value) if value else "None"
            f.write(key + '\n' + write_out + "\n\n")

