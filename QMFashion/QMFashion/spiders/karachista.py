# -*- coding: utf-8 -*-
import scrapy
from ..items import QmfashionItem
from ..utilfunc import extract_first_paragraph
from datetime import datetime 
from dateutil.parser import parse as dateParse

class KarachistaSpider(scrapy.Spider):
	name = 'karachista'
	start_urls = ['https://www.karachista.com/category/fashion/']

	def parse(self, response):
		for href in response.css('div.main div.posts-wrap article div.post-thumb a::attr(href)').extract():
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

		id_constructor = (response.css('body article.the-post::attr(id)').extract_first()).split('-')

		qmfashionItem = QmfashionItem(
			_id = 'karachista' + '-' + id_constructor[len(id_constructor)-1],
			published_time = published_time,
			modified_time = modified_time,
			url = response.request.url,
			title = response.css('body article.the-post header.post-header div.post-meta .post-title::text').extract_first(),
			opening_text = extract_first_paragraph(response,'body article.the-post div.post-content'),
			news_source = "Karachista",
			posted = False
			)
		return qmfashionItem