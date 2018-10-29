# -*- coding: utf-8 -*-
import scrapy
from ..items import QmfashionItem
from ..utilfunc import extract_first_paragraph
from datetime import datetime 
from dateutil.parser import parse as dateParse

class Fashion360Spider(scrapy.Spider):
	name = 'fashion360'
	start_urls = ['http://fashion360.pk/category/women-dresses/', 'http://fashion360.pk/category/celebrity-photoshoots/']

	def parse(self, response):
		for href in response.css('body div[id="wrapper-content"] div.content-area-inner article div.post-wrapper header.post-title a::attr(href)').extract():
			yield response.follow(href, self.parse_author)

	def parse_author(self, response):
		
		published_time = dateParse(response.css('meta[property="article:published_time"]::attr(content)').extract_first()).replace(tzinfo=None)
		try:
			modified_time = dateParse(response.css('meta[property="article:modified_time"]::attr(content)').extract_first()).replace(tzinfo=None)
		except:
			modified_time = published_time

		todays_date = datetime.now()
		if published_time.date() < todays_date.date():
			return None

		id_constructor = response.css('div[id="wrapper-main"] article::attr(id)').extract_first().split('-')

		qmfashionItem = QmfashionItem(
			_id = 'fashion360' + '-' + id_constructor[len(id_constructor)-1],
			published_time = published_time,
			modified_time = modified_time,
			url = response.request.url,
			title = response.css('meta[property="og:title"]::attr(content)').extract_first(),
			opening_text = extract_first_paragraph(response,'div[id="wrapper-main"] article div.post-content div.entry-content'),
			news_source = "Fashion360",
			posted = False
			)

		return qmfashionItem