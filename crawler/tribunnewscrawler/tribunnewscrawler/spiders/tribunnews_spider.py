import scrapy
import re
from tribunnewscrawler.htmlparser import strip_tags
from tribunnewscrawler.items import TribunnewsItem

class TribunnewsSpider(scrapy.Spider):
	name = "tribunnews"
	allowed_domains = ["tribunnews.com"]
	start_urls = [
		"http://www.tribunnews.com/index-news"
	]

	def parse(self, response):
		for i in response.xpath('//ul[@class="lsi"]/li'):
			item = TribunnewsItem()
			#Media Label
			item['media'] = 'Tribun'
			#Date
			item['date'] = i.xpath('time[@class="grey"]/text()').extract()[0]
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Preview
			item['preview'] = 'No Preview'
			#Title
			item['title'] = i.xpath('h3[@class="f16 fbo"]/a').extract()[0]
			item['title'] = strip_tags(item['title'])
			item['title'] = re.sub('^\s+', '', item['title'])
			item['title'] = re.sub(' \s+$', '', item['title'])
			#Link
			item['link'] = i.xpath('h3[@class="f16 fbo"]/a/@href').extract()[0]

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date Format
		item['date'] = re.sub('^\S+, ', '', item['date'])
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
		text_cleaner = response.xpath('//*[@id="article_con"]/div[3]').extract()[0]
		text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_cleaner))
		text_cleaner = text_cleaner.replace(u'\u201c', u'"')
		text_cleaner = text_cleaner.replace(u'\u201d', u'"')
		text_cleaner = text_cleaner.replace(u'\u2013', u'-')
		text_cleaner = text_cleaner.replace(u'\u2014', u'-')
		text_cleaner = text_cleaner.replace(u'\u2018', u"'")
		text_cleaner = text_cleaner.replace(u'\u2019', u"'")
		text_cleaner = text_cleaner.replace(u'\u2026', u"...")
		text_cleaner = text_cleaner.replace(u'\u200e', u'')
		text_cleaner = re.sub('\\xad', ' ', text_cleaner)
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

		#Copyright
		if (response.xpath('//*[@id="article_con"]/div[4]/div[@class="f12 grey mb15"]/div[1]/text()')) :
			cop_chk1 = response.xpath('//*[@id="article_con"]/div[4]/div[@class="f12 grey mb15"]/div[1]/text()').extract()[0]
			cop_chk1 = re.sub('^\s+', '', cop_chk1)
			cop_chk1 = re.sub('\s+$', '', cop_chk1)
			chk1 = cop_chk1
			cop_chk1 = re.sub(':.*$', '', cop_chk1)
			if (cop_chk1 == "Penulis") :
				item['author'] = re.sub('^.*: ', '', chk1)
			elif (cop_chk1 == "Editor") :
				item['editor'] = re.sub('^.*: ', '', chk1)
			elif (cop_chk1 == "Sumber") :
				item['source'] = response.xpath('//*[@id="article_con"]/div[4]/div[@class="f12 grey mb15"]/div[1]/a/@title').extract()[0]

		if (response.xpath('//*[@id="article_con"]/div[4]/div[@class="f12 grey mb15"]/div[2]/text()')) :
			cop_chk2 = response.xpath('//*[@id="article_con"]/div[4]/div[@class="f12 grey mb15"]/div[2]/text()').extract()[0]
			cop_chk2 = re.sub('^\s+', '', cop_chk2)
			cop_chk2 = re.sub('\s+$', '', cop_chk2)
			chk2 = cop_chk2
			cop_chk2 = re.sub(':.*$', '', cop_chk2)
			if (cop_chk2 == "Editor") :
				item['editor'] = re.sub('^.*: ', '', chk2)
			elif (cop_chk2 == "Sumber") :
				item['source'] = response.xpath('//*[@id="article_con"]/div[4]/div[@class="f12 grey mb15"]/div[2]/a/@title').extract()[0]

		yield item
