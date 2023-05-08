# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import pymongo.errors
import json


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        if spider.name == 'labru':
            item['title_id'] = int(item['book_url'].strip('/').split('/')[-1])
            item['publisher'], item['year'] = self.process_publusher(
                item['publisher'])
            item['ISBN'] = item['ISBN'].split()[1]
            item['rate'] = float(item['rate'])
            item['price'], item['discount_price'] = self.process_price_lab(
                item['general'])
        else:
            main = json.loads(item['main']) # преобразуем в json
            item['title_id'] = int(
                main['url'].strip('/').split('/')[-1].split('-')[-1])
            item['title'] = main['name']
            item['authors'] = main['author'].split(', ')
            item['book_url'] = main['url']
            item['cover_image'] = main['image']
            item['publisher'] = main['publisher']
            try:
                item['year'] = int(main['datePublished'])
            except KeyError as er:
                item['year'] = None
            item['ISBN'] = main['isbn']
            try:
                item['rate'] = float(main['aggregateRating']['ratingValue'])
            except KeyError as er:
                item['rate'] = None
            item['price'], item['discount_price'] = self.process_price_bk24(
                item['general'])
            del item['main']
        del item['general']

        collection = self.mongo_base[spider.name]
        collection.create_index('title_id', unique=True)
        duplicate = 0
        try:
            collection.insert_one(item)
        except pymongo.errors.DuplicateKeyError as er:
            duplicate += 1
        return item

    def process_publusher(self, data):
        publisher = data[1]
        year = int(data[2].split()[1])
        return publisher, year

    def process_price_lab(self, general):
        for i in range(len(general)):
            general[i] = general[i].strip()
        while "" in general:
            general.remove("")
        price = float(general[1])
        if len(general) == 3:
            discount_price = None
        else:
            discount_price = float(general[-2])
        return price, discount_price

    def process_price_bk24(self, general):
        for i in range(len(general)):
            general[i] = general[i].strip()
        while "" in general:
            general.remove("")
        if len(general) <= 4:
            price = float(general[1].replace(' ', ''))
            discount_price = None
        else:
            discount_price = float(general[1].replace(' ', ''))
            normal = general.pop(-2).split()[:-1]
            price = float(
                ''.join(normal[i] for i in range(len(normal))))
        return price, discount_price
