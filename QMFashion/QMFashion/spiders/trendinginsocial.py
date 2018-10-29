# -*- coding: utf-8 -*-
import scrapy
from ..items import QmfashionItem
from ..utilfunc import extract_first_paragraph
from datetime import datetime 
from dateutil.parser import parse as dateParse

class TrendingInSocialSpider(scrapy.Spider):
	name = 'trendinginsocial'
	start_urls = ['https://www.trendinginsocial.com/category/trending-in-fashion-beauty/']

	def parse(self, response):
		for href in response.css('div.inner-wrapper div[id="main-content"] div.post-listing article h2 a::attr(href)').extract():
			yield response.follow(href, self.parse_author)

	def parse_author(self, response):
		
		published_time = dateParse(response.css('body article[id="the-post"] p.post-meta span.tie-date::text').extract_first()).replace(tzinfo=None)
		modified_time = published_time

		todays_date = datetime.now()
		if published_time.date() < todays_date.date():
			return None

		for item in (response.css('body::attr(class)').extract_first()).split(' '):
			if 'postid' in item:
				id_constructor = item.split('-')

		qmfashionItem = QmfashionItem(
			_id = 'trendinginsocial' + '-' + id_constructor[len(id_constructor)-1],
			published_time = published_time,
			modified_time = modified_time,
			url = response.request.url,
			title = response.css('article[id="the-post"] div.post-inner .post-title span::text').extract_first(),
			opening_text = extract_first_paragraph(response,'article[id="the-post"] div.post-inner div.entry >'),
			news_source = "Trendinginsocial",
			posted = False
			)

		return qmfashionItem
