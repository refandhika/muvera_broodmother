import scrapy
import re
from rimanewscrawler.htmlparser import strip_tags
from rimanewscrawler.items import RimanewsItem

class RimanewsSpider(scrapy.Spider):
	name = "rimanews"
	allowed_domains = ["rimanews.com"]
	start_urls = [
		"http://rimanews.com/index/berita/terbaru"
	]

	def parse(self, response):
		for i in response.xpath('//div[@class="div-idx"]/div'):
			item = RimanewsItem()
			#Media Label
			item['media'] = 'Rima'
			#Date
			item['date'] = i.xpath('div[2]/div[1]/text()').extract()[0]
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			item['title'] = i.xpath('div[2]/div[3]/a').extract()[0]
			item['title'] = strip_tags(item['title'])
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
			#Link
			item['link'] = i.xpath('div[2]/div[3]/a/@href').extract()[0]
			#Sinopsis
			try:
				item['preview'] = i.xpath('div[2]/div[4]/text()').extract()[0]
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
			except:
				item['preview'] = 'No Preview'

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date
		date_cleaner = item['date']
		date_cleaner = re.sub('\| ', '', date_cleaner)
		item['date'] = date_cleaner

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

		for y in range(len(item['date'])-10,len(item['date'])-6):
			tahun = tahun + item['date'][y]

		for y in range(len(item['date'])-5,len(item['date'])):
			jam = jam + item['date'][y]


		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ':00'

		#Content
		pc = 0
		text_sum = response.xpath('//div[@class="isi-right"]/p').extract()[pc]
		text_check = response.xpath('//div[@class="isi-right"]/p').extract()[pc]
		for p in response.xpath('//div[@class="isi-right"]/p') :
			if (text_sum == text_check) :
				pc = pc + 1
				try:
					text_check = response.xpath('//div[@class="isi-right"]/p').extract()[pc]
				except:
					pass
			elif (text_sum != text_check) :
				text_sum = text_sum + text_check
				pc = pc + 1
				try:
					text_check = response.xpath('//div[@class="isi-right"]/p').extract()[pc]
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
		#try :
		#	item['author'] = response.xpath('//a[@rel="author"]/text()').extract()[0]
		#except :
		#	pass
		#Source
		#try :
		#	item['source'] = re.search(' \(.+?/(.+?)\)$', item['cont']).group(1)
		#except :
		#	pass

		yield item
