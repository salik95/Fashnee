# -*- coding: utf-8 -*-
import scrapy
from ..items import QmfashionItem
from ..utilfunc import extract_first_paragraph
from datetime import datetime 
from dateutil.parser import parse as dateParse

class SomethinghauteSpider(scrapy.Spider):
	name = 'somethinghaute'
	start_urls = ['https://www.somethinghaute.com/category/fashion-style/']

	def parse(self, response):
		for href in response.css("article h2.eltd-post-title a::attr(href)").extract():
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

		for item in (response.css('body::attr(class)').extract_first()).split(' '):
			if 'postid' in item:
				id_constructor = item.split('-')

		qmfashionItem = QmfashionItem(
			_id = 'somethinghaute' + '-' + id_constructor[len(id_constructor)-1],
			published_time = published_time,
			modified_time = modified_time,
			url = response.request.url,
			title = response.css('.eltd-post-title a::text').extract_first(),
			opening_text = extract_first_paragraph(response,"article div.eltd-post-content div.eltd-post-text"),
			news_source = "Somethinghaute",
			posted = False
			)

		return qmfashionItem