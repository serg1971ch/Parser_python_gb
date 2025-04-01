# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    title_id = scrapy.Field()  # ID товара, уникальый индекс для исключения дублирования
    title = scrapy.Field()  # название
    book_url = scrapy.Field()  # ссылка на книгу на сайте
    cover_image = scrapy.Field()  # ссылка на изображение обложки
    rate = scrapy.Field()  # рейтинг книги
    ISBN = scrapy.Field()  # код ISBN
    authors = scrapy.Field()  # список авторов
    publisher = scrapy.Field()  # издательство
    year = scrapy.Field()  # год издания
    price = scrapy.Field()  # цена
    discount_price = scrapy.Field()  # цена с учётом скидки, если есть
    main = scrapy.Field()  # вспомогательное поле для извлечения информации
    general = scrapy.Field()  # вспомогательное поле для извлечения информации
    _id = scrapy.Field()  # поле для внутреннего индекса MongoDB
