import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # вакансии по запросу "аналитик"
    start_urls = [
        'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA']

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            '//a[@data-qa="vacancy-serp__vacancy-title"]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.css(
            'a.HH-Pager-Controls-Next::attr("href")').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_url = response.url
        # вся информация по вакансии нашлась в теле скрипта
        general = response.xpath(
            '//script[@type="application/ld+json"]//text()').extract_first()
        yield JobparserItem(general=general, vacancy_url=vacancy_url)
