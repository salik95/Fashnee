# -*- coding: utf-8 -*-
import scrapy
from ..items import QmfashionItem
from ..utilfunc import extract_first_paragraph
from datetime import datetime 
from dateutil.parser import parse as dateParse

class DawnSpider(scrapy.Spider):
	name = 'dawn'
	start_urls = ['http://images.dawn.com/style/']

	def parse(self, response):
		for href in response.css("div.content main article figure a::attr(href)").extract():
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

		qmfashionItem = QmfashionItem(
			_id = 'dawn' + '-' + response.css('.story__title::attr(data-id)').extract_first(),
			published_time = published_time,
			modified_time = modified_time,
			url = response.request.url,
			title = response.css('.story__title a::text').extract_first(),
			opening_text = extract_first_paragraph(response,"article.story .story__content"),
			news_source = "Dawn",
			posted = False
			)

		return qmfashionItem