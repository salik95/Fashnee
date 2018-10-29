# -*- coding: utf-8 -*-
import scrapy
from ..items import QmfashionItem
from ..utilfunc import extract_first_paragraph
from datetime import datetime 
from dateutil.parser import parse as dateParse
import hashlib

class SecretClosetSpider(scrapy.Spider):
	name = 'secretcloset'
	start_urls = ['http://www.secretcloset.pk/blog/']

	def parse(self, response):
		for href in response.css('div.blog-contents div.blog-desc h2 a::attr(href)').extract():
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

		article_title = response.css('meta[property="og:title"]::attr(content)').extract_first()

		qmfashionItem = QmfashionItem(
			_id = 'secretcloset' + '-' + hashlib.md5(article_title.encode('utf-8')).hexdigest(),
			published_time = published_time,
			modified_time = modified_time,
			url = response.request.url,
			title = article_title,
			opening_text = extract_first_paragraph(response,'div.main-container div.blogs div.blog-details'),
			news_source = "Secretcloset",
			posted = False
			)

		return qmfashionItem