# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
class MongoPipeline(object):
    collection_name = 'yoho_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', '127.0.0.1'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'paper')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # 获得正确的maching_items
        pipeline = [
            {"$group": {"_id": "$matching.id", "categories": {"$addToSet": "$category"}}},
            {"$project": {"size": {"$size": "$categories"}}},
            {"$match": {"size": 2}},
            {"$out": "yoho_valid_matchings"}
        ]
        self.db[self.collection_name].aggregate(pipeline)
        self.client.close()

    def process_item(self, item, spider):
        # 防止重复
        if self.db[self.collection_name].find({"product_url": item['product_url']}).count() == 0 \
                or self.db[self.collection_name].find({"matching.id": item['matching']['id']}).count() == 0:
            self.db[self.collection_name].insert(dict(item))
        return item
