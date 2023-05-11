# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from io import BytesIO  #
from scrapy.pipelines.images import ImageException  #
from PIL import Image  #
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
import os
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
import pymongo.errors


class LeroyPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    # переопределим путь к изображениям (images/запрос/<артикул>/full/file_name.jpg)
    def file_path(self, request, response=None, info=None, *, item=None):
        # определим глобальную переменную, для использования в  def thumb_path, так как он не имеет доступа к item   
        global cat_name
        cat_name = item['main']
        dir_name = str(item['general']['article'])
        file_name = request.url.split('/')[-1]
        return f'{cat_name}/{dir_name}/full/{file_name}'

    # переопределим путь к сжатым файлам (images/запрос/<артикул>/<тепень сжатия>/file_name.jpg)
        def thumb_path(self, request, thumb_id, response=None, info=None):
            file_name = request.url.split('/')[-1]
            dir_name = file_name.replace('.jpg', '').split('_')[0]
            return f'{cat_name}/{dir_name}/{thumb_id}/small_{file_name}'

    def item_completed(self, results, item, info):

        for result in [x for ok, x in results if ok]:
            path = result['path']
            slug = path.split('/')[0]

            settings = get_project_settings()
            storage = settings.get('IMAGES_STORE')

            # если пути к папке не существует-создадим её
            if not os.path.exists(os.path.join(storage, slug)):
                os.makedirs(os.path.join(storage, slug))

        if self.IMAGES_RESULT_FIELD in item.fields:
            item[self.IMAGES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item


class LeroyparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        item['article'], item['name'], item['price'] = self.process_general(
            item['general'])
        collection = self.mongo_base[item['main']]
        del item['general']
        del item['main']
        collection.create_index('article', unique=True)
        duplicate = 0
        try:
            collection.insert_one(item)
        except pymongo.errors.DuplicateKeyError:
            duplicate += 1
        return item

    def process_general(self, general):
        return general['article'], general['name'], general['price']
