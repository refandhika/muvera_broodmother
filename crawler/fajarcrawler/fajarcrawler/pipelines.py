# -*- coding: utf-8 -*-
#import json
import sys
import MySQLdb
import hashlib

#from scrapy import signals
#from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem
from scrapy.http import Request

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MySQLStorePipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(user='root', passwd='', db='muvera', host='localhost', charset="utf8", use_unicode=True)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT INTO media_data (media, title, author, date, content, editor, source, link, preview, opening, quote1, quote2, quote3, quote4, quote5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
				(item['media'].encode('utf-8'),
					item['title'].encode('utf-8'),
					item['author'].encode('utf-8'),
					item['date'].encode('utf-8'),
					item['cont'].encode('utf-8'),
					item['editor'].encode('utf-8'),
					item['source'].encode('utf-8'),
					item['link'].encode('utf-8'),
					item['preview'].encode('utf-8'),
					item['opening'].encode('utf-8'),
					item['quote1'].encode('utf-8'),
					item['quote2'].encode('utf-8'),
					item['quote3'].encode('utf-8'),
					item['quote4'].encode('utf-8'),
					item['quote5'].encode('utf-8')))
			self.conn.commit()

		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])

		return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.links_seen = set()

    def process_item(self, item, spider):
        if item['link'] in self.links_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.links_seen.add(item['link'])
            return item