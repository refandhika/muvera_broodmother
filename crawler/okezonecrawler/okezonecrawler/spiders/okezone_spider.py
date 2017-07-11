import scrapy
import re
from okezonecrawler.htmlparser import strip_tags
from okezonecrawler.items import OkezoneItem

page = 0
class OkezoneSpider(scrapy.Spider):
	name = "okezone"
	allowed_domains = ["okezone.com"]
	start_urls = [
		"http://index.okezone.com/home/index/" + str(page)
	]

	def parse(self, response):
		global page
		linkfinal = ''
		if (page >=60 ):
			page = page + 15
		linkfinal = "http://index.okezone.com/home/index/" + str(page)
		for i in response.xpath('//*[@id="in"]/ol/li'):
			item = OkezoneItem()
			#Media Label
			item['media'] = 'Okezone'
			#Date
			item['date'] = ''
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			item['title'] = i.xpath('h4/a').extract()[0]
			item['title'] = strip_tags(item['title'])
			#Link
			item['link'] = i.xpath('h4/a/@href').extract()[0]
			#Sinopsis
			item['preview'] = 'No Preview'

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

		yield scrapy.Request(linkfinal, self.parse)

	def parse_content(self, response):
		item = response.meta['item']

		#Date Format
		item['date'] = response.xpath('//div[@class="meta-post"]//time/text()').extract()[0]
		item['date'] = re.sub('^\S+, ', '', item['date'])
		item['date'] = re.sub('- ', '', item['date'])
		item['date'] = re.sub(' \S+$', '', item['date'])

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

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"

		#Content
		text_cleaner = response.xpath('//*[@id="contentx"]').extract()[0]
		text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_cleaner))
		text_cleaner = text_cleaner.replace(u'\u201c', u'"')
		text_cleaner = text_cleaner.replace(u'\u201d', u'"')
		text_cleaner = text_cleaner.replace(u'\u2013', u'-')
		text_cleaner = text_cleaner.replace(u'\u2014', u'-')
		text_cleaner = text_cleaner.replace(u'\u2019', u"'")
		text_cleaner = text_cleaner.replace(u'\u200e', u'')
		text_cleaner = re.sub('^\s+', '', text_cleaner)
		text_cleaner = re.sub('\s+$', '', text_cleaner)
		item['cont'] = re.sub('\\xa0', '', text_cleaner)

		#Editor
		if (response.xpath('//div[@class="detail-img"]/strong/text()')) :
			item['editor'] = response.xpath('//div[@class="detail-img"]/strong/text()').extract()[0]
		elif (response.xpath('//div[@class="detnews"]/strong/text()')) :
			item['editor'] = response.xpath('//div[@class="detnews"]/strong/text()').extract()[0]

		#Copyright
		cop_chk = response.xpath('//div[@class="nmreporter"]/span/text()').extract()[0]
		if (cop_chk == "Jurnalis") :
			item['author'] = response.xpath('//div[@class="nmreporter"]/div/text()').extract()[0]
		elif (cop_chk == "Agregasi") :
			item['source'] = response.xpath('//div[@class="nmreporter"]/div/a/@href').extract()[0]
			item['source'] = re.sub('http://', '', text_cleaner)

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
