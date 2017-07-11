import scrapy
import re
from fajarcrawler.htmlparser import strip_tags
from fajarcrawler.items import FajarItem

class FajarSpider(scrapy.Spider):
	name = "fajar"
	allowed_domains = ["fajar.co.id"]
	start_urls = [
		"http://fajar.co.id/index-berita/"
	]

	def parse(self, response):
		for i in response.xpath('//*[@id="archive-list-wrap"]/ul/li'):
			item = FajarItem()
			#Media Label
			item['media'] = 'Fajar'
			#Date
			item['date'] = ''
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			if (i.xpath('a/div/div[2]/div/h2')):
				item['title'] = i.xpath('a/div/div[2]/div/h2').extract()[0]
			elif (i.xpath('a/div/h2')):
				item['title'] = i.xpath('a/div/h2').extract()[0]
			item['title'] = strip_tags(re.sub('[\t\n\r\f\v]', '', item['title']))
			item['title'] = item['title'].replace(u'\u201c', u'"')
			item['title'] = item['title'].replace(u'\u201d', u'"')
			item['title'] = item['title'].replace(u'\u2013', u'-')
			item['title'] = item['title'].replace(u'\u2014', u'-')
			item['title'] = item['title'].replace(u'\u2018', u"'")
			item['title'] = item['title'].replace(u'\u2019', u"'")
			item['title'] = item['title'].replace(u'\u2026', u"...")
			item['title'] = item['title'].replace(u'\u200e', u'')
			item['title'] = re.sub('\\xa0', ' ', item['title'])
			item['title'] = re.sub('\\xad', ' ', item['title'])
			item['title'] = re.sub('\s+', ' ', item['title'])
			#Link
			item['link'] = i.xpath('a/@href').extract()[0]
			#Sinopsis
			if (i.xpath('a/div/div[2]/div/p/text()')):
				item['preview'] = i.xpath('a/div/div[2]/div/p/text()').extract()[0]
			elif (i.xpath('a/div/p/text()')):
				item['preview'] = i.xpath('a/div/p/text()').extract()[0]
			else:
				item['preview'] = 'No Preview'
			item['preview'] = strip_tags(re.sub('[\t\n\r\f\v]', '', item['preview']))
			item['preview'] = item['preview'].replace(u'\u201c', u'"')
			item['preview'] = item['preview'].replace(u'\u201d', u'"')
			item['preview'] = item['preview'].replace(u'\u2013', u'-')
			item['preview'] = item['preview'].replace(u'\u2014', u'-')
			item['preview'] = item['preview'].replace(u'\u2018', u"'")
			item['preview'] = item['preview'].replace(u'\u2019', u"'")
			item['preview'] = item['preview'].replace(u'\u2026', u"...")
			item['preview'] = item['preview'].replace(u'\u200e', u'')
			item['preview'] = re.sub('\\xa0', ' ', item['preview'])
			item['preview'] = re.sub('\\xad', ' ', item['preview'])
			item['preview'] = re.sub('\s+', ' ', item['preview'])

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date
		date_cleaner = response.xpath('//time[@itemprop="datePublished"][1]/text()').extract()[0]
		item['date'] = re.sub(',', '', date_cleaner)

		#for x in range (1,10):
		#	print item['date']

		#tanggal = response.xpath('//time[@itemprop="datePublished"]/@datetime').extract[0]
		tanggal = ''
		bulan = ''
		tahun = ''
		jam = ''
		time_chk = ''

		for y in range(len(item['date'])-5,len(item['date'])):
			jam = jam + item['date'][y]
		for y in range(len(item['date'])-11,len(item['date'])-7):
			tahun = tahun + item['date'][y]
		for y in range(len(item['date'])-14,len(item['date'])-12):
			tanggal = tanggal + item['date'][y]

		tanggal = re.sub(' ', '', tanggal)
		tanggal = tanggal.zfill(2)

		for y in item['date']:
			if y.isalpha():
				bulan = bulan + y

		#Convert format bulan to number
		if (bulan == 'January'):
			bulan = '01'
		elif (bulan == 'February'):
			bulan = '02'
		elif (bulan == 'March'):
			bulan = '03'
		elif (bulan == 'April'):
			bulan = '04'
		elif (bulan == 'May'):
			bulan = '05'
		elif (bulan == 'June'):
			bulan = '06'
		elif (bulan == 'July'):
			bulan = '07'
		elif (bulan == 'August'):
			bulan = '08'
		elif (bulan == 'September'):
			bulan = '09'
		elif (bulan == 'October'):
			bulan = '10'
		elif (bulan == 'November'):
			bulan = '11'
		elif (bulan == 'December'):
			bulan = '12'

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"
		#item['date'] = tanggal + ' ' + jam + ":00"

		if (response.xpath('//*[@id="content-main"]/p/a')):
			deeplink = response.xpath('//*[@id="content-main"]/p/a/@href').extract()[0]
			checklink = deeplink[:4]
			if(checklink == 'http'):
				item['link'] = response.xpath('//*[@id="content-main"]/p/a/@href').extract()[0]
				request = scrapy.Request(item['link'],callback=self.parse_deep_content, dont_filter=True)
				request.meta['item'] = item
				yield request
		else:
			#Content
			pc = 0
			text_sum = response.xpath('//*[@id="content-main"]/p').extract()[pc]
			text_check = response.xpath('//*[@id="content-main"]/p').extract()[pc]
			for p in response.xpath('//*[@id="content-main"]/p') :
				if (text_sum == text_check) :
					pc = pc + 1
					try:
						text_check = response.xpath('//*[@id="content-main"]/p').extract()[pc]
					except:
						pass
				elif (text_sum != text_check) :
					text_sum = text_sum + text_check
					pc = pc + 1
					try:
						text_check = response.xpath('//*[@id="content-main"]/p').extract()[pc]
					except:
						pass

			text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_sum))
			text_cleaner = text_cleaner.replace(u'\u201c', u'"')
			text_cleaner = text_cleaner.replace(u'\u201d', u'"')
			text_cleaner = text_cleaner.replace(u'\u2013', u'-')
			text_cleaner = text_cleaner.replace(u'\u2014', u'-')
			text_cleaner = text_cleaner.replace(u'\u2018', u"'")
			text_cleaner = text_cleaner.replace(u'\u2019', u"'")
			text_cleaner = text_cleaner.replace(u'\u2026', u"...")
			text_cleaner = text_cleaner.replace(u'\u200e', u'')
			text_cleaner = re.sub('\\xa0', ' ', text_cleaner)
			text_cleaner = re.sub('\\xad', ' ', text_cleaner)
			text_cleaner = re.sub('\s+', ' ', text_cleaner)
			item['cont'] = text_cleaner

			#Opening
			opening_formula = re.compile(ur'\s*[A-Z].+?\.')
			temp = re.findall(opening_formula,item['cont'])
			if len(temp) >= 4:
				opening = str(temp[0])+str(temp[1])+str(temp[2])+str(temp[3])
			elif len(temp) == 3:
				opening = str(temp[0])+str(temp[1])+str(temp[2])
			elif len(temp) == 2:
				opening = str(temp[0])+str(temp[1])
			elif len(temp) == 1:
				opening = str(temp[0])
			else :
				opening = 'No Content'
			item['opening'] = opening

			#Quote
			quote_formula = re.compile(ur'\"[A-Z].+?[\,\.]+?\".+?\.')
			quote1 = ''
			quote2 = ''
			quote3 = ''
			quote4 = ''
			quote5 = ''

			temp = re.findall(quote_formula,item['cont'])
			if len(temp) >= 5:
				quote1 = str(temp[0])
				quote2 = str(temp[1])
				quote3 = str(temp[2])
				quote4 = str(temp[3])
				quote5 = str(temp[4])
			elif len(temp) == 4:
				quote1 = str(temp[0])
				quote2 = str(temp[1])
				quote3 = str(temp[2])
				quote4 = str(temp[3])
			elif len(temp) == 3:
				quote1 = str(temp[0])
				quote2 = str(temp[1])
				quote3 = str(temp[2])
			elif len(temp) == 2:
				quote1 = str(temp[0])
				quote2 = str(temp[1])
			elif len(temp) == 1:
				quote1 = str(temp[0])
			else:
				quote1 = "No Quote"
			item['quote1'] = quote1
			item['quote2'] = quote2
			item['quote3'] = quote3
			item['quote4'] = quote4
			item['quote5'] = quote5

			#Editor
			#try :
			#	item['editor'] = re.search(' \((.+?)/.+\)$', item['cont']).group(1)
			#except :
			#	pass
			#Author
			try :
				item['author'] = response.xpath('//a[@rel="author"]/text()').extract()[0]
			except :
				pass
			#Source
			#try :
			#	item['source'] = re.search(' \(.+?/(.+?)\)$', item['cont']).group(1)
			#except :
			#	pass

			yield item

	def parse_deep_content(self, response):
		item = response.meta['item']

		#Date
		#date_cleaner = response.xpath('//time[@itemprop="datePublished"]/text()').extract()[0]
		#item['date'] = re.sub(',', '', date_cleaner)

		#for x in range (1,10):
		#	print item['date']

		#tanggal = response.xpath('//time[@itemprop="datePublished"]/@datetime').extract[0]
		#tanggal = ''
		#bulan = ''
		#tahun = ''
		#jam = ''
		#time_chk = ''

		#for y in range(len(item['date'])-2,len(item['date'])):
		#	time_chk = time_chk + item['date'][y]

		#if (time_chk == "am") :
		#	item['date'] = re.sub(' am', '', date_cleaner)
		#	for y in range(len(item['date'])-5,len(item['date'])):
		#		jam = jam + item['date'][y]
		#	jam = re.sub('@', '', jam)
		#	jam = jam.zfill(5)
		#	for y in range(len(item['date'])-11,len(item['date'])-7):
		#		tahun = tahun + item['date'][y]
		#	for y in range(len(item['date'])-14,len(item['date'])-12):
		#		tanggal = tanggal + item['date'][y]
		#elif (time_chk == "pm") :
		#	item['date'] = re.sub(' pm', '', date_cleaner)
		#	for y in range(len(item['date'])-5,len(item['date'])-3):
		#		jam = jam + item['date'][y]
		#	jam = re.sub('@', '', jam)
		#	jam = int(jam) + 12
		#	jam = str(jam).zfill(2)
		#	for y in range(len(item['date'])-3,len(item['date'])):
		#		jam = jam + item['date'][y]
		#	for y in range(len(item['date'])-11,len(item['date'])-7):
		#		tahun = tahun + item['date'][y]
		#	for y in range(len(item['date'])-14,len(item['date'])-12):
		#		tanggal = tanggal + item['date'][y]

		#tanggal = re.sub(' ', '', tanggal)
		#tanggal = tanggal.zfill(2)

		#for y in item['date']:
		#	if y.isalpha():
		#		bulan = bulan + y

		#Convert format bulan to number
		#if (bulan == 'January'):
		#	bulan = '01'
		#elif (bulan == 'February'):
		#	bulan = '02'
		#elif (bulan == 'March'):
		#	bulan = '03'
		#elif (bulan == 'April'):
		#	bulan = '04'
		#elif (bulan == 'May'):
		#	bulan = '05'
		#elif (bulan == 'June'):
		#	bulan = '06'
		#elif (bulan == 'July'):
		#	bulan = '07'
		#elif (bulan == 'August'):
		#	bulan = '08'
		#elif (bulan == 'September'):
		#	bulan = '09'
		#elif (bulan == 'October'):
		#	bulan = '10'
		#elif (bulan == 'November'):
		#	bulan = '11'
		#elif (bulan == 'December'):
		#	bulan = '12'

		#item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"
		#item['date'] = tanggal + ' ' + jam + ":00"

		#Content
		pc = 0
		text_sum = response.xpath('//*[@id="content-main"]/p').extract()[pc]
		text_check = response.xpath('//*[@id="content-main"]/p').extract()[pc]
		for p in response.xpath('//*[@id="content-main"]/p') :
			if (text_sum == text_check) :
				pc = pc + 1
				try:
					text_check = response.xpath('//*[@id="content-main"]/p').extract()[pc]
				except:
					pass
			elif (text_sum != text_check) :
				text_sum = text_sum + text_check
				pc = pc + 1
				try:
					text_check = response.xpath('//*[@id="content-main"]/p').extract()[pc]
				except:
					pass

		text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_sum))
		text_cleaner = text_cleaner.replace(u'\u201c', u'"')
		text_cleaner = text_cleaner.replace(u'\u201d', u'"')
		text_cleaner = text_cleaner.replace(u'\u2013', u'-')
		text_cleaner = text_cleaner.replace(u'\u2014', u'-')
		text_cleaner = text_cleaner.replace(u'\u2018', u"'")
		text_cleaner = text_cleaner.replace(u'\u2019', u"'")
		text_cleaner = text_cleaner.replace(u'\u2026', u"...")
		text_cleaner = text_cleaner.replace(u'\u200e', u'')
		text_cleaner = re.sub('\\xa0', ' ', text_cleaner)
		text_cleaner = re.sub('\\xad', ' ', text_cleaner)
		text_cleaner = re.sub('\s+', ' ', text_cleaner)
		item['cont'] = text_cleaner

		#Opening
		opening_formula = re.compile(ur'\s*[A-Z].+?\.')
		temp = re.findall(opening_formula,item['cont'])
		if len(temp) >= 4:
			opening = str(temp[0])+str(temp[1])+str(temp[2])+str(temp[3])
		elif len(temp) == 3:
			opening = str(temp[0])+str(temp[1])+str(temp[2])
		elif len(temp) == 2:
			opening = str(temp[0])+str(temp[1])
		elif len(temp) == 1:
			opening = str(temp[0])
		else :
			opening = 'No Content'
		item['opening'] = opening

		#Quote
		quote_formula = re.compile(ur'\"[A-Z].+?[\,\.]+?\".+?\.')
		quote1 = ''
		quote2 = ''
		quote3 = ''
		quote4 = ''
		quote5 = ''

		temp = re.findall(quote_formula,item['cont'])
		if len(temp) >= 5:
			quote1 = str(temp[0])
			quote2 = str(temp[1])
			quote3 = str(temp[2])
			quote4 = str(temp[3])
			quote5 = str(temp[4])
		elif len(temp) == 4:
			quote1 = str(temp[0])
			quote2 = str(temp[1])
			quote3 = str(temp[2])
			quote4 = str(temp[3])
		elif len(temp) == 3:
			quote1 = str(temp[0])
			quote2 = str(temp[1])
			quote3 = str(temp[2])
		elif len(temp) == 2:
			quote1 = str(temp[0])
			quote2 = str(temp[1])
		elif len(temp) == 1:
			quote1 = str(temp[0])
		else:
			quote1 = "No Quote"
		item['quote1'] = quote1
		item['quote2'] = quote2
		item['quote3'] = quote3
		item['quote4'] = quote4
		item['quote5'] = quote5

		#Editor
		#try :
		#	item['editor'] = re.search(' \((.+?)/.+\)$', item['cont']).group(1)
		#except :
		#	pass
		#Author
		try :
			item['author'] = response.xpath('//a[@rel="author"]/text()').extract()[0]
		except :
			pass
		#Source
		#try :
		#	item['source'] = re.search(' \(.+?/(.+?)\)$', item['cont']).group(1)
		#except :
		#	pass

		yield item