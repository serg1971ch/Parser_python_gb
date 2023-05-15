# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import pymongo.errors
import json
from datetime import datetime


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy2103

    def process_item(self, item, spider):
        # преобразуем в json
        vacancy_info = json.loads(item['general'])
        item['name'] = vacancy_info['title']
        item['city'] = vacancy_info['jobLocation']['address'][
            'addressLocality']
        item['employer'] = vacancy_info['hiringOrganization']['name']
        item['source'] = self.process_source(spider.name)
        item['vacancy_url'], item['vacancy_id'] = self.process_link(
            vacancy_info['url'],
            spider.name) if spider.name == 'sjru' else self.process_link(
            item['vacancy_url'], spider.name)
        try:
            item['min_salary'], item['max_salary'], item[
                'currency'] = self.process_salary(vacancy_info['baseSalary'],
                                                  spider.name)
        except KeyError as er:
            item['min_salary'], item['max_salary'], item[
                'currency'] = None, None, None
        item['created_at'] = self.process_date(vacancy_info['datePosted'],
                                               spider.name)
        del item['general']
        collection = self.mongo_base[spider.name]
        collection.create_index('vacancy_id', unique=True)
        duplicate = 0
        try:
            collection.insert_one(item)
        except pymongo.errors.DuplicateKeyError:
            duplicate += 1
        return item

    def process_link(self, vacancy_url, spider_name):
        real_link = []
        if spider_name == 'hhru':
            short_link = vacancy_url.split('?')[0]
            real_link.append(short_link)
            real_link.append(int(short_link.split('/')[-1]))
        else:
            real_link.append(vacancy_url)
            real_link.append(int(vacancy_url.split('.')[-2].split('-')[-1]))
        return real_link

    def process_date(self, created_at, spider_name):
        created_at = created_at.replace('T', ' ')[:-6] + " " + created_at[
                                                               -6:].replace(
            ':', '')
        return datetime.strptime(created_at,
                                 '%Y-%m-%d %H:%M:%S %z') if spider_name == 'sjru' else datetime.strptime(
            created_at, '%Y-%m-%d %H:%M:%S.%f %z')

    def process_source(self, source):
        if source == 'hhru':
            return 'HH.RU'
        else:
            return 'SUPERJOB.RU'

    def process_salary(self, salary, spider_name):
        currency = salary.get('currency')
        min_salary = salary['value'].get('minValue')
        max_salary = salary['value'].get('maxValue')
        if spider_name == 'hhru' and not min_salary:
            max_salary = salary['value'].get('value')
        return min_salary, max_salary, currency
