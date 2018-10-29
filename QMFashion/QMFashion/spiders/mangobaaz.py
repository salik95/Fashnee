# -*- coding: utf-8 -*-
import scrapy
from ..items import QmfashionItem
from ..utilfunc import extract_first_paragraph
from datetime import datetime 
from dateutil.parser import parse as dateParse
import requests
from lxml.html import fromstring

class MangobaazSpider(scrapy.Spider):
	name = 'mangobaaz'
	start_urls = ['https://www.mangobaaz.com/category/fashion/']

	def parse(self, response):
		r = requests.get('https://www.mangobaaz.com/category/fashion/feed')
		tree = fromstring(r.content)
		for href in tree.xpath("//a/@href"):
			yield response.follow(href, self.parse_author)

	def parse_author(self, response):

		try:
			published_time = dateParse(response.css('meta[property="article:published_time"]::attr(content)').extract_first()).replace(tzinfo=None)
		except:
			published_time = datetime.now()
		try:
			modified_time = dateParse(response.css('meta[property="article:modified_time"]::attr(content)').extract_first()).replace(tzinfo=None)
		except:
			modified_time = published_time

		todays_date = datetime.now()
		if published_time.date() < todays_date.date():
			raise scrapy.exceptions.CloseSpider('termination condition met')
			return None

		for item in (response.css('body::attr(class)').extract_first()).split(' '):
			if 'postid' in item:
				id_constructor = item.split('-')

		qmfashionItem = QmfashionItem(
			_id = 'mangobaaz' + '-' + id_constructor[len(id_constructor)-1],
			published_time = published_time,
			modified_time = modified_time,
			url = response.request.url,
			title = response.css('title::text').extract_first(),
			opening_text = extract_first_paragraph(response,'article[id="post-' + id_constructor[len(id_constructor)-1] + '"] div.entry-content >'),
			news_source = "Mangobaaz",
			posted = False
			)
		return qmfashionItem