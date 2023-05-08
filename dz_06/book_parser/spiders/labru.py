import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabruSpider(scrapy.Spider):
    name = 'labru'
    allowed_domains = ['labirint.ru']
    # книги по запросу: "программирование"
    start_urls = [
        'https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/?stype=0&available=1&paperbooks=1&ebooks=1']

    def parse(self, response: HtmlResponse):
        links = response.css('a.cover::attr(href)').extract()
        for link in links:
            yield response.follow('https://www.labirint.ru' + link,
                                  callback=self.book_parse)
        next_page = response.xpath(
            '//div[@class="pagination-next"]//a/@href').extract_first()
        if next_page:
            yield response.follow(self.start_urls[0].split('?')[0] + next_page,
                                  callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        title = response.xpath(
            '//div[@id="product-left-column"]//@data-name').extract_first()
        authors = response.xpath(
            '//a[@data-event-label="author"]/text()').extract()
        book_url = response.url
        cover = response.xpath(
            '//div[@id="product-image"]//img/@data-src').extract_first()
        publisher = response.xpath(
            '//div[@class="publisher"]//text()').extract()
        # информация о ценах
        general = response.xpath(
            '//div[@class="buying"]/div[contains(@class, "buying-price")]//text()').extract()
        ISBN = response.xpath('//div[@class="isbn"]/text()').extract_first()
        rate = response.xpath('//div[@id="rate"]/text()').extract_first()
        yield BookparserItem(title=title, authors=authors, book_url=book_url,
                              general=general, cover_image=cover,
                              publisher=publisher, ISBN=ISBN,
                              rate=rate)
