import scrapy
import re
from detikcrawler.htmlparser import strip_tags
from detikcrawler.items import DetikItem
from scrapy.http import FormRequest

kanal = ['news','finance','hot','inet','sport','oto','travel','food','health','wolipop']

class DetikSpider(scrapy.Spider):
	name = "detik"
	allowed_domains = ["detik.com"]
	start_urls = [
		"http://www.detik.com"
	]

	def parse(self, response):
		global kanal

		for prefix in kanal:
			if(prefix == 'wolipop'):
				linkkanal = "http://"+prefix+".detik.com/index"
			else:
				linkkanal = "http://"+prefix+".detik.com/indeks"
			yield scrapy.Request(linkkanal, callback=self.parse_kanal, dont_filter=True)

	def parse_kanal(self, response):
		if(response.xpath('//ul/li/article')):
			for i in response.xpath('//ul/li/article'):
				item = DetikItem()
				#Media Label
				item['media'] = 'Detik'
				#Link
				item['link'] = "http:" + i.xpath('div/a/@href').extract()[0]
				#Source
				item['source'] = 'No Source'
				#Preview
				item['preview'] = 'No Preview'

				#Request Page
				request = scrapy.Request(item['link'], callback=self.parse_content_v1, dont_filter=True)
				request.meta['item'] = item
				yield request
		elif(response.xpath('//ul[@class="list_indeks"]/li')):
			for i in response.xpath('//ul[@class="list_indeks"]/li'):
				item = DetikItem()
				#Media Label
				item['media'] = 'Detik'
				#Link
				if(i.xpath('a/@href')):
					item['link'] = i.xpath('a/@href').extract()[0]
				if(i.xpath('h5/a/@href')):
					item['link'] = i.xpath('h5/a/@href').extract()[0]
				#Source
				item['source'] = 'No Source'
				#Preview
				item['preview'] = 'No Preview'

				#Request Page
				request = scrapy.Request(item['link'], callback=self.parse_content_v2, dont_filter=True)
				request.meta['item'] = item
				yield request
		elif(response.xpath('//ul[@class="listnews4"]/li')):
			for i in response.xpath('//ul[@class="listnews4"]/li'):
				item = DetikItem()
				#Media Label
				item['media'] = 'Detik'
				#Link
				item['link'] = i.xpath('a/@href').extract()[0]
				#Source
				item['source'] = 'No Source'
				#Preview
				item['preview'] = 'No Preview'

				#Request Page
				request = scrapy.Request(item['link'], callback=self.parse_content_v2, dont_filter=True)
				request.meta['item'] = item
				yield request

	def parse_content_v1(self, response):
		item = response.meta['item']
		#Date
		if (response.xpath('//*[@class="date"]')):
			item['date'] = response.xpath('//*[@class="date"]/text()').extract()[0]
		else :
			item['date'] = 'No Date'

		item['date'] = re.sub('^\S+ ', '', item['date'])
		item['date'] = re.sub(', ', ' ', item['date'])
		item['date'] = re.sub(' \S+$', '', item['date'])

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
		elif (bulan == 'May' or bulan == 'Mei'):
			bulan = '05'
		elif (bulan == 'Jun'):
			bulan = '06'
		elif (bulan == 'Jul'):
			bulan = '07'
		elif (bulan == 'Aug' or bulan == 'Agu'):
			bulan = '08'
		elif (bulan == 'Sep'):
			bulan = '09'
		elif (bulan == 'Oct' or bulan == 'Okt'):
			bulan = '10'
		elif (bulan == 'Nov'):
			bulan = '11'
		elif (bulan == 'Dec' or bulan == 'Des'):
			bulan = '12'

		for y in range(len(item['date'])-10,len(item['date'])-6):
			tahun = tahun + item['date'][y]

		for y in range(len(item['date'])-5,len(item['date'])):
			jam = jam + item['date'][y]

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"

		#Title
		item['title'] = response.xpath('//article//h1/text()').extract()[0]
		item['title'] = re.sub('^\s+', '', item['title'])
		item['title'] = re.sub('\s+$', '', item['title'])

		#Author
		item['author'] = response.xpath('//*[@class="author"]/text()').extract()[0]
		item['author'] = re.sub(' - .+', '', item['author'])

		#Content
		text_cleaner = strip_tags(response.xpath('//*[@class="detail_text"]').extract()[0])
		text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_cleaner))
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
		text_cleaner = re.sub('^\s+', '', text_cleaner)
		text_cleaner = re.sub('\s+$', '', text_cleaner)
		text_cleaner = re.sub('\s+\$.+$', '', text_cleaner)
		text_cleaner = re.sub('\)\s+Photo Gallery.+$', ')', text_cleaner)
		text_cleaner = re.sub('\s+', ' ', text_cleaner)
		no_editor = ''
		for x in range(0,len(text_cleaner)-10):
			no_editor = no_editor + text_cleaner[x]
		item['cont'] = no_editor

		#Editor
		editor = ''
		for x in range(len(text_cleaner)-9,len(text_cleaner)):
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

	def parse_content_v2(self, response):
		item = response.meta['item']
		#Date
		if (response.xpath('//*[@class="date"][1]')):
			item['date'] = response.xpath('//*[@class="date"][1]/text()').extract()[0]
		else :
			item['date'] = 'No Date'

		item['date'] = re.sub('^.+, ', '', item['date'])
		item['date'] = re.sub(' \S+$', '', item['date'])

		tanggal = ''
		bulan = ''
		tahun = ''
		jam = ''

		for y in range(0,2):
			tanggal = tanggal + item['date'][y]

		for y in range(3,5):
			bulan = bulan + item['date'][y]

		for y in range(6,10):
			tahun = tahun + item['date'][y]

		for y in range(len(item['date'])-5,len(item['date'])):
			jam = jam + item['date'][y]

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"

		#Title
		item['title'] = response.xpath('//h1/text()').extract()[0]

		#Author
		item['author'] = response.xpath('//*[@class="author"]//strong/text()').extract()[0]
		item['author'] = re.sub(' - .+', '', item['author'])

		#Content
		if(response.xpath('//div[@class="text_detail"]')):
			text_cleaner = strip_tags(response.xpath('//div[@class="text_detail"]').extract()[0])
		elif(response.xpath('//div[@class="text_detail minwidth"]')):
			text_cleaner = strip_tags(response.xpath('//div[@class="text_detail minwidth"]').extract()[0])
		text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_cleaner))
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
		text_cleaner = re.sub('^\s+', '', text_cleaner)
		text_cleaner = re.sub('\s+$', '', text_cleaner)
		text_cleaner = re.sub('\s+\$.+$', '', text_cleaner)
		text_cleaner = re.sub('\)\s+Photo Gallery.+$', ')', text_cleaner)
		text_cleaner = re.sub('\s+', ' ', text_cleaner)
		no_editor = ''
		for x in range(0,len(text_cleaner)-10):
			no_editor = no_editor + text_cleaner[x]
		item['cont'] = no_editor

		#Editor
		editor = ''
		for x in range(len(text_cleaner)-9,len(text_cleaner)):
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
