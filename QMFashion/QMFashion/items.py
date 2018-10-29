# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QmfashionItem(scrapy.Item):
	_id = scrapy.Field()
	url = scrapy.Field()
	published_time = scrapy.Field()
	modified_time = scrapy.Field()
	title = scrapy.Field()
	opening_text = scrapy.Field()
	news_source = scrapy.Field()
	posted = scrapy.Field()

	def __repr__(self):
		return repr({"title": "----------------------" + self["title"] + "----------------------"})