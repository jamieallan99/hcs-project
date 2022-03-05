# HCS Project 2022 
We will scrape cookie policies to analyse them.

Further scope could be adding the ability to compare a specific policy and scrape the cookies as well.


How to run:
- install requirements

```
pip install -r requirements.txt
```

- install docker

https://www.docker.com/products/docker-desktop

- run docker ( add -d flag before -p to run in the background)

```
docker run -p 8050:8050 scrapinghub/splash --max-timeout 300
```

- run main.py

```
python main.py
```