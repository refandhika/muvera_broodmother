import scrapy
import re
from antaranewscrawler.htmlparser import strip_tags
from antaranewscrawler.items import AntaranewsItem

class AntaranewsSpider(scrapy.Spider):
	name = "antaranews"
	allowed_domains = ["antaranews.com"]
	start_urls = [
		"http://www.antaranews.com/terkini"
	]

	def parse(self, response):
		for i in response.xpath('//ul[@class="ul_rubrik"]/li/div[@class="paging_ekonomi"]'):
			item = AntaranewsItem()
			#Media Label
			item['media'] = 'Antara'
			#Date
			item['date'] = ''
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			if (i.xpath('div[@class="bxpd"]//a')) :
				item['title'] = i.xpath('div[@class="bxpd"]//a').extract()[0]
				item['title'] = strip_tags(item['title'])
			elif (i.xpath('div[@class="bxpd bxpd2"]/a')) :
				item['title'] = i.xpath('div[@class="bxpd bxpd2"]/a').extract()[0]
				item['title'] = strip_tags(item['title'])
			item['title'] = re.sub('[\t\n\r\f\v]', '', item['title'])
			#Link
			if (i.xpath('div[@class="bxpd"]//a/@href')) :
				item['link'] = i.xpath('div[@class="bxpd"]//a/@href').extract()[0]
				item['link'] = "http://www.antaranews.com" + item['link']
			elif (i.xpath('div[@class="bxpd bxpd2"]/a/@href')) :
				item['link'] = i.xpath('div[@class="bxpd bxpd2"]/a/@href').extract()[0]
				item['link'] = "http://www.antaranews.com" + item['link']
			#Sinopsis
			if (i.xpath('div[@class="bxpd"]//div[@class="pt5"]/text()')) :
				item['preview'] = i.xpath('div[@class="bxpd"]//div[@class="pt5"]/text()').extract()[0]
			elif (i.xpath('div[@class="bxpd bxpd2"]/div[@class="pt5"]/text()')) :
				item['preview'] = i.xpath('div[@class="bxpd bxpd2"]/div[@class="pt5"]/text()').extract()[0]
			else :
				item['preview'] = 'No Preview'
			item['preview'] = re.sub('\s+', ' ', item['preview'])

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date
		if (response.xpath('//time[@itemprop="datePublished"]/text()')) :
			date_cleaner = response.xpath('//time[@itemprop="datePublished"]/text()').extract()[0]
		elif (response.xpath('/html/body/div[2]/div[1]/div[2]/span/text()')) :
			date_cleaner = response.xpath('/html/body/div[2]/div[1]/div[2]/span/text()').extract()[0]

		date_cleaner = re.sub('^\S+, ', '', date_cleaner)
		item['date'] = re.sub(' \S+$', '', date_cleaner)

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
		text_cleaner = response.xpath('//*[@id="content_news"]').extract()[0]
		text_cleaner = strip_tags(text_cleaner)
		text_cleaner = re.sub('[\t\n\r\f\v]', '', text_cleaner)
		text_cleaner = re.sub('^\s+', '', text_cleaner)
		text_cleaner = re.sub('\s+$', '', text_cleaner)
		text_cleaner = text_cleaner.replace(u'\u201c', u'"')
		text_cleaner = text_cleaner.replace(u'\u201d', u'"')
		text_cleaner = text_cleaner.replace(u'\u2013', u'-')
		text_cleaner = text_cleaner.replace(u'\u2014', u'-')
		text_cleaner = text_cleaner.replace(u'\u2019', u"'")
		text_cleaner = text_cleaner.replace(u'\u200e', u'')
		text_cleaner = re.sub('\\xa0', '', text_cleaner)
		text_cleaner = re.sub('\(adsbygoogle.+$', '', text_cleaner)
		text_cleaner = re.sub('Editor:.+$', '', text_cleaner)
		text_cleaner = re.sub('Penerjemah:.+$', '', text_cleaner)
		text_cleaner = re.sub('  +', ' ', text_cleaner)
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
			item['editor'] = response.xpath('//span[@itemprop="editor"]/text()').extract()[0]
		except :
			pass
		#Author
		try :
			item['author'] = response.xpath('//span[@itemprop="author"]/text()').extract()[0]
		except :
			pass

		yield item
