import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Bk24ruSpider(scrapy.Spider):
    name = 'bk24ru'
    allowed_domains = ['book24.ru']
    # книги по запросу: "программирование"
    start_urls = [
        'https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5']

    def parse(self, response: HtmlResponse):
        links=response.css('a.book-preview__image-link::attr(href)').extract()
        for link in links:
            yield response.follow('https://book24.ru' + link, callback=self.book_parse)
        next_page= response.xpath('//a[contains(text(), "Далее")]/@href').extract_first()
        if next_page:
            yield response.follow('https://book24.ru'+next_page, callback=self.parse)


    def book_parse(self, response:HtmlResponse):
        # собираем информацию о цене
        general=response.xpath('//div[@class="item-actions__prices"]//text()').extract()
        # вся информация о товаре находится в теле скрипта
        main=response.xpath('//div[@class="item-detail__wrapper js-product-card"]/following::script[1]/text()').extract_first()
        yield BookparserItem(general=general, main=main)