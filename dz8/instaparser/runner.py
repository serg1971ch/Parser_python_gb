from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser.instaparser import settings
from instaparser.instaparser.spiders.profile import ProfileSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(ProfileSpider)

    process.start()