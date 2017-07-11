# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DetikItem(scrapy.Item):
	media = scrapy.Field()
	link = scrapy.Field()
	title = scrapy.Field()
	cont = scrapy.Field()
	date = scrapy.Field()
	author = scrapy.Field()
	editor = scrapy.Field()
	source = scrapy.Field()
	preview = scrapy.Field()
	opening = scrapy.Field()
	quote1 = scrapy.Field()
	quote2 = scrapy.Field()
	quote3 = scrapy.Field()
	quote4 = scrapy.Field()
	quote5 = scrapy.Field()