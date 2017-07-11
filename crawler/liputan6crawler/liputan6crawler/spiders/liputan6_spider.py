import scrapy
import re
from liputan6crawler.htmlparser import strip_tags
from liputan6crawler.items import Liputan6Item

counter = 1

class Liputan6Spider(scrapy.Spider):
	name = "liputan6"
	allowed_domains = ["liputan6.com"]
	start_urls = [
		"http://www.liputan6.com/indeks"
	]

	def parse(self, response):
		global counter
		linkfinal = "http://www.liputan6.com/indeks?page="+str(counter)
		if (counter <= 5):
			counter = counter + 1
		else:
			counter = 1
		for i in response.xpath('//section[@id="indeks-articles"]/div/article'):
			item = Liputan6Item()
			#Media Label
			item['media'] = 'Liputan 6'
			#Date
			if (i.xpath('aside/header/span/time/text()')) :
				item['date'] = i.xpath('aside/header/span/time/text()').extract()[0]
			else :
				item['date'] = ''
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			if (i.xpath('aside/header/h4/a/span')) :
				item['title'] = i.xpath('aside/header/h4/a/span').extract()[0]
				item['title'] = strip_tags(item['title'])
			else :
				item['title'] = 'No Title'
			#Link
			if (i.xpath('aside/header/h4/a/@href')) :
				item['link'] = i.xpath('aside/header/h4/a/@href').extract()[0]
			else :
				item['link'] = 'No Link'
			#Sinopsis
			if (i.xpath('aside/div/text()')) :
				item['preview'] = i.xpath('aside/div/text()').extract()[0]
			else :
				item['preview'] = 'No Preview'

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

		if (counter != 1) :
			yield scrapy.Request(linkfinal, self.parse,dont_filter=True)

	def parse_content(self, response):
		item = response.meta['item']

		#Date Format
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

		for y in range(len(item['date'])-10,len(item['date'])-6):
			tahun = tahun + item['date'][y]

		for y in range(len(item['date'])-5,len(item['date'])):
			jam = jam + item['date'][y]

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"

		#Content
		text_cleaner = response.xpath('//div[@class="read-page--content"]').extract()[0]
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
		item['cont'] = re.sub('\\xa0', '', text_cleaner)

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

		#Author
		if (response.xpath('//span[@itemprop="author"]/text()')) :
			item['author'] = response.xpath('//span[@itemprop="author"]/text()').extract()[0]
		elif (response.xpath('//header[@class="read-page--header"]//span[@itemprop="name"]/text()')) :
			item['author'] = response.xpath('//header[@class="read-page--header"]//span[@itemprop="name"]/text()').extract()[0]
		
		yield item
