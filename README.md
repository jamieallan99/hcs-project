# HCS Project 2022 
We will scrape cookie banners to analyse them.

Further, scope could be adding the ability to compare a specific policy and scrape the cookies as well.


**How to run Scrapy and Splash crawler:**
- Install requirements

```
pip install -r requirements.txt
```

- Install docker

https://www.docker.com/products/docker-desktop

- Run docker ( add -d flag before -p to run in the background)

```
docker run -p 8050:8050 scrapinghub/splash --max-timeout 300
```

- Run main.py

```
python main.py
```

Please note that you can provide the following command line arguments:
1. **-csv** that provides a csv file with the urls to be crawled
2. **-f** that specifies the name of the file to store the output

Examples can be seen below:

```
python main.py -csv myData.csv -f myOutputFile.txt
python main.py -csv Documents/myData.csv -f Documents/myOutputFile.txt
```

