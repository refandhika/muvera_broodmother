import scrapy
import re
from kompascrawler.htmlparser import strip_tags
from kompascrawler.items import KompasItem

class KompasSpider(scrapy.Spider):
	name = "kompas"
	allowed_domains = ["kompas.com"]
	start_urls = [
		"http://indeks.kompas.com"
	]

	def parse(self, response):
		for i in response.xpath('//div[@class="tleft"]'):
			item = KompasItem()
			#Media Label
			item['media'] = 'Kompas'
			#Date
			try :
				item['date'] = i.xpath('div/text()').extract()[0]
			except :
				pass
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			try :
				item['title'] = i.xpath('h3/a').extract()[0]
				item['title'] = strip_tags(item['title'])
				item['title'] = item['title'].replace(u'\u201c', u'"')
				item['title'] = item['title'].replace(u'\u201d', u'"')
				item['title'] = item['title'].replace(u'\u2013', u'-')
				item['title'] = item['title'].replace(u'\u2014', u'-')
				item['title'] = item['title'].replace(u'\u2018', u"'")
				item['title'] = item['title'].replace(u'\u2019', u"'")
				item['title'] = item['title'].replace(u'\u2026', u"...")
				item['title'] = item['title'].replace(u'\u200e', u'')
				item['title'] = re.sub('\\xa0', '', item['title'])
				item['title'] = re.sub('\\xad', '', item['title'])
			except :
				pass
			#Link
			try :
				item['link'] = i.xpath('h3/a/@href').extract()[0]
			except :
				pass
			#Sinopsis
			try :
				item['preview'] = i.xpath('p/text()').extract()[0]
			except :
				pass

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request
	
	def parse_content(self, response):
		item = response.meta['item']

		#Date Format
		item['date'] = re.sub('^\S+, ', '', item['date'])
		item['date'] = re.sub('\| ', '', item['date'])
		item['date'] = re.sub(' \S+$', '', item['date'])

		tgl = ''
		bln = ''
		thn = ''
		jam = ''

		for y in range(0,2):
			tgl = tgl + item['date'][y]
		tgl = re.sub('\s', '', tgl)
		tgl = str(tgl).zfill(2)

		for y in item['date']:
			if y.isalpha():
				bln = bln + y

		#Convert format bln to number
		if (bln == 'Januari'):
			bln = '01'
		elif (bln == 'Februari'):
			bln = '02'
		elif (bln == 'Maret'):
			bln = '03'
		elif (bln == 'April'):
			bln = '04'
		elif (bln == 'Mei'):
			bln = '05'
		elif (bln == 'Juni'):
			bln = '06'
		elif (bln == 'Juli'):
			bln = '07'
		elif (bln == 'Agustus'):
			bln = '08'
		elif (bln == 'September'):
			bln = '09'
		elif (bln == 'Oktober'):
			bln = '10'
		elif (bln == 'November'):
			bln = '11'
		elif (bln == 'Desember'):
			bln = '12'

		for y in range(len(item['date'])-10,len(item['date'])-6):
			thn = thn + item['date'][y]

		for y in range(len(item['date'])-5,len(item['date'])):
			jam = jam + item['date'][y]

		item['date'] = thn + '-' + bln + '-' + tgl + ' ' + jam + ":00"

		#Content
		if (response.xpath('//div[@class="kcm-read-text"]')) :
			text_cleaner = response.xpath('//div[@class="kcm-read-text"]').extract()[0]
		elif (response.xpath('//span[@class="kcmread1114"]')) :
			text_cleaner = response.xpath('//span[@class="kcmread1114"]').extract()[0]
		elif (response.xpath('//div[@class="div-read"]')) :
			text_cleaner = response.xpath('//div[@class="div-read"]').extract()[0]

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
		item['cont'] = re.sub(' \.title-.+\;\}$', '', text_cleaner)

		#Copyright
		if (response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[1]/td[1]')) :
			cop_chk = response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[1]/td[1]/text()').extract()[0]
			cop_chk = re.sub('^\s+', '', cop_chk)
			cop_chk = re.sub('\s+$', '', cop_chk)
			if (cop_chk == "Penulis") :
				item['author'] = response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['author'] = re.sub('^\s*: ', '', item['author'])
				item['author'] = re.sub('\s+$', '', item['author'])
			elif (cop_chk == "Editor") :
				item['editor'] = response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['editor'] = re.sub('^\s*: ', '', item['editor'])
				item['editor'] = re.sub('\s+$', '', item['editor'])
			elif (cop_chk == "Sumber") :
				item['source'] = response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['source'] = re.sub('^\s*: ', '', item['source'])
				item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[1]/td[1]')) :
			cop_chk = response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[1]/td[1]/text()').extract()[0]
			cop_chk = re.sub('^\s+', '', cop_chk)
			cop_chk = re.sub('\s+$', '', cop_chk)
			if (cop_chk == "Penulis") :
				item['author'] = response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['author'] = re.sub('^\s*: ', '', item['author'])
				item['author'] = re.sub('\s+$', '', item['author'])
			elif (cop_chk == "Editor") :
				item['editor'] = response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['editor'] = re.sub('^\s*: ', '', item['editor'])
				item['editor'] = re.sub('\s+$', '', item['editor'])
			elif (cop_chk == "Sumber") :
				item['source'] = response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['source'] = re.sub('^\s*: ', '', item['source'])
				item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[1]/td[1]')) :
			cop_chk = response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[1]/td[1]/text()').extract()[0]
			cop_chk = re.sub('^\s+', '', cop_chk)
			cop_chk = re.sub('\s+$', '', cop_chk)
			if (cop_chk == "Penulis") :
				item['author'] = response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['author'] = re.sub('^\s*: ', '', item['author'])
				item['author'] = re.sub('\s+$', '', item['author'])
			elif (cop_chk == "Editor") :
				item['editor'] = response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['editor'] = re.sub('^\s*: ', '', item['editor'])
				item['editor'] = re.sub('\s+$', '', item['editor'])
			elif (cop_chk == "Sumber") :
				item['source'] = response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['source'] = re.sub('^\s*: ', '', item['source'])
				item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[1]/td[1]')) :
			cop_chk = response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[1]/td[1]/text()').extract()[0]
			cop_chk = re.sub('^\s+', '', cop_chk)
			cop_chk = re.sub('\s+$', '', cop_chk)
			if (cop_chk == "Penulis") :
				item['author'] = response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['author'] = re.sub('^\s*: ', '', item['author'])
				item['author'] = re.sub('\s+$', '', item['author'])
			elif (cop_chk == "Editor") :
				item['editor'] = response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['editor'] = re.sub('^\s*: ', '', item['editor'])
				item['editor'] = re.sub('\s+$', '', item['editor'])
			elif (cop_chk == "Sumber") :
				item['source'] = response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[1]/td[2]/text()').extract()[0]
				item['source'] = re.sub('^\s*: ', '', item['source'])
				item['source'] = re.sub('\s+$', '', item['source'])

		if (response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[2]/td[1]')) :
			cop_chk = response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[2]/td[1]/text()').extract()[0]
			cop_chk = re.sub('^\s+', '', cop_chk)
			cop_chk = re.sub('\s+$', '', cop_chk)
			if (cop_chk == "Editor") :
				item['editor'] = response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[2]/td[2]/text()').extract()[0]
				item['editor'] = re.sub('^\s*: ', '', item['editor'])
				item['editor'] = re.sub('\s+$', '', item['editor'])
			elif (cop_chk == "Sumber") :
				item['source'] = response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[2]/td[2]/text()').extract()[0]
				item['source'] = re.sub('^\s*: ', '', item['source'])
				item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[2]/td[1]')) :
			cop_chk = response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[2]/td[1]/text()').extract()[0]
			cop_chk = re.sub('^\s+', '', cop_chk)
			cop_chk = re.sub('\s+$', '', cop_chk)
			if (cop_chk == "Editor") :
				item['editor'] = response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[2]/td[2]/text()').extract()[0]
				item['editor'] = re.sub('^\s*: ', '', item['editor'])
				item['editor'] = re.sub('\s+$', '', item['editor'])
			elif (cop_chk == "Sumber") :
				item['source'] = response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[2]/td[2]/text()').extract()[0]
				item['source'] = re.sub('^\s*: ', '', item['source'])
				item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[2]/td[1]')) :
			cop_chk = response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[2]/td[1]/text()').extract()[0]
			cop_chk = re.sub('^\s+', '', cop_chk)
			cop_chk = re.sub('\s+$', '', cop_chk)
			if (cop_chk == "Editor") :
				item['editor'] = response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[2]/td[2]/text()').extract()[0]
				item['editor'] = re.sub('^\s*: ', '', item['editor'])
				item['editor'] = re.sub('\s+$', '', item['editor'])
			elif (cop_chk == "Sumber") :
				item['source'] = response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[2]/td[2]/text()').extract()[0]
				item['source'] = re.sub('^\s*: ', '', item['source'])
				item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[2]/td[1]')) :
			cop_chk = response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[2]/td[1]/text()').extract()[0]
			cop_chk = re.sub('^\s+', '', cop_chk)
			cop_chk = re.sub('\s+$', '', cop_chk)
			if (cop_chk == "Editor") :
				item['editor'] = response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[2]/td[2]/text()').extract()[0]
				item['editor'] = re.sub('^\s*: ', '', item['editor'])
				item['editor'] = re.sub('\s+$', '', item['editor'])
			elif (cop_chk == "Sumber") :
				item['source'] = response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[2]/td[2]/text()').extract()[0]
				item['source'] = re.sub('^\s*: ', '', item['source'])
				item['source'] = re.sub('\s+$', '', item['source'])

		if (response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[3]/td[1]')) :
			item['source'] = response.xpath('//div[@class="kcm-read-copy mt1"]/table/tbody/tr[3]/td[2]/text()').extract()[0]
			item['source'] = re.sub('^\s*: ', '', item['source'])
			item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[3]/td[1]')) :
			item['source'] = response.xpath('//div[@class="kcm-read-copy mt2"]/table/tbody/tr[3]/td[2]/text()').extract()[0]
			item['source'] = re.sub('^\s*: ', '', item['source'])
			item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[3]/td[1]')) :
			item['source'] = response.xpath('//div[@class="kcm-read-copy mb2"]/table/tbody/tr[3]/td[2]/text()').extract()[0]
			item['source'] = re.sub('^\s*: ', '', item['source'])
			item['source'] = re.sub('\s+$', '', item['source'])
		elif (response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[3]/td[1]')) :
			item['source'] = response.xpath('//div[@class="penulis-editor"]/table/tbody/tr[3]/td[2]/text()').extract()[0]
			item['source'] = re.sub('^\s*: ', '', item['source'])
			item['source'] = re.sub('\s+$', '', item['source'])

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
