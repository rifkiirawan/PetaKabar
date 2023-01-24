import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
# from submodule.scrapper.scrapper.spiders.news_spider import NewsSpider
from bencana.main.submodule.scrapper.scrapper.spiders.news_spider import NewsSpider

import sys    

class ScrapProcess:
    def __init__(self) -> None:
        if "twisted.internet.reactor" in sys.modules:
            del sys.modules["twisted.internet.reactor"]

        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
            # 'DOWNLOAD_DELAY': 3,
            'CONCURRENT_ITEMS': 100,
            'AUTOTHROTTLE_ENABLED': False,
            'TELNETCONSOLE_ENABLED': False
            # 'AUTOTHROTTLE_START_DELAY': 5,
            # 'ROBOTSTXT_OBEY': True
        })

    def crawlNews(self) -> str:
        # try:
            self.process.crawl(NewsSpider, 'news')
            self.process.start()

            # print('masuk')
            # return 'success'
        # except:
        #     print('keluar')
        #     return 'error'
