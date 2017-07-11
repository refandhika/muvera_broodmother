import scrapy
import re
from republikacrawler.htmlparser import strip_tags
from republikacrawler.items import RepublikaItem

class RepublikaSpider(scrapy.Spider):
	name = "republika"
	allowed_domains = ["republika.co.id"]
	start_urls = [
		"http://www.republika.co.id/indeks"
	]

	def parse(self, response):
		for i in response.xpath('/html/body/div/div[3]/div[3]/div[@class="wp-indeks"]'):
			item = RepublikaItem()
			#Media Label
			item['media'] = 'Republika'
			#Date
			item['date'] = ''
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Preview
			item['preview'] = 'No Preview'
			#Title
			item['title'] = i.xpath('a/div[3]').extract()[0]
			item['title'] = strip_tags(item['title'])
			#Link
			item['link'] = i.xpath('a/@href').extract()[0]
			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date Format
		date_cleaner = response.xpath('//div[@class="date-detail"]/text()').extract()[0]
		date_cleaner = re.sub(',', '', date_cleaner)
		date_cleaner = re.sub('\s+', ' ', date_cleaner)
		date_cleaner = re.sub('^\S+ ', '', date_cleaner)
		date_cleaner = re.sub(' \S+$', '', date_cleaner)
		#print date_cleaner

		count = 0
		tanggal = ''
		bulan = ''
		tahun = ''
		jam = ''

		for y in range(0,2):
			tanggal = tanggal + date_cleaner[y]

		for y in date_cleaner:
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
		elif (bulan == 'January'):
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

		for y in range(len(date_cleaner)-10,len(date_cleaner)-6):
			tahun = tahun + date_cleaner[y]

		for y in range(len(date_cleaner)-5,len(date_cleaner)):
			jam = jam + date_cleaner[y]

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"

		#Content
		if (response.xpath('//div[@class="content-detail"]')) :
			text_cleaner = response.xpath('//div[@class="content-detail"]').extract()[0]
		elif (response.xpath('//div[@class="txt-detail"]')) :
			text_cleaner = response.xpath('//div[@class="txt-detail"]').extract()[0]
		
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
		text_cleaner = re.sub('\\xa0', '', text_cleaner)
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

		#Copyrigth
		try :
			cop_chk = response.xpath('//div[@class="wp-reset"]/div[@class="red"]').extract()[0]
			cop_chk = strip_tags(cop_chk)
			if (cop_chk[:3] == "Rep") :
				cop_chk = re.sub('/\s+', '/', cop_chk)
				item['author'] = re.sub('/.+', '', cop_chk)
				item['author'] = re.sub('^Rep: ', '', item['author'])
				item['editor'] = re.sub('.+/', '', cop_chk)
				item['editor'] = re.sub('^Red: ', '', item['editor'])
			else :
				cop_chk = re.sub('\s+Red:', 'Red:', cop_chk)
				item['editor'] = re.sub('Red: ', '', cop_chk)
		except :
			pass
				
		#Source
		if (response.xpath('//div[@class="detail-berita"]/div[3]/text()')) :
			item['source'] = response.xpath('//div[@class="detail-berita"]/div[3]/text()').extract()[0]
			item['source'] = re.sub('^Sumber : ', '', item['source'])

		yield item
