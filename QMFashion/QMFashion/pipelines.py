# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import facebook
import pytz

class QmfashionPipeline(object):
	collection_name = 'fashion_articles'
	def __init__(self, mongo_uri, mongo_db ,mongo_port, mongo_user, mongo_password, page_id, access_token):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db
		self.mongo_port = mongo_port
		self.mongo_user = mongo_user
		self.mongo_password = mongo_password
		self.page_id = page_id
		self.access_token = access_token

	@classmethod
	def from_crawler(cls, crawler):
		## pull in information from settings.py
		return cls(
			mongo_uri=crawler.settings.get('MONGO_URI'),
			mongo_db= crawler.settings.get('MONGO_DATABASE'),
			mongo_port = crawler.settings.get('MONGO_PORT'),
			mongo_user = crawler.settings.get('MONGO_USER'),
			mongo_password = crawler.settings.get('MONGO_PASSWORD'),
			page_id = crawler.settings.get('PAGE_ID'),
			access_token = crawler.settings.get('ACCESS_TOKEN')
		)

	def open_spider(self, spider):
		## initializing spider
		## opening db connection
		self.client = pymongo.MongoClient(self.mongo_uri , self.mongo_port)
		self.db = self.client[self.mongo_db]
		self.db.authenticate(self.mongo_user , self.mongo_password)
		self.graph = facebook.GraphAPI(access_token = self.access_token)

	def close_spider(self, spider):
		# clean up when spider is closed
		self.client.close()

	def process_item(self, item, spider):
		try:
			self.db[self.collection_name].insert(dict(item))
			logging.info("Article added to MongoDB")
			# self.graph.put_object(parent_object = self.page_id, connection_name = 'feed', message = dict(item)['opening_text'], link = dict(item)['url'])
		except Exception as e:
			logging.debug(str(e))
		return item
