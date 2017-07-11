import scrapy
import re
from cnnindocrawler.htmlparser import strip_tags
from cnnindocrawler.items import CnnindoItem

class CnnindoSpider(scrapy.Spider):
	name = "cnnindo"
	allowed_domains = ["cnnindonesia.com"]
	start_urls = [
		"http://www.cnnindonesia.com/indeks/"
	]

	def parse(self, response):
		for i in response.xpath('//ul[@class="list_indeks"]/li'):
			item = CnnindoItem()
			#Media Label
			item['media'] = 'CNN Indonesia'
			#Date
			item['date'] = i.xpath('div[1]/span/text()').extract()[0]
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			item['title'] = i.xpath('div[1]/h3/a/text()').extract()[0]
			#Link
			item['link'] = i.xpath('div[1]/h3/a/@href').extract()[0]
			#Sinopsis
			item['preview'] = i.xpath('div[1]/text()').extract()[3]
			item['preview'] = re.sub('^\s+', '', item['preview'])
			item['preview'] = re.sub('\s+$', '', item['preview'])
			item['preview'] = re.sub('\\xa0', '', item['preview'])

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date Format
		item['date'] = re.sub('^\S+, ', '', item['date'])

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

		#Content
		if (response.xpath('//*[@id="detail"]')) :
			text_cleaner = response.xpath('//*[@id="detail"]').extract()[0]
		elif (response.xpath('//div[@class="text_detail"]')) :
			text_cleaner = response.xpath('//*[@class="text_detail"]').extract()[0]
		text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_cleaner))
		text_cleaner = text_cleaner.replace(u'\u201c', u'"')
		text_cleaner = text_cleaner.replace(u'\u201d', u'"')
		text_cleaner = text_cleaner.replace(u'\u2013', u'-')
		text_cleaner = text_cleaner.replace(u'\u2014', u'-')
		text_cleaner = text_cleaner.replace(u'\u2019', u"'")
		text_cleaner = text_cleaner.replace(u'\u200e', u'')
		text_cleaner = re.sub('^\s+', '', text_cleaner)
		text_cleaner = re.sub('\s+$', '', text_cleaner)
		text_cleaner = re.sub('--\s+', '--  ', text_cleaner)
		text_cleaner = re.sub('  \s+.*$', '', text_cleaner)
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
		if (response.xpath('//div[@class="author"]/strong/text()')) :
			item['author'] = response.xpath('//div[@class="author"]/strong/text()').extract()[0]
		else :
			item['author'] = ''

		#Editor
		if (response.xpath('//*[@id="detail"]/b/text()')) :
			item['editor'] = response.xpath('//*[@id="detail"]/b/text()').extract()[0]
		else :
			item['editor'] = ''

		yield item
