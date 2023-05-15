# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    name = scrapy.Field()  # наименование вакансии
    min_salary = scrapy.Field()  # минимальная зарплата
    max_salary = scrapy.Field()  # максимальная зарплата
    currency = scrapy.Field()  # валюта
    city = scrapy.Field()  # город
    source = scrapy.Field()  # сайт, где размещена вакансия
    vacancy_url = scrapy.Field()  # ссылка на вакансию
    vacancy_id = scrapy.Field()  # уникальный ID вакансии, для исключения дублирования
    employer = scrapy.Field()  # работодатель
    created_at = scrapy.Field()  # дата размещения вакансия
    general = scrapy.Field()  # вспомогательное поле для извлечение информации
    _id = scrapy.Field()  # поле для уникального ID MongoDB
