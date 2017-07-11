import scrapy
import re
from metrotvnewscrawler.htmlparser import strip_tags
from metrotvnewscrawler.items import MetrotvnewsItem

class MetrotvnewsSpider(scrapy.Spider):
	name = "metrotvnews"
	allowed_domains = ["metrotvnews.com"]
	start_urls = [
		"http://www.metrotvnews.com/index"
	]

	def parse(self, response):
		for i in response.xpath('//div[@class="style_06"]/ul/li'):
			item = MetrotvnewsItem()
			#Media Label
			item['media'] = 'Metro TV'
			#Date
			date_cleaner = i.xpath('div[2]/text()').extract()[0]
			item['date'] = re.sub('^.+, ', '', date_cleaner)
			#item['date'] = re.sub(' - ', '', date_cleaner)
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			item['title'] = i.xpath('h2/a').extract()[0]
			item['title'] = strip_tags(item['title'])
			#Link
			item['link'] = i.xpath('h2/a/@href').extract()[0]
			#Sinopsis
			item['preview'] = i.xpath('p/text()').extract()[0]

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Author+Date
		authdate = response.xpath('//div[@class="reg"]/text()').extract()[0]
		authdate = authdate.replace(u' \u2022 ', u'||')
		authdate = re.sub('\\xa0', '', authdate)
		#date_cleaner = re.search('\|\| (.+?)$', authdate).group(1)
		#item['date'] = re.sub(' \S+$', '', date_cleaner)

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
		elif (bulan == 'Mei' or bulan =='May'):
			bulan = '05'
		elif (bulan == 'Jun'):
			bulan = '06'
		elif (bulan == 'Jul'):
			bulan = '07'
		elif (bulan == 'Agu' or bulan == 'Aug'):
			bulan = '08'
		elif (bulan == 'Sep'):
			bulan = '09'
		elif (bulan == 'Okt' or bulan == 'Oct'):
			bulan = '10'
		elif (bulan == 'Nov'):
			bulan = '11'
		elif (bulan == 'Des' or bulan == 'Dec'):
			bulan = '12'

		for y in range(len(item['date'])-10,len(item['date'])-6):
			tahun = tahun + item['date'][y]

		for y in range(len(item['date'])-5,len(item['date'])):
			jam = jam + item['date'][y]

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"

		#Content + Editor
		pc = 0
		text_sum = response.xpath('//div[@class="tru"]/p').extract()[0]
		text_sum = strip_tags(text_sum)
		text_check = response.xpath('//div[@class="tru"]/text()').extract()[pc]
		for p in response.xpath('//div[@class="tru"]/text()') :
			text_sum = text_sum + text_check
			pc = pc + 1
			try:
				text_check = response.xpath('//div[@class="tru"]/text()').extract()[pc]
			except:
				pass
		
		text_cleaner = re.sub('[\t\n\r\f\v]', '', text_sum)
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
		text_cleaner = re.sub('\s\s\s+', '', text_cleaner)
		#Editor
		try :
			item['editor'] = re.search('\((.{1,3})\)$', text_cleaner).group(1)
		except :
			pass
		#Author
		try :
			item['author'] = re.search('^ (.+?) \|\|', authdate).group(1)
		except :
			pass
		#Content Only
		item['cont'] = re.sub('\.\(.+$', '.', text_cleaner)

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
