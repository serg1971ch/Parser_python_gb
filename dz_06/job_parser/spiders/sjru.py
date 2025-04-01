import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    # вакансии по запросу "аналитик"
    start_urls = ['https://www.superjob.ru/vakansii/analitik.html?noGeo=1']

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            '//span[contains(@class, "f-test-text-company-item-salary")]/..//a/@href').extract()
        for link in links:
            yield response.follow('https://www.superjob.ru' + link,
                                  callback=self.vacancy_parse)
        next_page = response.css(
            'a.f-test-button-dalshe::attr("href")').extract_first()
        if next_page:
            yield response.follow('https://www.superjob.ru' + next_page,
                                  callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        # вся информация по вакансии нашлась в теле скрипта
        general=response.xpath(
            '//div[@class="_1Tjoc UGN79 undefined _1XYex"]//script//text()').extract_first()
        yield JobparserItem(general=general)

