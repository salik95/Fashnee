# -*- coding: utf-8 -*-
import scrapy
from ..items import QmfashionItem
from ..utilfunc import extract_first_paragraph
from datetime import datetime 
from dateutil.parser import parse as dateParse

class SundaySpider(scrapy.Spider):
	name = 'sunday'
	start_urls = ['https://sunday.com.pk/category/fashion/']

	def parse(self, response):
		for href in response.css('section[id="content"] article header .entry-title a::attr(href)').extract():
			yield response.follow(href, self.parse_author)

	def parse_author(self, response):
		
		published_time = dateParse(response.css('main[id="content"] article header div.entry-meta time::attr(datetime)').extract_first()).replace(tzinfo=None)
		modified_time = published_time

		todays_date = datetime.now()
		if published_time.date() < todays_date.date():
			return None

		id_constructor = response.css('div.site-content main[id="content"] article::attr(id)').extract_first().split('-')

		first_paragraph = extract_first_paragraph(response,'div.site-content main[id="content"] article div.entry-content')
		if first_paragraph is None:
			first_paragraph = response.css('div.site-content main[id="content"] article div.single-title .entry-title::text').extract_first()

		qmfashionItem = QmfashionItem(
			_id = 'sunday' + '-' + id_constructor[len(id_constructor)-1],
			published_time = published_time,
			modified_time = modified_time,
			url = response.request.url,
			title = response.css('div.site-content main[id="content"] article div.single-title .entry-title::text').extract_first(),
			opening_text = first_paragraph,
			news_source = "Sunday.com.pk",
			posted = False
			)
		return qmfashionItem