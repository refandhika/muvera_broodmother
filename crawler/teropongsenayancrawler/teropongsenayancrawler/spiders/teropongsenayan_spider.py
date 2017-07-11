import scrapy
import re
from teropongsenayancrawler.htmlparser import strip_tags
from teropongsenayancrawler.items import TeropongsenayanItem

class TeropongsenayanSpider(scrapy.Spider):
	name = "teropongsenayan"
	allowed_domains = ["teropongsenayan.com"]
	start_urls = [
		"http://www.teropongsenayan.com/indeks-berita"
	]

	def parse(self, response):
		for i in response.xpath('//ul[contains(@class, "media-list")]'):
			item = TeropongsenayanItem()
			#Media Label
			item['media'] = 'Teropong Senayan'
			#Date
			item['date'] = ''
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			if (i.xpath('*//div[@class="tsupdate-main-title"]/a')) :
				item['title'] = i.xpath('*//div[@class="tsupdate-main-title"]/a').extract()[0]
			elif (i.xpath('*//div[@class="tsupdate-title"]/a')) :
				item['title'] = i.xpath('*//div[@class="tsupdate-title"]/a').extract()[0]
			else :
				item['title'] = ''
			item['title'] = strip_tags(item['title'])
			print item['title']
			#Link
			if (i.xpath('*//div[@class="tsupdate-main-title"]/a')) :
				item['link'] = i.xpath('*//div[@class="tsupdate-main-title"]/a/@href').extract()[0]
			elif (i.xpath('*//div[@class="tsupdate-title"]/a')) :
				item['link'] = i.xpath('*//div[@class="tsupdate-title"]/a/@href').extract()[0]
			else :
				item['link'] = ''
			if (item['link'] != '' ) :
				item['link'] = "http://www.teropongsenayan.com/" + item['link']
			else :
				item['link'] = ''
			print item['link']
			#Sinopsis
			if (i.xpath('*//div[@class="tsupdate-main-title-date"][1]/text()')) :
				item['preview'] = i.xpath('*//div[@class="tsupdate-main-title-date"][1]/text()').extract()[0]
			elif (i.xpath('*//p/text()')) :
				item['preview'] = i.xpath('*//p/text()').extract()[0]
			else :
				item['preview'] = 'No Preview'
			print item['preview']
			#Request Page
			if (item['link'] != ''): 
				request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
				request.meta['item'] = item
				yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date
		date_cleaner = response.xpath('//div[@class="detailberita-writer"]/span[3]/text()').extract()[0]
		date_cleaner = re.sub('\- ', '', date_cleaner)
		date_cleaner = re.sub('^.+,  ', '', date_cleaner)
		date_cleaner = re.sub(' W.+$', '', date_cleaner)
		item['date'] = date_cleaner
		print item['preview']

		tanggal = ''
		bulan = ''
		tahun = ''
		jam = ''

		for y in range(0,2):
			tanggal = tanggal + item['date'][y]

		for y in item['date']:
			if y.isalpha():
				bulan = bulan + y

		#Convert format bulan to number
		if (bulan == 'Jan'):
			bulan = '01'
		elif (bulan == 'Feb'):
			bulan = '02'
		elif (bulan == 'Mar'):
			bulan = '03'
		elif (bulan == 'Apr'):
			bulan = '04'
		elif (bulan == 'Mei'):
			bulan = '05'
		elif (bulan == 'Jun'):
			bulan = '06'
		elif (bulan == 'Jul'):
			bulan = '07'
		elif (bulan == 'Agu'):
			bulan = '08'
		elif (bulan == 'Sep'):
			bulan = '09'
		elif (bulan == 'Okt'):
			bulan = '10'
		elif (bulan == 'Nov'):
			bulan = '11'
		elif (bulan == 'Des'):
			bulan = '12'

		for y in range(len(item['date'])-13,len(item['date'])-9):
			tahun = tahun + item['date'][y]

		for y in range(len(item['date'])-8,len(item['date'])):
			jam = jam + item['date'][y]


		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam

		#Content
		pc = 0
		text_sum = response.xpath('//div[@class="detailberita-isiberita"]/p').extract()[pc]
		text_check = response.xpath('//div[@class="detailberita-isiberita"]/p').extract()[pc]
		for p in response.xpath('//div[@class="detailberita-isiberita"]/p') :
			if (text_sum == text_check) :
				pc = pc + 1
				try:
					text_check = response.xpath('//div[@class="detailberita-isiberita"]/p').extract()[pc]
				except:
					pass
			elif (text_sum != text_check) :
				text_sum = text_sum + text_check
				pc = pc + 1
				try:
					text_check = response.xpath('//div[@class="detailberita-isiberita"]/p').extract()[pc]
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
		try :
			item['editor'] = re.search('\((.{1,3})\)$', text_cleaner).group(1)
		except :
			pass
		#Author
		try :
			item['author'] = response.xpath('//div[@class="detailberita-writer"]/span[1]/text()').extract()[0]
		except :
			pass
		#Source
		#try :
		#	item['source'] = response.xpath('//div[@class="detailberita-penulis"][2]/text()').extract()[1]
		#	item['source'] = re.sub(', ', '', item['source'])
		#except :
		#	pass

		yield item
