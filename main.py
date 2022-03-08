from argparse import ArgumentParser
import os

# Change the main.py so that it can accept arguments:
# 1. crawling a comma separated list of urls
# 2. ability to pass a path to custom url file
# 3. ability to specify output filename

print("SETTING THE PARSER")
parser = ArgumentParser()
parser.add_argument("-urls", nargs="+", help="Provide a list of urls to crawl (no commas needed)", required=False)
parser.add_argument("-csv", help="Provide a csv file with the urls to be crawled", required=False)
parser.add_argument("-f", "--filename", help="Specify the name of the file to store the output", required=False)
args, leftovers = parser.parse_known_args()

if args.csv is not None:
    os.environ["CSV"] = args.csv
else:
    os.environ["CSV"] = "top500Domains.csv"

csv = os.getenv("CSV")
print(csv)

# these import statements must be here (instead of at the top of the file) because
# the global variable CSV must be set first

from crawler import PolicyCrawler, Crawler
from html_parsing import strip_tags

crawler = Crawler()
crawler.crawl(PolicyCrawler)

if args.filename is not None:
    with open(args.filename, 'w', encoding="utf-8") as f:
        # crawl a comma separated list of urls provided by the user
        if args.urls is not None:
            for key, value in args.urls:
                write_out = strip_tags(value) if value else "None"
                f.write(key + '\n' + write_out + "\n\n")
        else:
            for key, value in crawler.output.items():
                write_out = strip_tags(value) if value else "None"
                f.write(key + '\n' + write_out + "\n\n")
else:
    with open('temp_file.txt', 'w', encoding="utf-8") as f:
        if args.urls is not None:
            # crawl a comma separated list of urls provided by the user
            for key, value in args.urls:
                write_out = strip_tags(value) if value else "None"
                f.write(key + '\n' + write_out + "\n\n")
        else:
            for key, value in crawler.output.items():
                write_out = strip_tags(value) if value else "None"
                f.write(key + '\n' + write_out + "\n\n")

