from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from bookparser import settings
from bookparser.spiders.labru import LabruSpider
from bookparser.spiders.bk24ru import Bk24ruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabruSpider)
    process.crawl(Bk24ruSpider)

    process.start()
