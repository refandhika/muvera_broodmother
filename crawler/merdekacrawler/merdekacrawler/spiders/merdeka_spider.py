import scrapy
import re
from merdekacrawler.htmlparser import strip_tags
from merdekacrawler.items import MerdekaItem

class MerdekaSpider(scrapy.Spider):
	name = "merdeka"
	allowed_domains = ["merdeka.com"]
	start_urls = [
		"http://www.merdeka.com/indeks-berita/"
	]

	def parse(self, response):
		for i in response.xpath('//div[@id="mdk-idn-nd-r"]/ul/li'):
			item = MerdekaItem()
			#Media Label
			item['media'] = 'Merdeka'
			#Date
			item['date'] = i.xpath('span/text()').extract()[0]
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			item['title'] = i.xpath('a').extract()[0]
			item['title'] = strip_tags(item['title'])
			#Link
			item['link'] = i.xpath('a/@href').extract()[0]
			item['link'] = 'http://www.merdeka.com' + item['link']
			#Sinopsis
			item['preview'] = i.xpath('p/text()').extract()[0]

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date Format
		item['date'] = re.sub('^\S+, ', '', item['date'])
		
		count = 0
		tanggal = ''
		bulan = ''
		tahun = ''
		jam = ''

		for y in range(0,2):
			tanggal = tanggal + item['date'][y]
		tanggal = re.sub('\s', '', tanggal)
		tanggal = str(tanggal).zfill(2)

		for y in item['date']:
			if y.isalpha():
				bulan = bulan + y

		#Convert format bulan to number
		if (bulan == 'Januari'):
			bulan = '01'
		elif (bulan == 'Februari'):
			bulan = '02'
		elif (bulan == 'Maret'):
			bulan = '03'
		elif (bulan == 'April'):
			bulan = '04'
		elif (bulan == 'Mei'):
			bulan = '05'
		elif (bulan == 'Juni'):
			bulan = '06'
		elif (bulan == 'Juli'):
			bulan = '07'
		elif (bulan == 'Agustus'):
			bulan = '08'
		elif (bulan == 'September'):
			bulan = '09'
		elif (bulan == 'Oktober'):
			bulan = '10'
		elif (bulan == 'November'):
			bulan = '11'
		elif (bulan == 'Desember'):
			bulan = '12'

		for y in range(len(item['date'])-13,len(item['date'])-9):
			tahun = tahun + item['date'][y]

		for y in range(len(item['date'])-8,len(item['date'])):
			jam = jam + item['date'][y]

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam

		#Content
		text_cleaner = response.xpath('//div[@class="mdk-body-paragpraph"]').extract()[0]
		text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_cleaner))
		text_cleaner = text_cleaner.replace(u'\u201c', u'"')
		text_cleaner = text_cleaner.replace(u'\u201d', u'"')
		text_cleaner = text_cleaner.replace(u'\u2013', u'-')
		text_cleaner = text_cleaner.replace(u'\u2014', u'-')
		text_cleaner = text_cleaner.replace(u'\u2018', u"'")
		text_cleaner = text_cleaner.replace(u'\u2019', u"'")
		text_cleaner = text_cleaner.replace(u'\u2026', u"...")
		text_cleaner = text_cleaner.replace(u'\u200e', u'')
		text_cleaner = re.sub('^\s+', '', text_cleaner)
		text_cleaner = re.sub('\s+$', '', text_cleaner)
		text_cleaner = re.sub('\$\(document\)\..*', '', text_cleaner)
		text_cleaner = re.sub('\\xa0', '', text_cleaner)
		item['cont'] = text_cleaner

		#Copyright
		#chk_cop = response.xpath('//div[@id="mdk-body-news-reporter"]/text()').extract()[0]
		#chk_cop = re.sub(' : *$', '', chk_cop)

		#if (chk_cop == "Reporter") :
			#Author
		#	item['author'] = response.xpath('//div[@id="mdk-body-news-reporter"]/a/text()').extract()[0]
			#Editor
		#	if (response.xpath('//div[@id="mdk-body-newsinit"]/text()')) :
		#		item['editor'] = response.xpath('//div[@id="mdk-body-newsinit"]/text()').extract()[0]
		#	else :
		#		item['editor'] = ''
		#elif (chk_cop == "Sumber") :
			#Source
		#	item['source'] = response.xpath('//div[@id="mdk-body-news-reporter"]/a/img/@title').extract()[0]
			#Editor
		#	if (re.search('\)$', text_cleaner)) :
		#		no_editor = ''
		#		for x in range(0,len(text_cleaner)-10):
		#			no_editor = no_editor + text_cleaner[x]
		#		item['cont'] = no_editor
		#		editor = ''
		#		for x in range(len(text_cleaner)-9,len(text_cleaner)):
		#			editor = editor + text_cleaner[x]
		#		item['editor'] = editor

		#Author
		item['author'] = response.xpath('//*[@class="reporter"]/a/text()').extract()[0]
		#Editor
		if (re.search('\]$', text_cleaner)) :
			no_editor = ''
			for x in range(0,len(text_cleaner)-6):
				no_editor = no_editor + text_cleaner[x]
			item['cont'] = no_editor
			editor = ''
			for x in range(len(text_cleaner)-5,len(text_cleaner)):
				editor = editor + text_cleaner[x]
			item['editor'] = editor

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

		yield item
